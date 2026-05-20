#!/usr/bin/env python3
"""Serve les démos avec Content-Disposition: inline pour les PDF (iframe native)."""
from __future__ import annotations

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class DemoHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        if self.path.split("?", 1)[0].lower().endswith(".pdf"):
            self.send_header("Content-Disposition", "inline")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8765)
    args = parser.parse_args()
    server = HTTPServer(("", args.port), DemoHandler)
    print(f"Démos → http://127.0.0.1:{args.port}/demo-viewer-native.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
