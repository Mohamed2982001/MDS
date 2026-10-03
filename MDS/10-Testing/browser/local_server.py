#!/usr/bin/env python3
"""
MDS Ephemeral Local HTTP Test Server
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Provides an ephemeral, isolated HTTP daemon for serving MDS runtime and reference
application assets to headless browser sessions. Supports dynamic port allocation (port 0),
CORS headers for ES module loading, and clean deterministic teardown.
"""

import sys
import time
import socket
import threading
import urllib.request
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Optional

from .exceptions import ServerStartupError


class MDSHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    HTTP Request Handler serving static files with open CORS and cache-busting headers
    required for browser ES modules (`import ... from "../Runtime/..."`) and local testing.
    """

    def end_headers(self):
        # Mandatory CORS headers for local ES module execution
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

    def log_message(self, format, *args):
        # Quiet mode: suppress logging unless explicitly enabled
        if getattr(self.server, "verbose_logging", False):
            super().log_message(format, *args)


CHROMIUM_RESTRICTED_PORTS = {
    1, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 25, 37, 42, 43, 53, 77, 79, 87, 95,
    101, 102, 103, 104, 109, 110, 111, 113, 115, 117, 119, 123, 135, 139, 143, 179,
    389, 465, 512, 513, 514, 515, 526, 530, 531, 532, 540, 556, 563, 587, 601, 636,
    993, 995, 1719, 1720, 1723, 2049, 3659, 4045, 5060, 5061, 6000, 6566, 6665, 6666,
    6667, 6668, 6669, 6697, 10080,
}


class LocalTestServer:
    """
    Manages an ephemeral local HTTP server instance running in a dedicated background thread.
    """

    def __init__(
        self,
        serve_dir: Optional[Path] = None,
        port: int = 0,
        host: str = "127.0.0.1",
        verbose: bool = False
    ):
        if serve_dir is None:
            # Default to workspace root (parent of MDS)
            self.serve_dir = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.serve_dir = Path(serve_dir).resolve()

        self.requested_port = port
        self.host = host
        self.verbose = verbose
        self.port: Optional[int] = None
        self._httpd: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self._is_running = False

    @property
    def is_running(self) -> bool:
        return self._is_running and self._httpd is not None

    def start(self, timeout_sec: float = 5.0) -> int:
        """
        Starts the local server on an ephemeral or requested port and verifies readiness.
        Returns the bound port.
        """
        if self._is_running:
            return self.port  # Already running

        # Custom handler factory that binds serve_dir
        serve_dir_str = str(self.serve_dir)

        class CustomDirHandler(MDSHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=serve_dir_str, **kwargs)

        for attempt in range(20):
            try:
                self._httpd = HTTPServer((self.host, self.requested_port), CustomDirHandler)
                self._httpd.verbose_logging = self.verbose
                self.port = self._httpd.server_port
                if self.requested_port == 0 and self.port in CHROMIUM_RESTRICTED_PORTS:
                    self._httpd.server_close()
                    continue
                break
            except Exception as e:
                if attempt == 19:
                    raise ServerStartupError(f"Failed to bind HTTP server to {self.host}:{self.requested_port} - {e}")
                time.sleep(0.05)

        # Start server in a background daemon thread
        self._thread = threading.Thread(
            target=self._httpd.serve_forever,
            name=f"MDSServerThread-{self.port}",
            daemon=True
        )
        self._thread.start()
        self._is_running = True

        # Health check poll to ensure server socket is actively accepting requests
        start_time = time.time()
        health_url = f"http://{self.host}:{self.port}/"
        ready = False

        while time.time() - start_time < timeout_sec:
            try:
                with urllib.request.urlopen(health_url, timeout=0.5) as resp:
                    if resp.status in (200, 301, 302, 404):
                        ready = True
                        break
            except Exception:
                time.sleep(0.05)

        if not ready:
            self.stop()
            raise ServerStartupError(
                f"Local test server failed health check on {health_url} within {timeout_sec}s"
            )

        return self.port

    def stop(self) -> None:
        """Shuts down the server and releases socket resources cleanly."""
        if not self._is_running:
            return

        self._is_running = False
        if self._httpd:
            try:
                self._httpd.shutdown()
                self._httpd.server_close()
            except Exception:
                pass
            self._httpd = None

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
            self._thread = None

    def get_url(self, relative_path: str = "") -> str:
        """Constructs a fully qualified HTTP URL for the given relative path."""
        if not self.is_running:
            raise RuntimeError("Cannot construct URL: LocalTestServer is not running.")
        clean_path = relative_path.lstrip("/\\").replace("\\", "/")
        return f"http://{self.host}:{self.port}/{clean_path}"

    def __enter__(self) -> "LocalTestServer":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()
