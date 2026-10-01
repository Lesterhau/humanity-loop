#!/usr/bin/env python3
"""Tiny read-only status API for a serialized Foundry control-plane snapshot."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class StatusHandler(BaseHTTPRequestHandler):
    state_path: Path

    def do_GET(self):
        if self.path not in {"/", "/status", "/health"}:
            self.send_response(404)
            self.end_headers()
            return
        if self.path == "/health":
            payload = {"ok": True}
        else:
            try:
                payload = json.loads(self.state_path.read_text())
            except FileNotFoundError:
                payload = {
                    "active_agents": [],
                    "current_tasks": [],
                    "recent_outcomes": [],
                    "failures": [],
                    "usage": [],
                    "events": [],
                }
        body = json.dumps(payload, default=str).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", default="runtime/foundry-control-plane/state.json")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    StatusHandler.state_path = Path(args.state)
    ThreadingHTTPServer((args.host, args.port), StatusHandler).serve_forever()


if __name__ == "__main__":
    main()
