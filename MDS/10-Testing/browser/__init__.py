#!/usr/bin/env python3
"""
MDS Browser Automation Runner Bridge
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Public interface for the framework-neutral browser automation bridge:
- BrowserDriverBase: Abstract driver contract
- CDPBrowserDriver: Chromium CDP implementation over standard TCP sockets
- BrowserDiscovery: Cross-platform Chromium detection (Chrome, Edge, Chromium)
- LocalTestServer: Ephemeral HTTP daemon with open CORS headers
- BrowserSession: High-level isolated test session coordinator
- Viewport, BrowserInfo, BrowserCapabilityResult: Value models
- Domain exceptions
"""

from .models import (
    BrowserType,
    BrowserInfo,
    Viewport,
    ConsoleLogLevel,
    ConsoleLogEntry,
    BrowserExecutionStatus,
    BrowserCapabilityResult,
)

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
    ServerStartupError,
)

from .driver_base import BrowserDriverBase
from .browser_discovery import BrowserDiscovery
from .local_server import LocalTestServer
from .cdp_driver import CDPBrowserDriver
from .session import BrowserSession

__all__ = [
    "BrowserType",
    "BrowserInfo",
    "Viewport",
    "ConsoleLogLevel",
    "ConsoleLogEntry",
    "BrowserExecutionStatus",
    "BrowserCapabilityResult",
    "BrowserBridgeError",
    "BrowserNotFoundError",
    "BrowserLaunchError",
    "CDPConnectionError",
    "CDPCommandError",
    "NavigationError",
    "TimeoutError",
    "ElementNotFoundError",
    "InvalidCommandError",
    "ServerStartupError",
    "BrowserDriverBase",
    "BrowserDiscovery",
    "LocalTestServer",
    "CDPBrowserDriver",
    "BrowserSession",
]
