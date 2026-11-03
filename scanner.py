"""Small, conservative public-page prospecting scanner; standard library only."""
import argparse
import csv
import json
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.robotparser import RobotFileParser

BASE = Path(__file__).resolve().parent
USER_AGENT = "AgentWatcherProspecting/1.0 (personal research; public pages only)"
TIMEOUT = 15
MAX_BYTES = 2_000_000
DIRECT = {"Claude Code", "OpenAI Codex", "Cursor", "coding agents", "GitHub Copilot", "agentic coding"}
SECURITY = {"application security", "product security", "AI security", "secure software development", "prompt injection"}


class Blocked(Exception):
    """Access is restricted or cannot safely be established."""


class NoRedirect(HTTPRedirectHandler):
    # Stop rather than silently following an unchecked destination.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class PageText(HTMLParser):
    """Extract text, excluding scripts, CSS, templates and hidden HTML."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        hidden = (tag in {"script", "style", "noscript", "template"}
                  or "hidden" in attrs or attrs.get("aria-hidden") == "true")
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img",
                       "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, hidden))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not any(hidden for _, hidden in self.stack):
            self.parts.append(data)


def visible_text(html):
    parser = PageText()
    parser.feed(html)
    return " ".join(" ".join(parser.parts).split())


def count_keywords(text, keywords):
    # Whole phrases, case insensitive, allowing whitespace between words.
    return {word: len(re.findall(r"(?<!\w)" + r"\s+".join(
        re.escape(part) for part in word.split()) + r"(?!\w)", text, re.I))
        for word in keywords}


class Fetcher:
    def __init__(self):
        self.opener = build_opener(NoRedirect())
        self.robots = {}
        self.last_request = {}

    def request(self, url):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username:
            raise Blocked("Only public HTTPS URLs without credentials are supported")
        origin = f"{parsed.scheme}://{parsed.netloc}"
        time.sleep(max(0, self.last_request.get(origin, 0) + 1 - time.monotonic()))
        self.last_request[origin] = time.monotonic()
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with self.opener.open(req, timeout=TIMEOUT) as response:
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise ValueError("Response exceeds 2 MB limit")
            return raw.decode(response.headers.get_content_charset() or "utf-8",
                              errors="replace"), response.headers.get_content_type()

    def fetch(self, url, *, html=False):
        parsed = urlsplit(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin not in self.robots:
            try:
                body, _ = self.request(origin + "/robots.txt")
                if body.lstrip().startswith("<"):
                    raise Blocked("robots.txt returned HTML; permission unknown")
                robot = RobotFileParser()
                robot.parse(body.splitlines())
                self.robots[origin] = robot
            except (HTTPError, URLError, OSError, ValueError, Blocked) as exc:
                # Fail closed, including missing robots.txt; no page fetch follows.
                self.robots[origin] = str(exc)
        robot = self.robots[origin]
        if isinstance(robot, str):
            raise Blocked("Could not verify robots.txt: " + robot)
        if not robot.can_fetch(USER_AGENT, url):
            raise Blocked("Disallowed by robots.txt")
        delay = robot.crawl_delay(USER_AGENT) or 1
        rate = robot.request_rate(USER_AGENT)
        if rate:
            delay = max(delay, rate.seconds / rate.requests)
        if delay > 60:
            raise Blocked("Requested crawl delay exceeds this scanner's 60s limit")
        time.sleep(max(0, self.last_request.get(origin, 0) + delay - time.monotonic()))
        body, content_type = self.request(url)
        if content_type != "text/html":
            raise ValueError("Expected an HTML page")
        text = visible_text(body)
        if re.search(r"verify (?:you are|you're) human|access denied|just a moment|"
                     r"captcha|enable javascript and cookies", text, re.I):
            raise Blocked("Possible access challenge; page not counted")
        if not text.strip():
            raise ValueError("No readable HTML text")
        return body if html else text


def scan_company(target, keywords, fetcher):
    counts = dict.fromkeys(keywords, 0)
    pages = []
    urls = target["source_urls"].split("|")
    for url in urls:
        try:
            page_counts = count_keywords(fetcher.fetch(url), keywords)
            counts = {key: counts[key] + page_counts[key] for key in keywords}
            pages.append({"url": url, "status": "success", "counts": page_counts})
        except (HTTPError, URLError, OSError, ValueError, Blocked) as exc:
            restricted = isinstance(exc, Blocked) or (
                isinstance(exc, HTTPError) and exc.code in {301, 302, 303, 307, 308,
                                                                         401, 403, 429})
            pages.append({"url": url, "status": "blocked" if restricted else "error",
                          "detail": str(exc)})
    statuses = {page["status"] for page in pages}
    # A company is successful only if ALL configured pages succeeded.
    status = "error" if "error" in statuses else "blocked" if "blocked" in statuses else "success"
    return {"company": target["company"], "total_keyword_matches": sum(counts.values()),
            **counts, "coding_specific_mentions": sum(counts[k] for k in DIRECT if k in counts),
            "security_mentions": sum(counts[k] for k in SECURITY if k in counts),
            "generic_ai_mentions": sum(counts[k] for k in {"AI agents", "agentic AI"} if k in counts),
            "source_urls": "|".join(urls), "scan_date": datetime.now(timezone.utc).isoformat(),
            "scan_status": status, "successful_pages": sum(p["status"] == "success" for p in pages),
            "page_results": json.dumps(pages, ensure_ascii=False)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--curated", action="store_true", help="Write evidence.csv from curated sources")
    args = parser.parse_args()
    if args.curated:
        from evidence_scanner import main as evidence_main
        evidence_main()
        return
    keywords = [line.strip() for line in (BASE / "keywords.txt").read_text().splitlines()
                if line.strip()]
    with (BASE / "targets.csv").open(newline="", encoding="utf-8") as source:
        targets = list(csv.DictReader(source))
    fetcher = Fetcher()
    rows = []
    for target in targets:
        row = scan_company(target, keywords, fetcher)
        rows.append(row)
        print(f"{row['company']}: {row['total_keyword_matches']} matches; {row['scan_status']}", flush=True)
    rows.sort(key=lambda row: (-row["total_keyword_matches"], row["company"].casefold()))
    with (BASE / "ranked_targets_latest.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
