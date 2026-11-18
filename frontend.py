#!/usr/bin/env python3
"""Frontend server (runs next to Nginx).

Listens on port 1337. On every GET it first calls the backend, then replies:
  "Webserver <own hostname> is responding using backend <backend hostname>"
"""
import os
import socket
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 1337
HOSTNAME = socket.gethostname()
BACKEND_URL = "http://<PLACEHOLDER>:1337"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with urllib.request.urlopen(BACKEND_URL, timeout=3) as resp:
                backend = resp.read().decode().strip()
            status = 200
            body = f"Webserver {HOSTNAME} is responding using backend {backend}\n"
        except Exception as exc:
            status = 502
            body = f"Webserver {HOSTNAME} could not reach backend at {BACKEND_URL}: {exc}\n"

        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"Frontend {HOSTNAME} listening on :{PORT}, backend={BACKEND_URL}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
