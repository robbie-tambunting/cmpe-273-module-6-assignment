import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080

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
            # TODO: respond 200 with JSON that includes this Pod's name.
            #       Where does a container get its Pod name from? (see Q1 answer)
            pass
        elif self.path == "/health":
            # TODO: always 200 (liveness-style check)
            pass
        elif self.path == "/ready":
            # TODO: 200 if `ready` is True, otherwise 503
            pass
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        global ready
        if self.path == "/ready/fail":
            # TODO: flip the flag so /ready starts failing, then respond
            pass
        elif self.path == "/ready/restore":
            # TODO: flip it back, then respond
            pass
        else:
            self._send_json(404, {"error": "not found"})


if __name__ == "__main__":
    # TODO: which address must we bind to so the container is reachable
    #       from outside itself? ("127.0.0.1" will NOT work in a container)
    server = HTTPServer(("TODO", PORT), Handler)
    print(f"inventory listening on {PORT}", flush=True)
    server.serve_forever()
