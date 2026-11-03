"""Curated evidence extraction. Categories are review hints, never adoption verdicts."""
import csv
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError

from scanner import BASE, Blocked, Fetcher, count_keywords, visible_text

CATEGORIES = {'explicit coding-agent adoption', 'AI-assisted development',
              'AI security hiring', 'generic AI', 'other'}
FIELDS = ['company', 'source_title', 'source_url', 'publication_date',
          'publication_date_basis', 'matched_keywords', 'evidence_excerpt',
          'signal_category', 'fetch_status', 'fetch_detail', 'review_status',
          'evidence_origin', 'attribution', 'scan_date']


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title = []
        self.date = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        # Publication metadata only: do not mistake modification dates for publication.
        if tag == 'meta' and (attrs.get('property') or attrs.get('name', '')).lower() in {
                'article:published_time', 'datepublished'}:
            self.date = attrs.get('content', '')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def valid_date(value):
    """Accept explicit ISO dates only; never infer dates from a URL."""
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T.*)?', value):
        return ''
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).date().isoformat()
    except ValueError:
        return ''


def extract(html, keywords, evidence_anchor=""):
    metadata = Metadata()
    metadata.feed(html)
    text = visible_text(html)
    matches = [word for word, count in count_keywords(text, keywords).items() if count]
    # Keep an exact, short continuous span, rather than constructing a quotation.
    positions = [match.start() for word in matches for match in re.finditer(
        r'(?<!\w)' + r'\s+'.join(re.escape(p) for p in word.split()) + r'(?!\w)', text, re.I)]
    # A curated anchor selects relevant context only if it actually appears.
    if evidence_anchor and evidence_anchor not in text:
        raise ValueError('Curated evidence anchor not found; review source wording')
    start = text.index(evidence_anchor) if evidence_anchor else (min(positions) if positions else 0)
    # At most 24 exact consecutive words; no generated or stitched quotations.
    excerpt = ' '.join(text[start:].split()[:24]) if matches or evidence_anchor else ''
    # Deliberately conservative: no automated explicit-adoption or hiring classification.
    development = {'AI SDLC', 'AI-assisted software development', 'AI-assisted coding',
                   'AI coding assistants', 'GitHub Copilot', 'Claude Code', 'coding agents',
                   'agentic coding', 'developer productivity', 'developer experience'}
    category = 'AI-assisted development' if development.intersection(matches) else (
        'generic AI' if {'AI agents', 'agentic AI'}.intersection(matches) else 'other')
    date = valid_date(metadata.date)
    return {'source_title': ' '.join(' '.join(metadata.title).split()),
            'publication_date': date,
            'publication_date_basis': 'publisher HTML publication metadata; verify' if date else '',
            'matched_keywords': '|'.join(matches), 'evidence_excerpt': excerpt,
            'signal_category': category}


def scan_source(source, keywords, fetcher):
    row = dict.fromkeys(FIELDS, '')
    row.update(company=source['company'], source_url=source['source_url'],
               source_title=source.get('source_title', ''), signal_category='other',
               review_status='needs human verification', evidence_origin='automated fetch',
               scan_date=datetime.now(timezone.utc).isoformat())
    try:
        row.update(extract(fetcher.fetch(source['source_url'], html=True), keywords,
                           source.get('evidence_anchor', '')))
        row['fetch_status'] = 'success'
    except (HTTPError, URLError, OSError, ValueError, Blocked) as exc:
        restricted = isinstance(exc, Blocked) or (
            isinstance(exc, HTTPError) and exc.code in {301, 302, 303, 307, 308, 401, 403, 429})
        row.update(fetch_status='blocked' if restricted else 'error', fetch_detail=str(exc))
    return row


def manual_row(source, companies):
    """Import human-supplied evidence separately; never erase an automated failure."""
    if source['company'] not in companies:
        raise ValueError('Manual evidence company must appear in targets.csv')
    if not source.get('attribution', '').strip() or not source.get('verified_on', '').strip():
        raise ValueError('Manual evidence needs attribution and verified_on')
    if not valid_date(source['verified_on']):
        raise ValueError('verified_on must be an ISO date')
    if source.get('signal_category') not in CATEGORIES:
        raise ValueError('Unknown manual signal category')
    if source.get('publication_date') and not valid_date(source['publication_date']):
        raise ValueError('Publication date must be ISO or blank')
    if not source.get('source_url', '').startswith('https://') or not source.get('evidence_excerpt'):
        raise ValueError('Manual evidence needs a public HTTPS source URL and exact excerpt')
    row = {field: source.get(field, '') for field in FIELDS}
    row.update(fetch_status='not fetched (manual entry)', evidence_origin='human-supplied entry',
               review_status='human verification supplied; not independently checked',
               attribution=source['attribution'] + '; verified_on=' + source['verified_on'],
               scan_date=datetime.now(timezone.utc).isoformat())
    return row


def main():
    def read(name):
        with (BASE / name).open(newline='', encoding='utf-8') as handle:
            return list(csv.DictReader(handle))
    companies = [row['company'] for row in read('targets.csv')]
    sources = read('curated_sources.csv')
    if any(source['company'] not in companies for source in sources):
        raise ValueError('Curated companies must appear in targets.csv')
    keywords = (BASE / 'keywords.txt').read_text(encoding='utf-8').splitlines()
    fetcher = Fetcher()
    rows = []
    for source in sources:
        row = scan_source(source, keywords, fetcher)
        rows.append(row)
        print(f"{row['company']}: {row['fetch_status']}; {row['matched_keywords']}", flush=True)
    manual_path = BASE / 'manual_evidence.csv'
    if manual_path.exists():
        rows.extend(manual_row(source, companies) for source in read('manual_evidence.csv'))
    for company in companies:
        if not any(row['company'] == company for row in rows):
            row = dict.fromkeys(FIELDS, '')
            row.update(company=company, signal_category='other', fetch_status='not configured',
                       review_status='no curated source supplied',
                       scan_date=datetime.now(timezone.utc).isoformat())
            rows.append(row)
    with (BASE / 'evidence.csv').open('w', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    main()
