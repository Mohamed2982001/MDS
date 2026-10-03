#!/usr/bin/env python3
"""
MDS Chrome DevTools Protocol (CDP) Browser Driver
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standard-library based, zero-external-dependency CDP browser driver.
Communicates directly with Chromium (Chrome, Edge, Chromium) via RFC 6455
WebSocket protocol over standard Python sockets.
"""

import os
import sys
import time
import json
import base64
import struct
import socket
import tempfile
import shutil
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, List, Dict, Any

from .models import Viewport, ConsoleLogEntry, ConsoleLogLevel, BrowserInfo, BrowserType
from .driver_base import BrowserDriverBase
from .browser_discovery import BrowserDiscovery
from .exceptions import (
    BrowserBridgeError,
    BrowserNotFoundError,
    BrowserLaunchError,
    CDPConnectionError,
    CDPCommandError,
    NavigationError,
    TimeoutError,
    ElementNotFoundError,
    InvalidCommandError,
)


class _CDPSocketClient:
    """
    Minimal synchronous RFC 6455 WebSocket client communicating over raw TCP sockets.
    Provides deterministic JSON-RPC 2.0 dispatch and CDP event parsing with 0 external dependencies.
    """

    def __init__(self, ws_url: str, timeout: float = 15.0):
        self.ws_url = ws_url
        parsed = urllib.parse.urlparse(ws_url)
        self.host = parsed.hostname or "127.0.0.1"
        self.port = parsed.port or 9222
        self.path = parsed.path
        if parsed.query:
            self.path += f"?{parsed.query}"

        self.timeout = timeout
        self.sock: Optional[socket.socket] = None
        self._next_id = 1
        self._is_closed = False

        self._connect()

    def _connect(self):
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
            self.sock.settimeout(self.timeout)
            self._handshake()
        except Exception as e:
            raise CDPConnectionError(f"Failed to connect to CDP WebSocket at {self.ws_url}: {e}")

    def _handshake(self):
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        headers = [
            f"GET {self.path} HTTP/1.1",
            f"Host: {self.host}:{self.port}",
            "Upgrade: websocket",
            "Connection: Upgrade",
            f"Sec-WebSocket-Key: {key}",
            "Sec-WebSocket-Version: 13",
            "",
            "",
        ]
        self.sock.sendall("\r\n".join(headers).encode("utf-8"))

        response = b""
        while b"\r\n\r\n" not in response:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise CDPConnectionError("Connection closed during WebSocket handshake")
            response += chunk

        # Chromium responds with 'HTTP/1.1 101 WebSocket Protocol Handshake' or 'HTTP/1.1 101 Switching Protocols'
        if not response.startswith(b"HTTP/1.1 101"):
            raise CDPConnectionError(f"CDP WebSocket handshake rejected: {response[:120]}")

    def send_command(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        event_handler: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Sends a JSON-RPC request to the browser and waits synchronously for the response.
        Incoming events encountered while waiting are dispatched to event_handler.
        """
        if self._is_closed or not self.sock:
            raise CDPConnectionError("Cannot send command: WebSocket is closed")

        cid = self._next_id
        self._next_id += 1
        payload = json.dumps({"id": cid, "method": method, "params": params or {}}).encode("utf-8")

        # RFC 6455 client-to-server text frame with masking
        frame = bytearray([0x81])
        length = len(payload)
        mask_key = os.urandom(4)
        if length <= 125:
            frame.append(0x80 | length)
        elif length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(struct.pack("!H", length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack("!Q", length))
        frame.extend(mask_key)
        frame.extend(b ^ mask_key[i % 4] for i, b in enumerate(payload))

        self.sock.sendall(frame)

        # Wait for matching response frame
        cmd_timeout = timeout or self.timeout
        old_timeout = self.sock.gettimeout()
        self.sock.settimeout(cmd_timeout)
        start_time = time.time()

        try:
            while True:
                if time.time() - start_time > cmd_timeout:
                    raise TimeoutError(f"CDP command '{method}' (id={cid}) timed out after {cmd_timeout}s")

                msg = self._recv_frame()
                if not msg:
                    continue

                try:
                    data = json.loads(msg)
                except Exception:
                    continue

                if "method" in data:
                    if event_handler:
                        event_handler(data["method"], data.get("params", {}))
                elif data.get("id") == cid:
                    if "error" in data:
                        err = data["error"]
                        raise CDPCommandError(
                            message=err.get("message", "Unknown CDP error"),
                            code=err.get("code", -1),
                            details=str(err.get("data", ""))
                        )
                    return data
        finally:
            if self.sock and not self._is_closed:
                self.sock.settimeout(old_timeout)

    def drain_events(self, timeout: float = 0.1, event_handler: Optional[Any] = None):
        """Drains non-blocking event frames currently buffered in the socket."""
        if self._is_closed or not self.sock:
            return
        old_timeout = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        try:
            while True:
                msg = self._recv_frame()
                if not msg:
                    break
                try:
                    data = json.loads(msg)
                    if "method" in data and event_handler:
                        event_handler(data["method"], data.get("params", {}))
                except Exception:
                    pass
        except (socket.timeout, TimeoutError):
            pass
        finally:
            if self.sock and not self._is_closed:
                self.sock.settimeout(old_timeout)

    def _recv_frame(self) -> str:
        fragments = bytearray()
        while True:
            header = self._recv_exact(2)
            if not header:
                return ""
            b1, b2 = header[0], header[1]
            fin = bool(b1 & 0x80)
            opcode = b1 & 0x0F
            if opcode == 0x8:  # Close frame
                self._is_closed = True
                return ""

            masked = bool(b2 & 0x80)
            length = b2 & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]

            if masked:
                mask_key = self._recv_exact(4)

            payload = self._recv_exact(length)
            if masked:
                payload = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))

            fragments.extend(payload)
            if fin:
                break

        return fragments.decode("utf-8", errors="ignore")

    def _recv_exact(self, num_bytes: int) -> bytes:
        buf = bytearray()
        while len(buf) < num_bytes:
            chunk = self.sock.recv(num_bytes - len(buf))
            if not chunk:
                break
            buf.extend(chunk)
        return bytes(buf)

    def close(self):
        self._is_closed = True
        if self.sock:
            try:
                # Send close frame
                mask_key = os.urandom(4)
                frame = bytearray([0x88, 0x80]) + mask_key
                self.sock.sendall(frame)
            except Exception:
                pass
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


class CDPBrowserDriver(BrowserDriverBase):
    """
    Framework-neutral Browser Driver implementing the approved Phase 9.7 Browser Bridge contract.
    Controls host Chromium binaries via CDP over lightweight, zero-dependency TCP sockets.
    """

    # Allowed navigation hosts to prevent unintended external internet requests
    ALLOWED_HOSTS = {"127.0.0.1", "localhost", "0.0.0.0"}

    def __init__(
        self,
        browser_info: Optional[BrowserInfo] = None,
        timeout: float = 15.0,
        temp_dir_prefix: str = "mds_browser_session_"
    ):
        self.browser_info = browser_info
        self.default_timeout = timeout
        self.temp_dir_prefix = temp_dir_prefix

        self.proc: Optional[subprocess.Popen] = None
        self.user_data_dir: Optional[str] = None
        self.port: Optional[int] = None
        self.target_ws_url: Optional[str] = None
        self.cdp_client: Optional[_CDPSocketClient] = None

        self._console_logs: List[ConsoleLogEntry] = []
        self._viewport: Optional[Viewport] = None
        self._active_url: str = ""
        self._is_launched = False

    @property
    def is_connected(self) -> bool:
        return (
            self._is_launched
            and self.proc is not None
            and self.proc.poll() is None
            and self.cdp_client is not None
            and not self.cdp_client._is_closed
        )

    def _on_cdp_event(self, method: str, params: Dict[str, Any]):
        """Internal callback for asynchronous browser events."""
        if method == "Runtime.consoleAPICalled":
            level = params.get("type", "log")
            args = params.get("args", [])
            text_parts = []
            for a in args:
                val = a.get("value")
                if val is not None:
                    text_parts.append(str(val))
                else:
                    text_parts.append(str(a.get("description", "")))
            msg = " ".join(text_parts)
            self._console_logs.append(
                ConsoleLogEntry(
                    level=level,
                    text=msg,
                    timestamp=time.time(),
                    url=self._active_url
                )
            )
        elif method == "Runtime.exceptionThrown":
            details = params.get("exceptionDetails", {})
            text = details.get("text", "Uncaught JavaScript Exception")
            if "exception" in details and "description" in details["exception"]:
                text += f": {details['exception']['description']}"
            self._console_logs.append(
                ConsoleLogEntry(
                    level="error",
                    text=text,
                    timestamp=time.time(),
                    url=self._active_url
                )
            )

    def launch(self, headless: bool = True, port: int = 0) -> None:
        """
        Launches the browser in headless mode with an ephemeral user-data-dir
        and connects via Chrome DevTools Protocol.
        """
        if self._is_launched:
            return

        # 1. Discover browser if not provided
        if not self.browser_info:
            preferred = BrowserDiscovery.get_preferred()
            if not preferred:
                raise BrowserNotFoundError(
                    "No Chromium-compatible browser binary found on host system."
                )
            self.browser_info = preferred

        executable = Path(self.browser_info.path)
        if not executable.exists():
            raise BrowserNotFoundError(f"Browser executable not found: {executable}")

        # 2. Allocate temporary isolated user-data-dir
        self.user_data_dir = tempfile.mkdtemp(prefix=self.temp_dir_prefix)

        # 3. Assemble secure, isolated Chrome flags
        cmd = [
            str(executable),
            "--headless=new" if headless else "--start-maximized",
            "--disable-gpu",
            "--no-sandbox",
            "--window-size=1440,900",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={self.user_data_dir}",
            "--disable-dev-shm-usage",
            "--disable-background-networking",
            "--disable-extensions",
            "--disable-sync",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-popup-blocking",
            "--enable-automation",
            "--hide-scrollbars",
            "about:blank",
        ]

        try:
            self.proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL
            )
        except Exception as e:
            self.close()
            raise BrowserLaunchError(f"Failed to spawn browser subprocess: {e}")

        # 4. Wait for DevToolsActivePort to be written by Chromium
        port_file = Path(self.user_data_dir) / "DevToolsActivePort"
        assigned_port = None
        start_wait = time.time()

        while time.time() - start_wait < 10.0:
            if self.proc.poll() is not None:
                err_out = ""
                if self.proc.stderr:
                    err_out = self.proc.stderr.read().decode("utf-8", errors="ignore")
                self.close()
                raise BrowserLaunchError(f"Browser process died prematurely: {err_out}")

            if port_file.exists():
                try:
                    with open(port_file, "r", encoding="utf-8") as fp:
                        lines = [l.strip() for l in fp.readlines() if l.strip()]
                    if lines:
                        assigned_port = int(lines[0])
                        break
                except Exception:
                    pass
            time.sleep(0.05)

        if not assigned_port:
            self.close()
            raise BrowserLaunchError("Timeout waiting for browser DevToolsActivePort file")

        self.port = assigned_port

        # 5. Connect to browser target page
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/list", timeout=5.0) as resp:
                targets = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            self.close()
            raise CDPConnectionError(f"Failed to query /json/list on port {self.port}: {e}")

        # Prefer 'page' type target
        page_target = None
        for t in targets:
            if t.get("type") == "page":
                page_target = t
                break
        if not page_target and targets:
            page_target = targets[0]

        if not page_target or "webSocketDebuggerUrl" not in page_target:
            self.close()
            raise CDPConnectionError("No valid page target found with webSocketDebuggerUrl")

        self.target_ws_url = page_target["webSocketDebuggerUrl"]

        # 6. Establish CDP WebSocket connection
        self.cdp_client = _CDPSocketClient(self.target_ws_url, timeout=self.default_timeout)

        # 7. Enable core domains
        self.cdp_client.send_command("Page.enable", event_handler=self._on_cdp_event)
        self.cdp_client.send_command("Runtime.enable", event_handler=self._on_cdp_event)
        self.cdp_client.send_command("DOM.enable", event_handler=self._on_cdp_event)

        # Mark launched and set default desktop viewport
        self._is_launched = True
        self.set_viewport(1440, 900)

    def navigate(self, url: str) -> None:
        """
        Navigates to the designated URL with safety enforcement and waits for document readiness.
        """
        if not self.is_connected or not self.cdp_client:
            raise BrowserBridgeError("Cannot navigate: Browser is not connected")

        # Security check: Restrict arbitrary external internet navigation
        if not url.startswith("about:") and not url.startswith("data:"):
            parsed = urllib.parse.urlparse(url)
            host = parsed.hostname
            if host not in self.ALLOWED_HOSTS:
                raise InvalidCommandError(
                    f"Navigation to non-local host '{host}' is prohibited by MDS safety policy."
                )

        self._active_url = url

        # Issue Page.navigate command
        res = self.cdp_client.send_command(
            "Page.navigate",
            {"url": url},
            event_handler=self._on_cdp_event
        )

        if "result" in res and res["result"].get("errorText"):
            raise NavigationError(f"Page navigation failed: {res['result']['errorText']}")

        # Wait for document.readyState === 'complete'
        start_wait = time.time()
        ready = False
        while time.time() - start_wait < self.default_timeout:
            try:
                state_res = self.evaluate("document.readyState")
                if state_res in ("interactive", "complete"):
                    ready = True
                    break
            except Exception:
                pass
            time.sleep(0.05)

        if not ready:
            raise NavigationError(f"Navigation timed out waiting for readyState on {url}")

        # Drain any console logs or lifecycle events emitted during load
        self.cdp_client.drain_events(timeout=0.1, event_handler=self._on_cdp_event)

    def set_viewport(self, width: int, height: int, device_scale_factor: float = 1.0) -> None:
        """Configures device emulation metrics."""
        if not self.is_connected or not self.cdp_client:
            raise BrowserBridgeError("Cannot set viewport: Browser is not connected")

        if width <= 0 or height <= 0:
            raise InvalidCommandError(f"Invalid viewport dimensions: {width}x{height}")

        self.cdp_client.send_command(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": device_scale_factor,
                "mobile": width <= 768,
            },
            event_handler=self._on_cdp_event
        )
        self._viewport = Viewport(
            width=width,
            height=height,
            device_scale_factor=device_scale_factor,
            is_mobile=(width <= 768)
        )

    def evaluate(self, script: str) -> Any:
        """
        Evaluates JavaScript expression in global page context and returns deserialized value.
        """
        if not self.is_connected or not self.cdp_client:
            raise BrowserBridgeError("Cannot evaluate script: Browser is not connected")

        res = self.cdp_client.send_command(
            "Runtime.evaluate",
            {
                "expression": script,
                "returnByValue": True,
                "awaitPromise": True,
            },
            event_handler=self._on_cdp_event
        )

        res_obj = res.get("result", {})
        if "exceptionDetails" in res_obj:
            details = res_obj["exceptionDetails"]
            text = details.get("text", "Evaluation exception")
            if "exception" in details and "description" in details["exception"]:
                text += f": {details['exception']['description']}"
            raise CDPCommandError(text)

        result_val = res_obj.get("result", {})
        return result_val.get("value")

    def wait_for(self, selector: str, timeout_ms: int = 5000) -> bool:
        """
        Polls DOM until an element matching selector exists in document.
        """
        start_time = time.time()
        timeout_sec = timeout_ms / 1000.0

        check_script = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            return el !== null;
        }})()
        """

        while time.time() - start_time < timeout_sec:
            try:
                found = self.evaluate(check_script)
                if found is True:
                    return True
            except Exception:
                pass
            time.sleep(0.05)

        raise TimeoutError(f"Timed out waiting for element '{selector}' after {timeout_ms}ms")

    def click(self, selector: str, timeout_ms: int = 5000) -> bool:
        """
        Locates element by selector, ensures visibility, and dispatches native click.
        """
        self.wait_for(selector, timeout_ms=timeout_ms)

        click_script = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (!el) return false;
            el.scrollIntoView({{ block: 'center', inline: 'center' }});
            el.focus();
            el.click();
            return true;
        }})()
        """
        res = self.evaluate(click_script)
        if not res:
            raise ElementNotFoundError(selector, timeout_ms=timeout_ms)

        # Allow microtasks and DOM updates to settle
        time.sleep(0.05)
        self.cdp_client.drain_events(timeout=0.05, event_handler=self._on_cdp_event)
        return True

    def type_text(self, selector: str, text: str, timeout_ms: int = 5000) -> bool:
        """
        Focuses element, updates value, and dispatches input/change DOM events.
        """
        self.wait_for(selector, timeout_ms=timeout_ms)

        type_script = f"""
        ((sel, val) => {{
            const el = document.querySelector(sel);
            if (!el) return false;
            el.scrollIntoView({{ block: 'center', inline: 'center' }});
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return true;
        }})({json.dumps(selector)}, {json.dumps(text)})
        """
        res = self.evaluate(type_script)
        if not res:
            raise ElementNotFoundError(selector, timeout_ms=timeout_ms)

        time.sleep(0.05)
        self.cdp_client.drain_events(timeout=0.05, event_handler=self._on_cdp_event)
        return True

    def screenshot(self, output_path: Optional[str] = None) -> bytes:
        """
        Captures a PNG screenshot via CDP Page.captureScreenshot.
        """
        if not self.is_connected or not self.cdp_client:
            raise BrowserBridgeError("Cannot capture screenshot: Browser is not connected")

        res = self.cdp_client.send_command(
            "Page.captureScreenshot",
            {"format": "png"},
            event_handler=self._on_cdp_event
        )

        b64_data = res.get("result", {}).get("data", "")
        if not b64_data:
            raise CDPCommandError("No image data returned from Page.captureScreenshot")

        raw_bytes = base64.b64decode(b64_data)

        if output_path:
            out_file = Path(output_path).resolve()
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(raw_bytes)

        return raw_bytes

    def get_console_logs(self) -> List[ConsoleLogEntry]:
        """Returns all console logs captured up to this point."""
        if self.cdp_client:
            self.cdp_client.drain_events(timeout=0.05, event_handler=self._on_cdp_event)
        return list(self._console_logs)

    def close(self) -> None:
        """Closes CDP connection, terminates subprocess, and cleans up temporary files."""
        if self.cdp_client:
            try:
                self.cdp_client.send_command("Browser.close", timeout=1.0)
            except Exception:
                pass
            self.cdp_client.close()
            self.cdp_client = None

        if self.proc:
            try:
                if self.proc.stdout:
                    self.proc.stdout.close()
                if self.proc.stderr:
                    self.proc.stderr.close()
            except Exception:
                pass
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2.0)
            except Exception:
                try:
                    self.proc.kill()
                    self.proc.wait(timeout=1.0)
                except Exception:
                    pass
            self.proc = None

        if self.user_data_dir and os.path.exists(self.user_data_dir):
            for _ in range(25):
                try:
                    shutil.rmtree(self.user_data_dir)
                    break
                except Exception:
                    time.sleep(0.08)
            self.user_data_dir = None

        self._is_launched = False

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
