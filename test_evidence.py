"""Offline evidence tests; all source content is fictional."""
import unittest
from unittest.mock import patch

from evidence_scanner import extract, manual_row, scan_source
from scanner import Blocked, Fetcher


class EvidenceTests(unittest.TestCase):
    def test_title_date_and_exact_excerpt(self):
        html = ('<title>Fictional engineering</title>'
                '<meta property="article:published_time" content="2026-02-12T10:00:00Z">'
                '<p>We are evaluating GitHub Copilot for AI-assisted coding.</p>')
        row = extract(html, ['GitHub Copilot', 'AI-assisted coding', 'Cursor'])
        self.assertEqual(row['source_title'], 'Fictional engineering')
        self.assertEqual(row['publication_date'], '2026-02-12')
        self.assertEqual(row['matched_keywords'], 'GitHub Copilot|AI-assisted coding')
        self.assertEqual(row['evidence_excerpt'],
                         'GitHub Copilot for AI-assisted coding.')
        self.assertEqual(row['signal_category'], 'AI-assisted development')

    def test_curated_anchor_must_exist_and_excerpt_is_exact(self):
        html = '<p>Navigation Claude Code. Our engineers use a coding agent regularly.</p>'
        row = extract(html, ['Claude Code'], 'Our engineers')
        self.assertEqual(row['evidence_excerpt'], 'Our engineers use a coding agent regularly.')
        with self.assertRaises(ValueError):
            extract(html, ['Claude Code'], 'Invented statement')

    def test_no_adoption_claim_from_keyword_or_negation(self):
        for text in ['We use Claude Code.', 'We do not use Claude Code.']:
            row = extract('<p>' + text + '</p>', ['Claude Code'])
            self.assertNotEqual(row['signal_category'], 'explicit coding-agent adoption')
        row = extract('<p>AI security hiring plans are unconfirmed.</p>', ['AI security'])
        self.assertEqual(row['signal_category'], 'other')

    def test_missing_invalid_and_modified_dates_stay_blank(self):
        for html in ['<p>2026 is exciting.</p>',
                     '<meta property="article:modified_time" content="2026-01-01">',
                     '<meta property="article:published_time" content="2026-02-31">']:
            self.assertEqual(extract(html, [])['publication_date'], '')

    def test_failed_fetch_has_no_invented_evidence(self):
        with patch.object(Fetcher, 'fetch', side_effect=Blocked('robots denied')):
            row = scan_source({'company': 'Fictional', 'source_title': 'Supplied title',
                               'source_url': 'https://fictional.example/article'},
                              ['Claude Code'], Fetcher())
        self.assertEqual(row['fetch_status'], 'blocked')
        self.assertEqual(row['fetch_detail'], 'robots denied')
        for key in ['matched_keywords', 'evidence_excerpt', 'publication_date']:
            self.assertEqual(row[key], '')
        self.assertEqual(row['review_status'], 'needs human verification')

    def test_manual_entry_requires_attribution_and_stays_separate(self):
        source = {'company': 'Fictional', 'source_url': 'https://fictional.example/article',
                  'signal_category': 'explicit coding-agent adoption',
                  'evidence_excerpt': 'We use a coding agent.'}
        with self.assertRaises(ValueError):
            manual_row(source, ['Fictional'])
        source.update(attribution='Fictional reviewer; publisher page', verified_on='2026-11-01')
        row = manual_row(source, ['Fictional'])
        self.assertEqual(row['fetch_status'], 'not fetched (manual entry)')
        self.assertEqual(row['evidence_origin'], 'human-supplied entry')
        self.assertIn('not independently checked', row['review_status'])
        self.assertEqual(row['publication_date'], '')


if __name__ == '__main__':
    unittest.main()
