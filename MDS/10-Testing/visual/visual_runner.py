#!/usr/bin/env python3
"""
MDS Visual Automation Runner & CDP Capture Engine
Phase 9.7.7: Visual Regression Engine & Snapshot Diffing
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Drives live headless Chromium via Chrome DevTools Protocol (CDP),
injects pinned local Cairo font artifacts, executes 7-step pre-capture
settlement (motion freeze, caret suppression, reflow settling), and
captures pixel-perfect raster snapshots.
"""

import base64
import time
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

try:
    from browser.cdp_driver import CDPBrowserDriver
    from browser.local_server import LocalTestServer
    from browser.models import BrowserInfo
    from browser.browser_discovery import BrowserDiscovery
except ImportError:
    from ..browser.cdp_driver import CDPBrowserDriver
    from ..browser.local_server import LocalTestServer
    from ..browser.models import BrowserInfo
    from ..browser.browser_discovery import BrowserDiscovery

from .visual_models import BaselineConfig, VisualExecutionStatus
from .baseline_manager import BaselineManager, FontArtifactUnavailableError


class VisualRunner:
    """
    Executes headless Chrome capture workflows against the locked MDS Reference Application.
    Guarantees deterministic, reproducible raster captures without CDN dependencies.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.baseline_manager = BaselineManager(workspace_root=self.workspace_root)
        self.preferred_browser: Optional[BrowserInfo] = BrowserDiscovery.get_preferred()
        self._cached_font_css: Optional[str] = None

    @property
    def is_browser_available(self) -> bool:
        return self.preferred_browser is not None and self.preferred_browser.is_available

    def _get_font_css(self) -> str:
        """
        Loads local Cairo font files, computes real SHA-256 hashes,
        and constructs an offline @font-face CSS block using base64 data URIs.
        """
        if self._cached_font_css:
            return self._cached_font_css

        is_valid, msg, font_info = self.baseline_manager.verify_fonts()
        if not is_valid:
            raise FontArtifactUnavailableError(msg)

        reg_path = Path(font_info["regular"]["path"])
        bold_path = Path(font_info["bold"]["path"])

        reg_b64 = base64.b64encode(reg_path.read_bytes()).decode("ascii")
        bold_b64 = base64.b64encode(bold_path.read_bytes()).decode("ascii")

        font_format = "truetype" if reg_path.suffix.lower() == ".ttf" else "woff2"

        css = f"""
        @font-face {{
            font-family: 'Cairo';
            font-style: normal;
            font-weight: 400;
            font-display: block;
            src: url('data:font/{font_format};base64,{reg_b64}') format('{font_format}');
        }}
        @font-face {{
            font-family: 'Cairo';
            font-style: normal;
            font-weight: 700;
            font-display: block;
            src: url('data:font/{font_format};base64,{bold_b64}') format('{font_format}');
        }}
        """
        self._cached_font_css = css
        return css

    def capture_baseline_snapshot(
        self,
        driver: CDPBrowserDriver,
        server: LocalTestServer,
        config: BaselineConfig
    ) -> bytes:
        """
        Executes the 7-step pre-capture settlement algorithm and returns PNG bytes.
        """
        # 1. Navigate to target SPA hash route
        target_url = server.get_url(f"MDS/Reference-Application/index.html{config.route}")
        driver.navigate(target_url)
        driver.wait_for("#ctrl-ref-role", timeout_ms=5000)

        # 2. Configure Viewport
        driver.set_viewport(width=config.width, height=config.height, device_scale_factor=1.0)

        # 3. Apply Theme, Density, and Direction attributes
        state_script = f"""
        (() => {{
            const root = document.documentElement;
            root.setAttribute('data-theme', '{config.theme}');
            root.setAttribute('data-density', '{config.density}');
            root.setAttribute('dir', '{config.direction}');
            if ('{config.route}'.startsWith('#/items/edit')) {{
                window.location.hash = '#/items/edit';
            }} else if ('{config.route}'.startsWith('#/items')) {{
                window.location.hash = '#/items';
            }} else {{
                window.location.hash = '#/overview';
            }}
            window.dispatchEvent(new HashChangeEvent('hashchange'));
        }})()
        """
        driver.evaluate(state_script)

        # 4. Inject Motion & Caret Suppression Styles
        suppress_script = """
        (() => {
            let style = document.getElementById('mds-visual-suppress');
            if (!style) {
                style = document.createElement('style');
                style.id = 'mds-visual-suppress';
                document.head.appendChild(style);
            }
            style.textContent = `
                *, *::before, *::after {
                    animation-duration: 0s !important;
                    animation-delay: 0s !important;
                    transition-duration: 0s !important;
                    transition-delay: 0s !important;
                    caret-color: transparent !important;
                }
                ::-webkit-scrollbar {
                    display: none !important;
                    width: 0 !important;
                    height: 0 !important;
                }
            `;
        })()
        """
        driver.evaluate(suppress_script)

        # 5. Inject Local Cairo Font Artifacts
        font_css = self._get_font_css()
        font_injection_script = f"""
        (() => {{
            let style = document.getElementById('mds-pinned-cairo-font');
            if (!style) {{
                style = document.createElement('style');
                style.id = 'mds-pinned-cairo-font';
                document.head.appendChild(style);
            }}
            style.textContent = `{font_css}`;
        }})()
        """
        driver.evaluate(font_injection_script)

        # 6. Await Font Settlement & Double RAF
        settle_script = """
        (async () => {
            if (document.fonts) {
                await document.fonts.ready;
            }
            await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
            return true;
        })()
        """
        driver.evaluate(settle_script)
        time.sleep(0.15)  # Allow subpixel reflow stabilization

        # 7. Execute CDP Page.captureScreenshot with exact clip
        clip_params = {
            "x": 0,
            "y": 0,
            "width": config.width,
            "height": config.height,
            "scale": 1.0
        }
        res = driver.cdp_client.send_command(
            "Page.captureScreenshot",
            {
                "format": "png",
                "clip": clip_params,
                "captureBeyondViewport": False,
                "fromSurface": True
            },
            event_handler=driver._on_cdp_event
        )

        b64_data = res.get("result", {}).get("data", "")
        if not b64_data:
            raise RuntimeError(f"CDP captureScreenshot returned empty payload for {config.baseline_id}")

        return base64.b64decode(b64_data)
