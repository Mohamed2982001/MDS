"""
MDS Token Runtime Engine — Token Validator
Phase 9.2: Token Runtime Engine

Validates DTCG schema compliance, inventory invariants, and empty-value guards.
"""

from pathlib import Path
from typing import Any, Dict, List, Set

from .models import SchemaValidationError, ThemeOverride, Token, ValidationResult


# Known valid W3C DTCG token types
VALID_DTCG_TYPES = {
    "color",
    "dimension",
    "shadow",
    "number",
    "duration",
    "cubicBezier",
    "fontFamily",
    "fontWeight",
}

EXPECTED_FILE_COUNT = 18
EXPECTED_BASE_TOKEN_COUNT = 185
EXPECTED_TOTAL_TOKEN_COUNT = 188
EXPECTED_COMPONENT_TOKEN_COUNT = 47
EXPECTED_THEMES = {
    "mode.dark",
    "mode.high-contrast",
    "preset.refined",
    "density.compact",
}


class TokenValidator:
    """Validates token schema, inventory invariants, and integrity rules."""

    def __init__(self, strict: bool = True):
        self.strict = strict

    def validate(
        self,
        base_tokens: Dict[str, Token],
        theme_overrides: Dict[str, ThemeOverride],
        all_tokens: Dict[str, Token],
        files: List[Path]
    ) -> ValidationResult:
        """
        Executes complete validation pass across loaded tokens.

        Returns:
            ValidationResult with error and warning lists.
        Raises:
            SchemaValidationError if strict mode is enabled and errors occur.
        """
        errors: List[str] = []
        warnings: List[str] = []

        # 1. File Inventory Invariant
        if len(files) != EXPECTED_FILE_COUNT:
            errors.append(
                f"File count mismatch: expected {EXPECTED_FILE_COUNT} files, found {len(files)}"
            )

        # 2. Total Token Count Invariant (188 distinct paths)
        if len(all_tokens) != EXPECTED_TOTAL_TOKEN_COUNT:
            errors.append(
                f"Total token count mismatch: expected {EXPECTED_TOTAL_TOKEN_COUNT} distinct tokens, "
                f"found {len(all_tokens)}"
            )

        # 3. Base Token Count Invariant (185 non-theme tokens)
        if len(base_tokens) != EXPECTED_BASE_TOKEN_COUNT:
            errors.append(
                f"Base token count mismatch: expected {EXPECTED_BASE_TOKEN_COUNT} tokens, "
                f"found {len(base_tokens)}"
            )

        # 4. Component Token Invariant (47 tokens under components/)
        component_tokens = [t for t in base_tokens.values() if t.layer == "component"]
        if len(component_tokens) != EXPECTED_COMPONENT_TOKEN_COUNT:
            errors.append(
                f"Component token count mismatch: expected {EXPECTED_COMPONENT_TOKEN_COUNT} tokens, "
                f"found {len(component_tokens)}"
            )

        # 5. Theme Files Invariant
        found_themes = set(theme_overrides.keys())
        missing_themes = EXPECTED_THEMES - found_themes
        if missing_themes:
            errors.append(f"Missing required theme override files: {sorted(missing_themes)}")

        # 6. DTCG Schema and Value Guards
        for path, token in all_tokens.items():
            # Value presence
            if token.raw_value is None or token.raw_value == "":
                errors.append(f"Token '{path}' in {token.file_path} has empty or null value")

            # Type validity
            if token.type not in VALID_DTCG_TYPES and token.type != "unknown":
                warnings.append(
                    f"Token '{path}' has non-standard type '{token.type}' (expected one of {sorted(VALID_DTCG_TYPES)})"
                )

            # Alias syntax check
            if isinstance(token.raw_value, str) and "{" in token.raw_value:
                if not (token.raw_value.startswith("{") and token.raw_value.endswith("}")):
                    errors.append(
                        f"Token '{path}' has malformed alias syntax '{token.raw_value}'. "
                        f"Aliases must be wrapped strictly as '{{path.to.token}}'"
                    )

        result = ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

        if self.strict and not result.is_valid:
            raise SchemaValidationError(
                f"Token validation failed with {len(errors)} error(s):\n" + "\n".join(f"- {e}" for e in errors)
            )

        return result
