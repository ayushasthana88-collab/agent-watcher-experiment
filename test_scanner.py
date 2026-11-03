"""Offline tests use only fictional HTML and mocked network responses."""
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from scanner import Blocked, Fetcher, count_keywords, scan_company, visible_text


class ScannerTests(unittest.TestCase):
    def test_counts_and_text(self):
        text = visible_text('<p>CLAUDE <b>Code</b> and Claude Code.</p>'
                            '<script>Cursor</script><style>Cursor</style>'
                            '<p>cursors application security AI agents</p>')
        self.assertEqual(count_keywords(text, ['Claude Code', 'Cursor', 'AI agents']),
                         {'Claude Code': 2, 'Cursor': 0, 'AI agents': 1})

    def test_robots_disallow_prevents_page_request(self):
        fetcher = Fetcher()
        with patch.object(fetcher, 'request', return_value=(
                'User-agent: *\nDisallow: /private', 'text/plain')) as request:
            with self.assertRaises(Blocked):
                fetcher.fetch('https://fictional.example/private')
            request.assert_called_once_with('https://fictional.example/robots.txt')

    def test_robots_failure_prevents_page_request(self):
        fetcher = Fetcher()
        with patch.object(fetcher, 'request', side_effect=HTTPError(
                'https://fictional.example/robots.txt', 403, 'Forbidden', {}, None)) as request:
            with self.assertRaises(Blocked):
                fetcher.fetch('https://fictional.example/page')
            self.assertEqual(request.call_count, 1)

    def test_partial_failure_keeps_real_counts_and_details(self):
        fetcher = Fetcher()
        with patch.object(fetcher, 'fetch', side_effect=['AI agents', Blocked('denied')]):
            row = scan_company({'company': 'Fictional', 'source_urls':
                                'https://fictional.example/a|https://fictional.example/b'},
                               ['AI agents'], fetcher)
        self.assertEqual(row['total_keyword_matches'], 1)
        self.assertEqual(row['generic_ai_mentions'], 1)
        self.assertEqual(row['coding_specific_mentions'], 0)
        self.assertEqual(row['scan_status'], 'blocked')
        self.assertEqual(row['successful_pages'], 1)


if __name__ == '__main__':
    unittest.main()
