#!/usr/bin/env python3
"""Backend server (runs next to Redis).

Listens on port 1337 and answers every GET with the pod's hostname.
"""
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 1337
HOSTNAME = socket.gethostname()  # containers in a pod share a hostname = pod name


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"{HOSTNAME}\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Backend {HOSTNAME} listening on :{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
