#!/usr/bin/env python3
"""
MDS Browser Automation Models
Phase 9.7.4: Browser Automation Runner Bridge
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Standardized data structures and value objects for the browser automation bridge:
- BrowserType & BrowserInfo
- Viewport & canonical responsive presets
- ConsoleLogEntry & logging levels
- BrowserCapabilityResult & execution statuses
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List


class BrowserType(str, Enum):
    CHROME = "chrome"
    EDGE = "edge"
    CHROMIUM = "chromium"
    UNKNOWN = "unknown"


@dataclass
class BrowserInfo:
    name: str
    path: Path
    version: str
    browser_type: BrowserType
    is_available: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": str(self.path),
            "version": self.version,
            "browser_type": self.browser_type.value,
            "is_available": self.is_available,
        }


@dataclass
class Viewport:
    width: int
    height: int
    device_scale_factor: float = 1.0
    is_mobile: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "device_scale_factor": self.device_scale_factor,
            "is_mobile": self.is_mobile,
        }

    # Canonical MDS Responsive Viewport Presets
    @classmethod
    def mobile_compact(cls) -> "Viewport":
        """Canonical Mobile Viewport (320px x 640px)"""
        return cls(width=320, height=640, device_scale_factor=2.0, is_mobile=True)

    @classmethod
    def tablet_portrait(cls) -> "Viewport":
        """Canonical Tablet Viewport (768px x 1024px)"""
        return cls(width=768, height=1024, device_scale_factor=1.0, is_mobile=False)

    @classmethod
    def desktop_standard(cls) -> "Viewport":
        """Canonical Standard Desktop Viewport (1024px x 768px)"""
        return cls(width=1024, height=768, device_scale_factor=1.0, is_mobile=False)

    @classmethod
    def desktop_wide(cls) -> "Viewport":
        """Canonical Wide Desktop Viewport (1440px x 900px)"""
        return cls(width=1440, height=900, device_scale_factor=1.0, is_mobile=False)


class ConsoleLogLevel(str, Enum):
    LOG = "log"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"


@dataclass
class ConsoleLogEntry:
    level: str
    text: str
    timestamp: float
    url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "text": self.text,
            "timestamp": self.timestamp,
            "url": self.url,
        }


class BrowserExecutionStatus(str, Enum):
    """
    Canonical Tri-State outcome for browser validation capabilities.
    Any execution failure or uncaught error is classified as FAIL with detailed
    exception_type and error_message metadata.
    """
    PASS = "PASS"
    FAIL = "FAIL"
    DEFERRED = "DEFERRED"


@dataclass
class BrowserCapabilityResult:
    """
    Structured outcome of an MDS browser validation capability.
    Enforces the canonical Tri-State status: PASS, FAIL, DEFERRED.
    Never fabricates PASS when execution was skipped or environment was missing.
    """
    capability_id: str
    status: BrowserExecutionStatus
    duration_ms: float = 0.0
    evidence: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    exception_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "status": self.status.value if isinstance(self.status, BrowserExecutionStatus) else str(self.status),
            "duration_ms": self.duration_ms,
            "evidence": self.evidence,
            "error_message": self.error_message,
            "exception_type": self.exception_type,
        }

    def __repr__(self) -> str:
        err = f" - Error: [{self.exception_type}] {self.error_message}" if self.error_message else ""
        return f"[{self.status.value}] {self.capability_id} ({self.duration_ms:.1f}ms){err}"
