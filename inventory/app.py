import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8080"))

# Per-process state: each Pod has its own copy of this.
ready = True


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/":
            self._send_json(200, {"status": "ok", "pod_name": socket.gethostname()})
        elif self.path == "/health":
            self._send_json(200, {"status": "ok"})
        elif self.path == "/ready":
            # The kubelet's readiness probe only looks at the status code.
            if ready:
                self._send_json(200, {"ready": True})
            else:
                self._send_json(503, {"ready": False})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        global ready
        if self.path == "/ready/fail":
            ready = False
            self._send_json(200, {"ready": ready, "pod_name": socket.gethostname()})
        elif self.path == "/ready/restore":
            ready = True
            self._send_json(200, {"ready": ready, "pod_name": socket.gethostname()})
        else:
            self._send_json(404, {"error": "not found"})


if __name__ == "__main__":
    # 0.0.0.0 = all interfaces; 127.0.0.1 would be unreachable from outside the container.
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"inventory listening on {PORT}", flush=True)
    server.serve_forever()
