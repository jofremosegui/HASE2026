"""Serve the local HASE Lab dashboard; does not expose project or study files."""
import argparse
import errno
import json
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from hase_lab.live_checks import LiveChecks

ROOT = Path(__file__).resolve().parent
TASKS = ("workshops", "reviews", "buddies")
ASSETS = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
          "/style.css": ("style.css", "text/css")}
CHECKS = LiveChecks(ROOT)

class Handler(BaseHTTPRequestHandler):
    def send(self, status, content, mime):
        data = content.encode("utf-8") if isinstance(content, str) else content
        self.send_response(status)
        self.send_header("Content-Type", mime + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        request = urlsplit(self.path)
        if request.path in ASSETS:
            filename, mime = ASSETS[request.path]
            return self.send(200, (ROOT / "web" / filename).read_bytes(), mime)
        if request.path not in ("/api/preview", "/api/status"):
            return self.send(404, "Not found", "text/plain")
        query = parse_qs(request.query)
        task = query.get("task", [""])[0]
        actions = query.get("action", [])
        if task not in TASKS or len(actions) > 10 or any(len(a) > 80 for a in actions):
            return self.send(400, json.dumps({"error": "Invalid preview request"}), "application/json")
        try:
            if request.path == "/api/status":
                status = CHECKS.status(task, retry=query.get("retry") == ["1"])
                # Detailed test output remains in local researcher logs, not the dashboard.
                public = {key: status[key] for key in
                          ("all_passed", "fingerprint", "stale") if key in status}
                public["steps"] = [{key: step[key] for key in ("step", "passed")}
                                   for step in status.get("steps", [])]
                if status.get("error"):
                    public["error"] = "Checks could not finish. Check your saved Python files and try again."
                if status.get("log_warning"):
                    public["log_warning"] = "Local check results could not be saved. Please tell us."
                return self.send(200, json.dumps(public), "application/json")
            result = subprocess.run([sys.executable, "-B", "-m", "hase_lab.preview", task, *actions],
                                    cwd=ROOT, text=True, capture_output=True, timeout=5)
            if result.returncode:
                return self.send(422, json.dumps({"error": result.stderr[-5000:]}), "application/json")
            payload = json.loads(result.stdout)
            self.send(200, json.dumps(payload), "application/json")
        except subprocess.TimeoutExpired:
            self.send(504, json.dumps({"error": "Preview exceeded five seconds. Check for a loop in this task."}), "application/json")
        except (ValueError, OSError) as exc:
            self.send(500, json.dumps({"error": str(exc)}), "application/json")

    def log_message(self, fmt, *args):
        pass

def create_server(port=0):
    """Bind atomically: port 0 asks the OS to allocate a free local port."""
    try:
        return ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError as exc:
        if port and (exc.errno == errno.EADDRINUSE or getattr(exc, "winerror", None) == 10048):
            print(f"Port {port} is occupied; choosing a free local port.", flush=True)
            return ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        raise


def open_browser(url):
    try:
        if webbrowser.open(url):
            return
    except (webbrowser.Error, OSError):
        pass
    print(f"Open this address in your browser: {url}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0,
                        help="Optional preferred port; default: choose a free port automatically")
    parser.add_argument("--open", action="store_true", help="Open the local page in your browser")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")
    try:
        server = create_server(args.port)
    except OSError as exc:
        raise SystemExit(f"Cannot open a local server: {exc}. Ask us to check local security settings.")
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"HASE Lab: {url} (Ctrl+C to stop)", flush=True)
    if args.open:
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
