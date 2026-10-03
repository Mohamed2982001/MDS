"""
MDS Token Runtime Engine — Token Loader
Phase 9.2: Token Runtime Engine

Recursively discovers and parses all W3C DTCG token JSON files from MDS/02-Tokens/.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from .models import ThemeOverride, Token


# Standard selector mappings for multi-dimensional theme axes
THEME_SELECTOR_MAP = {
    "mode.dark.tokens.json": {
        "theme_id": "mode.dark",
        "selector": '[data-mode="dark"]',
    },
    "mode.high-contrast.tokens.json": {
        "theme_id": "mode.high-contrast",
        "selector": '[data-mode="high-contrast"]',
    },
    "preset.refined.tokens.json": {
        "theme_id": "preset.refined",
        "selector": '[data-preset="refined"]',
    },
    "density.compact.tokens.json": {
        "theme_id": "density.compact",
        "selector": '[data-density="compact"]',
    },
}


class TokenLoader:
    """Discovers and parses DTCG token files into structured Token objects."""

    def __init__(self, tokens_dir: Path):
        self.tokens_dir = Path(tokens_dir).resolve()
        if not self.tokens_dir.exists():
            raise FileNotFoundError(f"Tokens directory does not exist: {self.tokens_dir}")

    def discover_files(self) -> List[Path]:
        """Finds all *.tokens.json files sorted deterministically by relative path."""
        files = sorted(
            list(self.tokens_dir.rglob("*.tokens.json")),
            key=lambda p: str(p.relative_to(self.tokens_dir)).replace("\\", "/")
        )
        return files

    def _determine_tier(self, file_path: Path) -> str:
        """Determines the architectural tier of a token file based on directory structure."""
        rel_parts = file_path.relative_to(self.tokens_dir).parts
        if "primitives" in rel_parts:
            return "primitive"
        elif "semantic" in rel_parts:
            return "semantic"
        elif "components" in rel_parts:
            return "component"
        elif "themes" in rel_parts:
            return "theme"
        return "primitive"

    def _flatten_tokens(
        self,
        data: Dict[str, Any],
        tier: str,
        file_path: Path,
        prefix: str = "",
        inherited_type: str = ""
    ) -> Dict[str, Token]:
        """Recursively traverses a DTCG dictionary and extracts flattened Token instances."""
        tokens: Dict[str, Token] = {}
        
        # Check if current group declares an inherited $type
        current_type = data.get("$type", inherited_type)

        for key, value in data.items():
            if key.startswith("$"):
                continue  # Skip DTCG metadata at group level ($schema, $description, $extensions)
            
            curr_path = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                if "$value" in value:
                    token_type = value.get("$type") or current_type or "unknown"
                    desc = value.get("$description", "")
                    extensions = value.get("$extensions", {})
                    
                    # Layer override from extensions if explicitly provided
                    layer = extensions.get("mds", {}).get("layer", tier)

                    tokens[curr_path] = Token(
                        path=curr_path,
                        raw_value=value["$value"],
                        type=token_type,
                        description=desc,
                        layer=layer,
                        file_path=file_path,
                        extensions=extensions
                    )
                
                # Recurse for nested tokens or sub-groups
                sub_tokens = self._flatten_tokens(
                    value,
                    tier=tier,
                    file_path=file_path,
                    prefix=curr_path,
                    inherited_type=current_type
                )
                tokens.update(sub_tokens)

        return tokens

    def load(self) -> Tuple[Dict[str, Token], Dict[str, ThemeOverride], Dict[str, Token], List[Path]]:
        """
        Loads all tokens from the repository.

        Returns:
            Tuple of:
            - base_tokens: Dict[token_path, Token] (non-theme base tokens)
            - theme_overrides: Dict[theme_id, ThemeOverride] (theme override sets)
            - all_tokens: Dict[token_path, Token] (union of base tokens + theme-specific tokens)
            - files: List[Path] of discovered token files
        """
        files = self.discover_files()
        base_tokens: Dict[str, Token] = {}
        theme_overrides: Dict[str, ThemeOverride] = {}
        all_tokens: Dict[str, Token] = {}

        for file_path in files:
            tier = self._determine_tier(file_path)
            with open(file_path, "r", encoding="utf-8") as fp:
                data = json.load(fp)

            if tier == "theme":
                theme_info = THEME_SELECTOR_MAP.get(file_path.name, {
                    "theme_id": file_path.stem.replace(".tokens", ""),
                    "selector": f'[data-theme="{file_path.stem.replace(".tokens", "")}"]',
                })
                theme_id = theme_info["theme_id"]
                selector = theme_info["selector"]
                desc = data.get("$description", f"Theme overrides for {theme_id}")

                tokens = self._flatten_tokens(data, tier="theme", file_path=file_path)
                theme_override = ThemeOverride(
                    theme_id=theme_id,
                    selector=selector,
                    file_path=file_path,
                    description=desc,
                    tokens=tokens
                )
                theme_overrides[theme_id] = theme_override
                
                # Also register into all_tokens for global symbol resolution
                for p, t in tokens.items():
                    if p not in all_tokens:
                        all_tokens[p] = t
            else:
                tokens = self._flatten_tokens(data, tier=tier, file_path=file_path)
                base_tokens.update(tokens)
                all_tokens.update(tokens)

        return base_tokens, theme_overrides, all_tokens, files
