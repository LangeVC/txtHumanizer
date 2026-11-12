#!/usr/bin/env python3
"""
Tests for the txt-humanizer local web server and JSON API ('serve' command).
"""
import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from txthumanizer import __version__
from txthumanizer.commands.serve_cmd import MAX_BODY_BYTES, create_server


class ServeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server("127.0.0.1", 0)
        self.port = self.server.server_address[1]
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def _request(self, method: str, path: str, body: bytes | None = None, headers: dict | None = None):
        req_headers = dict(headers or {})
        if body is not None and "Content-Type" not in req_headers:
            req_headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=body,
            headers=req_headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, dict(resp.headers), resp.read()
        except urllib.error.HTTPError as err:
            return err.code, dict(err.headers), err.read()

    def _post_json(self, path: str, payload: dict):
        raw = json.dumps(payload).encode("utf-8")
        return self._request("POST", path, body=raw)

    def test_get_root_html_offline(self):
        status, headers, raw = self._request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", headers.get("Content-Type", ""))
        html = raw.decode("utf-8")
        self.assertIn("txt-humanizer", html)
        self.assertIn("inputText", html)
        self.assertIn("langSelect", html)
        self.assertIn("checkBtn", html)
        self.assertIn("transformBtn", html)
        self.assertIn("outputText", html)
        for lang_code in ("auto", "de", "en", "fr", "es", "it", "pt", "vi"):
            self.assertIn(f'value="{lang_code}"', html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)

    def test_get_health(self):
        status, headers, raw = self._request("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers.get("Content-Type", ""))
        data = json.loads(raw.decode("utf-8"))
        self.assertEqual(data, {"status": "ok", "version": __version__})

    def test_post_detect(self):
        status, _, raw = self._post_json(
            "/api/detect",
            {"text": "Wir parkieren das Velo beim Spital."},
        )
        self.assertEqual(status, 200)
        data = json.loads(raw.decode("utf-8"))
        self.assertEqual(data["language"], "de")
        self.assertEqual(data["variety"], "de-CH")
        self.assertIn("human_signals", data)

    def test_post_check(self):
        suspect = (
            "This watershed moment serves as a testament to her enduring legacy, "
            "highlighting the importance of leadership."
        )
        status, _, raw = self._post_json("/api/check", {"text": suspect, "lang": "en"})
        self.assertEqual(status, 200)
        data = json.loads(raw.decode("utf-8"))
        self.assertIn(data["verdict"], ("clean", "review", "suspect"))
        self.assertIsInstance(data["score"], (int, float))
        self.assertEqual(data["language"], "en")
        self.assertIn("variety", data)
        self.assertIn("human_signals", data)
        self.assertGreater(len(data["matches"]), 0)

    def test_post_check_auto_lang(self):
        status, _, raw = self._post_json(
            "/api/check",
            {"text": "I walked the dog in the sunny park yesterday.", "lang": "auto"},
        )
        self.assertEqual(status, 200)
        data = json.loads(raw.decode("utf-8"))
        self.assertEqual(data["language"], "en")
        self.assertEqual(data["verdict"], "clean")

    def test_post_transform(self):
        status, _, raw = self._post_json(
            "/api/transform",
            {"text": "Wir möchten diese Maßnahmen zeitnah implementieren.", "lang": "de"},
        )
        self.assertEqual(status, 200)
        data = json.loads(raw.decode("utf-8"))
        self.assertEqual(data["language"], "de")
        self.assertGreater(data["changes_applied"], 0)
        self.assertIsInstance(data["replacements"], list)
        self.assertIn("umsetzen", data["result"])

    def test_post_400_on_empty_text(self):
        for endpoint in ("/api/detect", "/api/check", "/api/transform"):
            status, _, raw = self._post_json(endpoint, {"text": "   "})
            self.assertEqual(status, 400)
            data = json.loads(raw.decode("utf-8"))
            self.assertIn("error", data)

    def test_post_400_on_missing_text_and_malformed_json(self):
        status, _, raw = self._post_json("/api/check", {"lang": "en"})
        self.assertEqual(status, 400)
        self.assertIn("error", json.loads(raw.decode("utf-8")))

        status, _, raw = self._request("POST", "/api/check", body=b"{not-valid-json")
        self.assertEqual(status, 400)
        self.assertIn("error", json.loads(raw.decode("utf-8")))

        status, _, raw = self._request("POST", "/api/detect", body=b'["not", "an", "object"]')
        self.assertEqual(status, 400)
        self.assertIn("error", json.loads(raw.decode("utf-8")))

    def test_post_413_on_oversized_body(self):
        oversized = b'{"text": "' + (b"a" * (MAX_BODY_BYTES + 32)) + b'"}'
        status, _, raw = self._request("POST", "/api/check", body=oversized)
        self.assertEqual(status, 413)
        data = json.loads(raw.decode("utf-8"))
        self.assertIn("error", data)

    def test_404_on_unknown_endpoints(self):
        status, headers, raw = self._request("GET", "/api/does-not-exist")
        self.assertEqual(status, 404)
        self.assertIn("application/json", headers.get("Content-Type", ""))
        self.assertIn("error", json.loads(raw.decode("utf-8")))

        status, headers, raw = self._post_json("/api/unknown", {"text": "hello"})
        self.assertEqual(status, 404)
        self.assertIn("application/json", headers.get("Content-Type", ""))
        self.assertIn("error", json.loads(raw.decode("utf-8")))


if __name__ == "__main__":
    unittest.main()
