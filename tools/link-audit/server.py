"""Tiny local server for the Jev tools: serves this folder and proxies page fetches
so the browser can read any website (sites block direct browser reads)."""
import http.server, socketserver, urllib.request, urllib.parse, os

PORT = 8765
CACHE = {}  # url -> (final_url, body); makes repeat runs instant
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/fetch?"):
            url = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("url", [""])[0]
            if not url.startswith(("http://", "https://")):
                self.send_error(400, "bad url"); return
            if url in CACHE:
                final, body = CACHE[url]
                self.send_response(200); self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("X-Final-Url", final); self.end_headers(); self.wfile.write(body); return
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh) JevLinkAudit/1.0"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    body = r.read(); final = r.geturl()
                CACHE[url] = (final, body)
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("X-Final-Url", final)
                self.end_headers(); self.wfile.write(body)
            except Exception as e:
                self.send_error(502, str(e)[:200])
            return
        return super().do_GET()
    def log_message(self, *a): pass

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

print(f"Jev tools on http://localhost:{PORT}")
Server(("", PORT), Handler).serve_forever()
