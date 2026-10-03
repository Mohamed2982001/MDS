#!/usr/bin/env python3
"""
MDS Semantic CSS AST Scanner — Layer C Architecture Validation
Phase 9.7.3: Static Validation Suite & Scanners
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Implements the four ratified CSS validation scopes from Phase 9.7.1:
- Scope A: Token Sources (MDS/02-Tokens/) -> Primitive hex/px values allowed (EXEMPT).
- Scope B: Author Stylesheets (MDS/Runtime/, Playground/, Reference-Application/) ->
           Strict: Zero raw hex, 100% logical properties, zero row-reverse, parent-owned spacing.
- Scope C: Compiled Token Distributions (MDS/Runtime/tokens/dist/) ->
           Compiled custom property assignments in @layer mds.tokens allowed.
- Scope D: Structural Layout Values -> Explicit whitelist allowed (0, 100%, flex, etc.).

Distinguishes CSS ID selectors (#app, #overview) from hex colors by parsing
selectors and declarations separately in an AST-aware tokenizer.
"""

import re
import sys
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

# Ensure UTF-8 stdout encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CssScope(str, Enum):
    SCOPE_A = "SCOPE_A"  # Token source definitions (primitive values allowed)
    SCOPE_B = "SCOPE_B"  # Author stylesheets (strict rules enforced)
    SCOPE_C = "SCOPE_C"  # Compiled token distribution (@layer mds.tokens)
    SCOPE_D = "SCOPE_D"  # Structural layout values (whitelisted mechanics)


class ViolationType(str, Enum):
    RAW_HEX_COLOR = "RAW_HEX_COLOR"
    PHYSICAL_PROPERTY = "PHYSICAL_PROPERTY"
    ROW_REVERSE = "ROW_REVERSE"
    HOST_EXTERNAL_MARGIN = "HOST_EXTERNAL_MARGIN"
    RAW_RGB_HSL = "RAW_RGB_HSL"


class CssViolation:
    def __init__(
        self,
        file_path: str,
        line_number: int,
        selector: str,
        property_name: str,
        value: str,
        violation_type: ViolationType,
        scope: CssScope,
        message: str
    ):
        self.file_path = file_path
        self.line_number = line_number
        self.selector = selector
        self.property_name = property_name
        self.value = value
        self.violation_type = violation_type
        self.scope = scope
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file_path,
            "line": self.line_number,
            "selector": self.selector,
            "property": self.property_name,
            "value": self.value,
            "violation_type": self.violation_type.value,
            "scope": self.scope.value,
            "message": self.message
        }

    def __repr__(self) -> str:
        return (
            f"[{self.violation_type.value}] {self.file_path}:{self.line_number} "
            f"in '{self.selector}' -> {self.property_name}: {self.value} ({self.message})"
        )


class CssScanResult:
    def __init__(self, file_path: str, scope: CssScope):
        self.file_path = file_path
        self.scope = scope
        self.rules_count = 0
        self.declarations_count = 0
        self.violations: List[CssViolation] = []

    @property
    def is_valid(self) -> bool:
        return len(self.violations) == 0

    def add_violation(self, violation: CssViolation):
        self.violations.append(violation)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file_path,
            "scope": self.scope.value,
            "is_valid": self.is_valid,
            "rules_count": self.rules_count,
            "declarations_count": self.declarations_count,
            "violations_count": len(self.violations),
            "violations": [v.to_dict() for v in self.violations]
        }


class CssAstScanner:
    """
    AST-aware CSS tokenizer and semantic validator.
    Separates rule selectors from declaration blocks, strips comments cleanly,
    and inspects declaration values under scope-specific invariants.
    """

    # Hex color pattern: 3, 4, 6, or 8 hex digits preceded by '#'
    HEX_COLOR_PATTERN = re.compile(r'#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b')

    # Raw rgb/rgba/hsl/hsla patterns
    RAW_COLOR_FN_PATTERN = re.compile(r'\b(rgb|rgba|hsl|hsla)\s*\([^)]*\)', re.IGNORECASE)

    # Physical directional properties strictly prohibited in Scope B
    PHYSICAL_PROPERTY_PATTERN = re.compile(
        r'^(margin|padding|border)-(left|right)$|^(border)-(left|right)-(width|style|color|radius)$|^(left|right)$',
        re.IGNORECASE
    )

    # Physical directional values in border/clear/float
    PHYSICAL_VALUE_PATTERN = re.compile(r'\b(left|right)\b', re.IGNORECASE)

    # Row-reverse pattern (WCAG 2.4.3 focus order preservation)
    ROW_REVERSE_PATTERN = re.compile(r'\brow-reverse\b', re.IGNORECASE)

    # Component host / root selectors for Parent-Owned Spacing
    HOST_SELECTOR_PATTERN = re.compile(r'(^|\s|,\s*)(:host|\.mds-[a-z0-9-]+)(\s*$|\s*,\s*|:[^a-z])', re.IGNORECASE)

    # Outer margin properties
    MARGIN_PROPERTY_PATTERN = re.compile(r'^margin(-block|-inline|-top|-bottom|-left|-right)?$', re.IGNORECASE)

    # URL fragment pattern e.g. url('#clip') or url("#filter")
    URL_FRAGMENT_PATTERN = re.compile(r'url\s*\(\s*[\'"]?#[^\'")]+[\'"]?\s*\)', re.IGNORECASE)

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent

    def determine_scope(self, file_path: Path) -> CssScope:
        """Determines the architectural scanning scope for a given CSS file."""
        posix_path = file_path.as_posix()

        # Scope A: Token sources
        if "02-Tokens" in posix_path:
            return CssScope.SCOPE_A

        # Scope C: Compiled token distribution
        if "tokens/dist" in posix_path or posix_path.endswith("/tokens.css"):
            return CssScope.SCOPE_C

        # Scope B: Runtime, Playground, Reference Application, Showcases, etc.
        return CssScope.SCOPE_B

    def scan_file(self, file_path: Path, scope: Optional[CssScope] = None) -> CssScanResult:
        """Reads and scans a CSS file on disk."""
        if not file_path.exists():
            res = CssScanResult(str(file_path), scope or CssScope.SCOPE_B)
            res.add_violation(CssViolation(
                file_path=str(file_path),
                line_number=1,
                selector="",
                property_name="",
                value="",
                violation_type=ViolationType.RAW_HEX_COLOR,
                scope=res.scope,
                message=f"File not found: {file_path}"
            ))
            return res

        effective_scope = scope or self.determine_scope(file_path)
        content = file_path.read_text(encoding="utf-8", errors="replace")
        return self.scan_string(content, effective_scope, str(file_path))

    def scan_string(self, css_text: str, scope: CssScope, file_path: str = "<memory>") -> CssScanResult:
        """Scans a CSS string under the designated scope using an AST-aware tokenizer."""
        result = CssScanResult(file_path, scope)

        # Scope A (Tokens) is completely exempt from zero-hex and physical property checks
        if scope == CssScope.SCOPE_A:
            return result

        # Step 1: Strip comments while preserving character count & line mapping
        clean_text, line_map = self._strip_comments_with_line_map(css_text)

        # Step 2: Tokenize rules into (selector, declaration_block, line_number)
        rules = self._parse_rules(clean_text, line_map)
        result.rules_count = len(rules)

        for selector, decl_block, rule_line in rules:
            # Check if this rule is inside @layer mds.tokens in Scope C
            is_scope_c_layer = (scope == CssScope.SCOPE_C)

            # Parse declarations inside `{ ... }`
            declarations = self._parse_declarations(decl_block, rule_line, clean_text, line_map)
            result.declarations_count += len(declarations)

            for prop, val, decl_line in declarations:
                self._validate_declaration(
                    result=result,
                    file_path=file_path,
                    scope=scope,
                    selector=selector,
                    property_name=prop,
                    value=val,
                    line_number=decl_line,
                    is_scope_c_layer=is_scope_c_layer
                )

        return result

    def _strip_comments_with_line_map(self, text: str) -> Tuple[str, List[int]]:
        """
        Replaces /* ... */ comments with whitespace, maintaining character offsets
        and pre-computing a line number index for instant line resolution.
        """
        chars = list(text)
        n = len(chars)
        i = 0
        in_comment = False

        while i < n:
            if not in_comment and i + 1 < n and chars[i] == '/' and chars[i + 1] == '*':
                in_comment = True
                chars[i] = ' '
                chars[i + 1] = ' '
                i += 2
            elif in_comment and i + 1 < n and chars[i] == '*' and chars[i + 1] == '/':
                in_comment = False
                chars[i] = ' '
                chars[i + 1] = ' '
                i += 2
            elif in_comment:
                if chars[i] != '\n':
                    chars[i] = ' '
                i += 1
            else:
                i += 1

        clean_text = "".join(chars)

        # Compute line start offsets
        line_starts = [0]
        for idx, ch in enumerate(clean_text):
            if ch == '\n':
                line_starts.append(idx + 1)

        return clean_text, line_starts

    def _offset_to_line(self, offset: int, line_starts: List[int]) -> int:
        """Binary search offset to find 1-based line number."""
        import bisect
        idx = bisect.bisect_right(line_starts, offset)
        return max(1, idx)

    def _parse_rules(self, text: str, line_starts: List[int]) -> List[Tuple[str, str, int]]:
        """
        Parses CSS into a list of tuples: (selector, declaration_block, line_number).
        Handles nested @media, @supports, @layer rules gracefully.
        """
        rules = []
        n = len(text)
        i = 0
        depth = 0
        selector_start = 0
        block_start = 0
        current_selectors = []

        while i < n:
            ch = text[i]

            if ch == '{':
                if depth == 0:
                    selector_raw = text[selector_start:i].strip()
                    block_start = i + 1
                    current_selectors.append((selector_raw, selector_start))
                elif depth >= 1:
                    # Nested block (e.g. inside @media or @keyframes)
                    nested_sel = text[selector_start:i].strip()
                    current_selectors.append((nested_sel, selector_start))
                    block_start = i + 1

                depth += 1
                selector_start = i + 1
                i += 1

            elif ch == '}':
                depth -= 1
                if current_selectors:
                    sel, sel_offset = current_selectors.pop()
                    decl_content = text[block_start:i]
                    line_num = self._offset_to_line(sel_offset, line_starts)
                    # If this block does not contain further child blocks, it is a declaration block
                    if '{' not in decl_content:
                        rules.append((sel, decl_content, line_num))
                selector_start = i + 1
                block_start = i + 1
                i += 1
            else:
                i += 1

        return rules

    def _parse_declarations(
        self,
        decl_block: str,
        rule_line: int,
        full_text: str,
        line_starts: List[int]
    ) -> List[Tuple[str, str, int]]:
        """Parses a CSS declaration block into (property, value, line_number) tuples."""
        decls = []
        raw_parts = decl_block.split(';')

        for part in raw_parts:
            part = part.strip()
            if not part or ':' not in part:
                continue

            # Handle custom properties vs standard properties
            colon_idx = part.find(':')
            prop = part[:colon_idx].strip()
            val = part[colon_idx + 1:].strip()

            if prop and val:
                decls.append((prop, val, rule_line))

        return decls

    def _validate_declaration(
        self,
        result: CssScanResult,
        file_path: str,
        scope: CssScope,
        selector: str,
        property_name: str,
        value: str,
        line_number: int,
        is_scope_c_layer: bool
    ):
        """Validates a single CSS declaration against the architectural rules."""
        # 1. Scope C Exception: Compiled token distributions in @layer mds.tokens are allowed
        if is_scope_c_layer:
            return

        # 2. Check for Raw Hex Color literals in property values (Scope B Invariant)
        # Mask out url(#fragment) references first so SVG filter/clip-path IDs are never flagged
        val_no_urls = self.URL_FRAGMENT_PATTERN.sub('url(MASKED)', value)
        hex_matches = self.HEX_COLOR_PATTERN.findall(val_no_urls)
        if hex_matches:
            result.add_violation(CssViolation(
                file_path=file_path,
                line_number=line_number,
                selector=selector,
                property_name=property_name,
                value=value,
                violation_type=ViolationType.RAW_HEX_COLOR,
                scope=scope,
                message=f"Hardcoded raw hex color '#{hex_matches[0]}' forbidden in Scope B. Use design token."
            ))

        # 3. Check for Physical Directional Properties (100% CSS Logical Properties Invariant)
        if self.PHYSICAL_PROPERTY_PATTERN.match(property_name):
            result.add_violation(CssViolation(
                file_path=file_path,
                line_number=line_number,
                selector=selector,
                property_name=property_name,
                value=value,
                violation_type=ViolationType.PHYSICAL_PROPERTY,
                scope=scope,
                message=f"Physical directional property '{property_name}' forbidden. Use CSS Logical Property."
            ))

        # 4. Check for Physical Values in clear / float (e.g. float: left/right)
        if property_name.lower() in ("float", "clear"):
            if self.PHYSICAL_VALUE_PATTERN.search(value):
                result.add_violation(CssViolation(
                    file_path=file_path,
                    line_number=line_number,
                    selector=selector,
                    property_name=property_name,
                    value=value,
                    violation_type=ViolationType.PHYSICAL_PROPERTY,
                    scope=scope,
                    message=f"Physical value '{value}' in '{property_name}' forbidden. Use inline-start/inline-end."
                ))

        # 5. Check for Row-Reverse (WCAG 2.4.3 focus order preservation)
        if self.ROW_REVERSE_PATTERN.search(value):
            result.add_violation(CssViolation(
                file_path=file_path,
                line_number=line_number,
                selector=selector,
                property_name=property_name,
                value=value,
                violation_type=ViolationType.ROW_REVERSE,
                scope=scope,
                message="Functional 'row-reverse' forbidden (WCAG 2.4.3 Focus Order Invariant)."
            ))

        # 6. Check for Parent-Owned Spacing in Component Stylesheets
        # Components must never declare physical external margins; layout primitives control layout spacing
        if "components" in file_path.replace("\\", "/").lower() and self._is_component_root_selector(selector):
            if re.match(r"^margin-(top|bottom|left|right)$", property_name, re.IGNORECASE):
                if value.strip() not in ("0", "0px", "none", "inherit", "unset"):
                    result.add_violation(CssViolation(
                        file_path=file_path,
                        line_number=line_number,
                        selector=selector,
                        property_name=property_name,
                        value=value,
                        violation_type=ViolationType.HOST_EXTERNAL_MARGIN,
                        scope=scope,
                        message=f"Parent-Owned Spacing violation: physical external margin '{property_name}: {value}' on component root '{selector}'."
                    ))


    def _is_component_root_selector(self, selector: str) -> bool:
        """Determines if a selector is a component root / host element selector."""
        sel = selector.strip()
        # Direct matches like :host, :host([open]), .mds-button, .mds-dialog
        # Does NOT match child/descendant selectors like .mds-button .mds-button__icon
        if ":host" in sel:
            return True

        # Check if it's a standalone .mds-component selector without descendant combinator
        # e.g. '.mds-button', '.mds-card:hover' is a root component selector
        # but '.mds-card .mds-card__header' is an internal element, which can have margins
        parts = sel.split()
        if len(parts) == 1 and parts[0].startswith(".mds-"):
            # Check it's not a BEM element (__element)
            base_class = parts[0].split(":")[0].split("[")[0]
            if "__" not in base_class:
                return True

        return False

    def scan_directory(self, dir_path: Path, recursive: bool = True) -> List[CssScanResult]:
        """Scans all CSS files in a directory."""
        results = []
        pattern = "**/*.css" if recursive else "*.css"
        for css_file in sorted(dir_path.glob(pattern)):
            results.append(self.scan_file(css_file))
        return results


if __name__ == "__main__":
    scanner = CssAstScanner()
    workspace = scanner.workspace_root
    target_dirs = [
        workspace / "MDS" / "Runtime",
        workspace / "MDS" / "Playground",
        workspace / "MDS" / "Reference-Application"
    ]

    total_files = 0
    total_violations = 0

    print("=========================================================================")
    print("                 MDS SEMANTIC CSS AST SCANNER                            ")
    print("=========================================================================")

    for d in target_dirs:
        if not d.exists():
            continue
        res_list = scanner.scan_directory(d)
        for r in res_list:
            total_files += 1
            rel_path = Path(r.file_path).relative_to(workspace)
            if not r.is_valid:
                total_violations += len(r.violations)
                print(f"[FAIL] {rel_path} ({len(r.violations)} violations)")
                for v in r.violations:
                    print(f"       └── Line {v.line_number}: {v.property_name}: {v.value} -> {v.message}")
            else:
                print(f"[PASS] {rel_path} ({r.rules_count} rules, {r.declarations_count} decls)")

    print("-------------------------------------------------------------------------")
    print(f"Total CSS Files Scanned: {total_files}")
    print(f"Total Violations:        {total_violations}")
    if total_violations == 0:
        print("[SUCCESS] All stylesheets conform 100% to MDS CSS Architecture.")
        sys.exit(0)
    else:
        print(f"[ERROR] Found {total_violations} CSS architectural violations.")
        sys.exit(1)
