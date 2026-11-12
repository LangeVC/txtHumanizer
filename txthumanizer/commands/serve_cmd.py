"""
Handler for 'serve' subcommand — local web UI and stdlib JSON API server.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import sys
import urllib.parse
import webbrowser

from catalog.engine.detector import detect_language
from txthumanizer import __version__
from txthumanizer.commands.check_cmd import evaluate_text
from txthumanizer.commands.transform_cmd import apply_transforms
from txthumanizer.formatter import bold, cyan, dim

MAX_BODY_BYTES = 1_048_576

_HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>txt-humanizer — Review &amp; Humanization Studio</title>
  <style>
    :root {
      --bg: #0f172a;
      --surface: #1e293b;
      --surface-alt: #0b1220;
      --border: #334155;
      --text: #e2e8f0;
      --muted: #94a3b8;
      --accent: #38bdf8;
      --accent-strong: #0284c7;
      --green: #22c55e;
      --yellow: #eab308;
      --red: #ef4444;
      --radius: 10px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 24px 16px 48px;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }
    .container {
      max-width: 980px;
      margin: 0 auto;
    }
    header {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }
    h1 {
      margin: 0;
      font-size: 1.35rem;
      letter-spacing: -0.01em;
    }
    .subtitle {
      color: var(--muted);
      font-size: 0.9rem;
      margin-top: 2px;
    }
    .version-pill {
      font-size: 0.8rem;
      padding: 4px 10px;
      border-radius: 999px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--accent);
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px;
      margin-bottom: 18px;
    }
    .controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      margin-top: 12px;
    }
    label {
      font-size: 0.85rem;
      color: var(--muted);
      font-weight: 600;
    }
    select, button {
      font: inherit;
      border-radius: 8px;
      border: 1px solid var(--border);
      padding: 8px 14px;
      background: var(--surface-alt);
      color: var(--text);
    }
    button {
      cursor: pointer;
      font-weight: 600;
      transition: opacity 0.15s ease, background 0.15s ease;
    }
    button:hover:not(:disabled) { opacity: 0.9; }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    .btn-primary {
      background: var(--accent-strong);
      border-color: var(--accent);
      color: #fff;
    }
    .btn-secondary {
      background: #334155;
      border-color: #475569;
    }
    textarea {
      width: 100%;
      min-height: 180px;
      padding: 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--surface-alt);
      color: var(--text);
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.92rem;
      resize: vertical;
    }
    textarea:focus, select:focus {
      outline: 2px solid var(--accent);
      outline-offset: 1px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
    }
    @media (min-width: 820px) {
      .grid { grid-template-columns: 1fr 1fr; }
    }
    .badges {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 600;
      border: 1px solid var(--border);
      background: var(--surface-alt);
    }
    .badge-clean { border-color: var(--green); color: var(--green); }
    .badge-review { border-color: var(--yellow); color: var(--yellow); }
    .badge-suspect { border-color: var(--red); color: var(--red); }
    .badge-signal { border-color: var(--green); color: #86efac; }
    .badge-info { border-color: var(--accent); color: var(--accent); }
    .section-title {
      margin: 0 0 10px;
      font-size: 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .match-list {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .match-item {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 12px;
    }
    .match-header {
      display: flex;
      justify-content: space-between;
      gap: 8px;
      font-weight: 600;
      font-size: 0.9rem;
    }
    .evidence-list {
      margin: 6px 0 0;
      padding-left: 18px;
      color: var(--muted);
      font-size: 0.84rem;
    }
    .error-banner {
      display: none;
      margin-top: 12px;
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid var(--red);
      background: rgba(239, 68, 68, 0.12);
      color: #fca5a5;
      font-size: 0.9rem;
    }
    .muted { color: var(--muted); font-size: 0.88rem; }
    .rep-list {
      margin: 10px 0 0;
      padding-left: 18px;
      font-size: 0.85rem;
      color: var(--muted);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>txt-humanizer</h1>
        <div class="subtitle">Offline multilingual AI pattern review &amp; dialect-aware humanization</div>
      </div>
      <span class="version-pill">v__VERSION__</span>
    </header>

    <section class="card">
      <label for="inputText">Input Text</label>
      <textarea id="inputText" placeholder="Paste or type text to detect language, check AI patterns, and humanize..."></textarea>
      <div class="controls">
        <label for="langSelect">Language:</label>
        <select id="langSelect">
          <option value="auto" selected>auto</option>
          <option value="de">de</option>
          <option value="en">en</option>
          <option value="fr">fr</option>
          <option value="es">es</option>
          <option value="it">it</option>
          <option value="pt">pt</option>
          <option value="vi">vi</option>
        </select>
        <button id="checkBtn" type="button" class="btn-primary">Check</button>
        <button id="transformBtn" type="button" class="btn-secondary">Transform</button>
      </div>
      <div id="errorBanner" class="error-banner" role="alert"></div>
    </section>

    <div class="grid">
      <section class="card" aria-live="polite">
        <h2 class="section-title">Analysis &amp; Evidence</h2>
        <div id="badgesContainer" class="badges">
          <span class="muted">Run Check to inspect verdict score, dialect variety, and human signals.</span>
        </div>
        <ul id="evidenceList" class="match-list"></ul>
      </section>

      <section class="card" aria-live="polite">
        <div class="section-title">
          <span>Transformed Output</span>
          <button id="copyBtn" type="button" class="btn-secondary">Copy</button>
        </div>
        <textarea id="outputText" readonly placeholder="Transformed text will appear here..."></textarea>
        <div id="transformSummary" class="muted" style="margin-top:8px;"></div>
        <ul id="replacementsList" class="rep-list"></ul>
      </section>
    </div>
  </div>

  <script>
    (function () {
      const inputEl = document.getElementById("inputText");
      const langEl = document.getElementById("langSelect");
      const checkBtn = document.getElementById("checkBtn");
      const transformBtn = document.getElementById("transformBtn");
      const copyBtn = document.getElementById("copyBtn");
      const errorBanner = document.getElementById("errorBanner");
      const badgesContainer = document.getElementById("badgesContainer");
      const evidenceList = document.getElementById("evidenceList");
      const outputText = document.getElementById("outputText");
      const transformSummary = document.getElementById("transformSummary");
      const replacementsList = document.getElementById("replacementsList");

      function showError(msg) {
        errorBanner.textContent = msg;
        errorBanner.style.display = msg ? "block" : "none";
      }

      function makeBadge(label, cls) {
        const span = document.createElement("span");
        span.className = "badge " + (cls || "");
        span.textContent = label;
        return span;
      }

      async function postJson(url, payload) {
        const resp = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await resp.json();
        if (!resp.ok) {
          throw new Error(data.error || ("Request failed with status " + resp.status));
        }
        return data;
      }

      function buildPayload() {
        const text = inputEl.value;
        const lang = langEl.value === "auto" ? null : langEl.value;
        return lang ? { text: text, lang: lang } : { text: text };
      }

      function renderCheck(data) {
        badgesContainer.innerHTML = "";
        evidenceList.innerHTML = "";

        const verdict = (data.verdict || "unknown").toLowerCase();
        const score = typeof data.score === "number" ? data.score : 0;
        const verdictClass = verdict === "clean"
          ? "badge-clean"
          : (verdict === "review" ? "badge-review" : "badge-suspect");

        badgesContainer.appendChild(
          makeBadge("Verdict: " + verdict.toUpperCase() + " (" + score + ")", verdictClass)
        );
        badgesContainer.appendChild(
          makeBadge("Language: " + String(data.language || "?").toUpperCase(), "badge-info")
        );
        badgesContainer.appendChild(
          makeBadge("Variety: " + String(data.variety || "standard"), "badge-info")
        );

        const signals = Array.isArray(data.human_signals) ? data.human_signals : [];
        if (signals.length > 0) {
          signals.forEach(function (sig) {
            const name = sig && sig.name ? sig.name : String(sig);
            badgesContainer.appendChild(makeBadge("Human Signal: " + name, "badge-signal"));
          });
        } else {
          badgesContainer.appendChild(makeBadge("Human Signals: none", ""));
        }

        const matches = Array.isArray(data.matches) ? data.matches : [];
        if (matches.length === 0) {
          const li = document.createElement("li");
          li.className = "muted";
          li.textContent = "No AI pattern triggers detected.";
          evidenceList.appendChild(li);
          return;
        }

        matches.forEach(function (m) {
          const li = document.createElement("li");
          li.className = "match-item";

          const header = document.createElement("div");
          header.className = "match-header";
          const title = document.createElement("span");
          title.textContent = "[Tier " + m.tier + "] " + m.name + " (" + m.id + ")";
          const pts = document.createElement("span");
          pts.textContent = "+" + m.penalty + " pts (x" + m.count + ")";
          header.appendChild(title);
          header.appendChild(pts);
          li.appendChild(header);

          if (Array.isArray(m.evidence) && m.evidence.length > 0) {
            const evUl = document.createElement("ul");
            evUl.className = "evidence-list";
            m.evidence.forEach(function (ev) {
              const evLi = document.createElement("li");
              evLi.textContent = "L" + ev.line + ": \"" + ev.snippet + "\"";
              evUl.appendChild(evLi);
            });
            li.appendChild(evUl);
          }

          evidenceList.appendChild(li);
        });
      }

      function renderTransform(data) {
        outputText.value = data.result || "";
        const count = data.changes_applied || 0;
        const langOut = String(data.language || "?").toUpperCase();
        transformSummary.textContent = "Language: " + langOut + " · Changes applied: " + count;

        replacementsList.innerHTML = "";
        const reps = Array.isArray(data.replacements) ? data.replacements : [];
        reps.forEach(function (r) {
          const li = document.createElement("li");
          li.textContent = r.target + " -> " + r.replacement + " (x" + r.count + ")";
          replacementsList.appendChild(li);
        });
      }

      async function handleAction(btn, endpoint, renderer) {
        showError("");
        btn.disabled = true;
        try {
          const data = await postJson(endpoint, buildPayload());
          renderer(data);
        } catch (err) {
          showError(err.message || "Unexpected error");
        } finally {
          btn.disabled = false;
        }
      }

      checkBtn.addEventListener("click", function () {
        handleAction(checkBtn, "/api/check", renderCheck);
      });

      transformBtn.addEventListener("click", function () {
        handleAction(transformBtn, "/api/transform", renderTransform);
      });

      copyBtn.addEventListener("click", async function () {
        if (!outputText.value) return;
        try {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(outputText.value);
          } else {
            outputText.select();
            document.execCommand("copy");
          }
          const orig = copyBtn.textContent;
          copyBtn.textContent = "Copied";
          setTimeout(function () { copyBtn.textContent = orig; }, 1200);
        } catch (_) {
          outputText.select();
        }
      });
    })();
  </script>
</body>
</html>
"""


class _RequestError(Exception):
    """HTTP error with status code and message."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def _send_bytes(handler: BaseHTTPRequestHandler, status: int, content_type: str, body: bytes) -> None:
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    _send_bytes(handler, status, "application/json; charset=utf-8", encoded)


def _html_response(handler: BaseHTTPRequestHandler, status: int, html_body: str) -> None:
    _send_bytes(handler, status, "text/html; charset=utf-8", html_body.encode("utf-8"))


def _extract_text_and_lang(data: dict, allow_lang: bool = True) -> tuple[str, str | None]:
    text = data.get("text")
    if not isinstance(text, str) or not text.strip():
        raise _RequestError(400, "Field 'text' must be a non-empty string")

    if not allow_lang:
        return text, None

    lang = data.get("lang")
    if lang is None:
        return text, None
    if not isinstance(lang, str):
        raise _RequestError(400, "Field 'lang' must be a string")

    lang_clean = lang.strip().lower()
    if lang_clean in ("", "auto"):
        return text, None
    return text, lang_clean


class HumanizerRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler serving the offline UI and JSON endpoints."""

    server_version = f"txt-humanizer/{__version__}"

    def log_message(self, format: str, *args) -> None:
        if getattr(self.server, "quiet", False):
            return
        super().log_message(format, *args)

    def _drain_excess_body(self, content_length: int) -> None:
        """Drain small oversized bodies in fixed chunks to prevent TCP RST on client send."""
        remaining = min(content_length, MAX_BODY_BYTES * 2)
        prev_timeout = self.connection.gettimeout()
        self.connection.settimeout(0.2)
        try:
            while remaining > 0:
                chunk = self.rfile.read(min(65_536, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
        except OSError:
            pass
        finally:
            self.connection.settimeout(prev_timeout)

    def _read_json_body(self) -> dict:
        raw_len = self.headers.get("Content-Length")
        if raw_len is None:
            raise _RequestError(400, "Missing Content-Length header")

        try:
            content_length = int(raw_len)
        except ValueError as exc:
            raise _RequestError(400, "Invalid Content-Length header") from exc

        if content_length < 0:
            raise _RequestError(400, "Invalid Content-Length header")
        if content_length > MAX_BODY_BYTES:
            self.close_connection = True
            self._drain_excess_body(content_length)
            raise _RequestError(413, f"Request body exceeds {MAX_BODY_BYTES} bytes")

        raw_body = self.rfile.read(content_length)
        if len(raw_body) != content_length:
            raise _RequestError(400, "Incomplete request body")

        try:
            decoded = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise _RequestError(400, "Request body must be valid UTF-8") from exc

        try:
            data = json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise _RequestError(400, f"Malformed JSON: {exc.msg}") from exc

        if not isinstance(data, dict):
            raise _RequestError(400, "JSON body must be an object")

        return data

    def do_GET(self) -> None:
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            _html_response(self, 200, _HTML_PAGE.replace("__VERSION__", __version__))
        elif path == "/api/health":
            _json_response(self, 200, {"status": "ok", "version": __version__})
        else:
            _json_response(self, 404, {"error": f"Unknown endpoint: {path}"})

    def do_POST(self) -> None:
        path = urllib.parse.urlparse(self.path).path
        if path not in ("/api/detect", "/api/check", "/api/transform"):
            self.close_connection = True
            _json_response(self, 404, {"error": f"Unknown endpoint: {path}"})
            return

        try:
            data = self._read_json_body()
            if path == "/api/detect":
                text, _ = _extract_text_and_lang(data, allow_lang=False)
                _json_response(self, 200, detect_language(text))
            elif path == "/api/check":
                text, lang = _extract_text_and_lang(data, allow_lang=True)
                _json_response(self, 200, evaluate_text(text, lang=lang))
            elif path == "/api/transform":
                text, lang = _extract_text_and_lang(data, allow_lang=True)
                transformed, count, changes, lang_out = apply_transforms(text, lang=lang)
                _json_response(
                    self,
                    200,
                    {
                        "language": lang_out,
                        "changes_applied": count,
                        "replacements": changes,
                        "result": transformed,
                    },
                )
        except _RequestError as err:
            _json_response(self, err.status, {"error": err.message})
        except Exception as exc:
            _json_response(self, 500, {"error": str(exc)})


class HumanizerServer(ThreadingHTTPServer):
    """Threaded stdlib HTTP server with daemon request threads."""

    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address: tuple[str, int], RequestHandlerClass, quiet: bool = True):
        self.quiet = quiet
        super().__init__(server_address, RequestHandlerClass)


def create_server(host: str = "127.0.0.1", port: int = 8080, quiet: bool = True) -> ThreadingHTTPServer:
    """Create and bind a ThreadingHTTPServer for txt-humanizer."""
    return HumanizerServer((host, port), HumanizerRequestHandler, quiet=quiet)


def run_serve(args, is_json: bool = False) -> int:
    """Start the local web UI and JSON API server."""
    host = getattr(args, "host", "127.0.0.1")
    port = int(getattr(args, "port", 8080))
    silent = bool(getattr(args, "silent", False))
    server = create_server(host, port, quiet=(is_json or silent))

    bound_host, bound_port = server.server_address[:2]
    browser_host = "127.0.0.1" if bound_host == "0.0.0.0" else bound_host
    url = f"http://{browser_host}:{bound_port}"

    if is_json:
        print(
            json.dumps(
                {
                    "status": "serving",
                    "url": url,
                    "host": bound_host,
                    "port": bound_port,
                    "version": __version__,
                }
            ),
            flush=True,
        )
    elif not silent:
        print(f"{bold('txt-humanizer web server')} listening on {cyan(url)}", flush=True)
        print(dim("Press Ctrl+C to stop."), flush=True)

    if getattr(args, "open", False):
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        if not is_json and not silent:
            sys.stdout.write("\nShutting down server.\n")
    finally:
        server.server_close()

    return 0
