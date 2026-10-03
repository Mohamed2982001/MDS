#!/usr/bin/env python3
"""
MDS Browser Automation Exceptions Hierarchy
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Defines domain-specific exceptions for deterministic browser bridge error handling.
"""


class BrowserBridgeError(Exception):
    """Base exception for all MDS browser automation bridge failures."""
    def __init__(self, message: str, capability_id: str = ""):
        super().__init__(message)
        self.message = message
        self.capability_id = capability_id


class BrowserNotFoundError(BrowserBridgeError):
    """Raised when no compatible Chromium browser binary can be discovered on the host system."""
    pass


class BrowserLaunchError(BrowserBridgeError):
    """Raised when the browser subprocess fails to spawn, dies prematurely, or fails initialization."""
    pass


class CDPConnectionError(BrowserBridgeError):
    """Raised when establishing or maintaining the Chrome DevTools Protocol WebSocket connection fails."""
    pass


class CDPCommandError(BrowserBridgeError):
    """Raised when a CDP command returns a JSON-RPC error response or evaluation exception."""
    def __init__(self, message: str, code: int = -1, details: str = "", capability_id: str = ""):
        super().__init__(message, capability_id)
        self.code = code
        self.details = details


class NavigationError(BrowserBridgeError):
    """Raised when navigating to a URL fails, returns an error status, or exceeds timeout."""
    pass


class TimeoutError(BrowserBridgeError):
    """Raised when an operation, wait_for, or event listener exceeds its allotted duration."""
    pass


class ElementNotFoundError(BrowserBridgeError):
    """Raised when a specified DOM selector cannot be matched within the active document."""
    def __init__(self, selector: str, timeout_ms: int = 0, capability_id: str = ""):
        msg = f"Element matching selector '{selector}' was not found within {timeout_ms}ms"
        super().__init__(msg, capability_id)
        self.selector = selector
        self.timeout_ms = timeout_ms


class InvalidCommandError(BrowserBridgeError):
    """Raised when an unrecognized command or invalid parameter is dispatched to the driver."""
    pass


class ServerStartupError(BrowserBridgeError):
    """Raised when the ephemeral local test HTTP server fails to bind or start."""
    pass
