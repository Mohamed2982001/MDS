#!/usr/bin/env python3
"""
MDS Browser Driver Base Abstraction
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Defines the abstract interface for all MDS browser drivers, ensuring framework-neutral
automation decoupling and complete isolation from runtime code.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Any
from pathlib import Path

from .models import ConsoleLogEntry, Viewport


class BrowserDriverBase(ABC):
    """
    Abstract interface for browser automation drivers in MDS.
    Any compliant driver (CDP, WebDriver, etc.) must implement this contract.
    """

    @abstractmethod
    def launch(self, headless: bool = True, port: int = 0) -> None:
        """
        Launches the browser process in the requested mode (headless by default).
        If port=0, an ephemeral dynamic port must be assigned by the operating system.
        """
        pass

    @abstractmethod
    def navigate(self, url: str) -> None:
        """
        Navigates the active page to the designated URL and waits for DOM readiness.
        """
        pass

    @abstractmethod
    def set_viewport(self, width: int, height: int, device_scale_factor: float = 1.0) -> None:
        """
        Resizes the browser viewport and sets device pixel ratio.
        """
        pass

    @abstractmethod
    def click(self, selector: str, timeout_ms: int = 5000) -> bool:
        """
        Locates the element matching selector, scrolls it into view, and executes a click event.
        Returns True on success, or raises ElementNotFoundError / TimeoutError.
        """
        pass

    @abstractmethod
    def type_text(self, selector: str, text: str, timeout_ms: int = 5000) -> bool:
        """
        Locates the input/textarea matching selector, focuses it, and inputs the specified text.
        Returns True on success, or raises ElementNotFoundError / TimeoutError.
        """
        pass

    @abstractmethod
    def wait_for(self, selector: str, timeout_ms: int = 5000) -> bool:
        """
        Polls the DOM until an element matching selector is present and attached.
        Returns True on success, or raises TimeoutError.
        """
        pass

    @abstractmethod
    def screenshot(self, output_path: Optional[str] = None) -> bytes:
        """
        Captures a PNG screenshot of the current page viewport.
        If output_path is provided, writes the image to disk. Returns raw PNG bytes.
        """
        pass

    @abstractmethod
    def evaluate(self, script: str) -> Any:
        """
        Executes JavaScript in the global page context and returns the serialized result.
        """
        pass

    @abstractmethod
    def get_console_logs(self) -> List[ConsoleLogEntry]:
        """
        Returns all console log messages, warnings, and errors captured during the session.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closes the active page, terminates the browser process, and purges all temporary resources.
        """
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Returns True if the browser process is alive and CDP communication is active.
        """
        pass

    # Context Manager Support
    def __enter__(self) -> "BrowserDriverBase":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
