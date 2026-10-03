#!/usr/bin/env python3
"""
MDS Repository Integrity Validator — Layer A Architecture Validation
Phase 9.7.3: Static Validation Suite & Scanners
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Validates Layer A architectural invariants:
- A-01: Canonical Directory Layout Guard (20 canonical layers & subdirectories).
- A-02: Clean Workspace Guard (Zero ad-hoc root scratch files or temp dumps).
- A-03: Intra-Repository Markdown Link Guard (Decodes percent-encoding, checks target existence).
- A-04: Zero NPM Dependency Guard (Zero node_modules or package.json in locked runtime areas).
"""

import os
import re
import sys
import urllib.parse
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

# Ensure UTF-8 stdout encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class RepoValidationResult:
    def __init__(self):
        self.checked_rules: List[str] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metrics: Dict[str, Any] = {}

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, rule_id: str, message: str):
        self.errors.append(f"[{rule_id}] {message}")

    def add_warning(self, rule_id: str, message: str):
        self.warnings.append(f"[{rule_id}] {message}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "metrics": self.metrics
        }


class RepoValidator:
    """
    Automated validator for repository structural integrity, layout,
    documentation linkages, and zero-npm dependency invariants.
    """

    CANONICAL_MDS_DIRS = [
        "00-Research",
        "01-Foundations",
        "02-Tokens",
        "03-Primitives",
        "04-Components",
        "05-Patterns",
        "06-Workflows",
        "07-Templates",
        "08-Experience-States",
        "09-Accessibility",
        "10-Responsive",
        "10-Testing",
        "11-AI",
        "12-Governance",
        "13-Implementation",
        "AGENT",
        "Documentation",
        "Playground",
        "Reference-Application",
        "Runtime"
    ]

    PROTECTED_RUNTIME_DIRS = [
        "MDS/Runtime",
        "MDS/Playground",
        "MDS/Reference-Application"
    ]

    BANNED_ARTIFACT_PATTERNS = [
        r"^temp_.*",
        r"^scratch_.*",
        r".*\.tmp$",
        r".*\.bak$",
        r".*\.orig$"
    ]

    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent.parent.parent
        self.mds_dir = self.workspace_root / "MDS"

    def validate_all(self) -> RepoValidationResult:
        """Executes all Layer A validation checks."""
        result = RepoValidationResult()
        self.validate_directory_layout(result)
        self.validate_clean_workspace(result)
        self.validate_zero_npm_dependencies(result)
        self.validate_markdown_links(result)
        return result

    def validate_directory_layout(self, result: RepoValidationResult):
        """A-01: Verifies all canonical MDS architectural directories exist."""
        result.checked_rules.append("A-01")
        if not self.mds_dir.exists():
            result.add_error("A-01", f"MDS root directory missing at {self.mds_dir}")
            return

        missing = []
        for d in self.CANONICAL_MDS_DIRS:
            target = self.mds_dir / d
            if not target.is_dir():
                missing.append(d)

        result.metrics["total_canonical_dirs"] = len(self.CANONICAL_MDS_DIRS)
        result.metrics["missing_canonical_dirs"] = missing

        if missing:
            result.add_error("A-01", f"Missing canonical architectural directories: {missing}")

    def validate_clean_workspace(self, result: RepoValidationResult):
        """A-02: Verifies zero stray scratch or temporary dump files exist in root/MDS."""
        result.checked_rules.append("A-02")
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.BANNED_ARTIFACT_PATTERNS]

        stray_files = []
        scan_roots = [self.workspace_root, self.mds_dir]
        for s_root in scan_roots:
            if not s_root.exists():
                continue
            for item in s_root.iterdir():
                if item.is_file():
                    for cp in compiled_patterns:
                        if cp.match(item.name):
                            stray_files.append(str(item.relative_to(self.workspace_root)))
                            break

        result.metrics["stray_files_found"] = stray_files
        if stray_files:
            result.add_error("A-02", f"Illegal temporary/scratch files found in workspace: {stray_files}")

    def validate_zero_npm_dependencies(self, result: RepoValidationResult):
        """A-04: Verifies zero npm/node artifacts exist in runtime and repository root."""
        result.checked_rules.append("A-04")
        banned_items = ["package.json", "package-lock.json", "node_modules"]

        violations = []
        # Check workspace root
        for b in banned_items:
            target = self.workspace_root / b
            if target.exists():
                violations.append(f"{self.workspace_root.name}/{b}")

        # Check protected runtime directories
        for rel_d in self.PROTECTED_RUNTIME_DIRS:
            target_dir = self.workspace_root / rel_d
            if target_dir.exists():
                for b in banned_items:
                    target = target_dir / b
                    if target.exists():
                        violations.append(f"{rel_d}/{b}")

        result.metrics["npm_violations"] = violations
        if violations:
            result.add_error("A-04", f"Illegal npm runtime dependencies found: {violations}")

    def validate_markdown_links(self, result: RepoValidationResult) -> Tuple[int, int]:
        """
        A-03: Scans Markdown documentation files in MDS and docs,
        unquotes URL percent-encoding, and verifies target file existence.
        """
        result.checked_rules.append("A-03")
        md_files = list(self.mds_dir.rglob("*.md"))
        docs_dir = self.workspace_root / "docs"
        if docs_dir.exists():
            md_files.extend(list(docs_dir.rglob("*.md")))

        checked_links = 0
        broken_links = []

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            for match in self.LINK_PATTERN.finditer(content):
                target = match.group(2).strip()
                # Skip external links and internal same-file anchors
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue

                # Strip anchor fragment
                target_clean = target.split("#")[0].strip()
                if not target_clean:
                    continue

                # Decode percent-encoding e.g. %20 -> space
                unquoted = urllib.parse.unquote(target_clean)

                if unquoted.startswith("file:///"):
                    clean_path = unquoted.replace("file:///", "")
                    # Normalize Windows drive slash e.g. /D:/ -> D:/
                    if re.match(r"^/[a-zA-Z]:", clean_path):
                        clean_path = clean_path[1:]
                    target_path = Path(clean_path)
                else:
                    target_path = (md_file.parent / unquoted).resolve()

                checked_links += 1
                if not target_path.exists():
                    rel_src = md_file.relative_to(self.workspace_root)
                    broken_links.append((str(rel_src), unquoted))

        result.metrics["markdown_files_scanned"] = len(md_files)
        result.metrics["intra_doc_links_checked"] = checked_links
        result.metrics["broken_links_count"] = len(broken_links)

        # In Phase 9.7.3, broken legacy doc links are logged as non-blocking advisories
        # (Severity MINOR / WARNING) under Section 5 Severity Matrix so doc debt is visible
        if broken_links:
            result.add_warning(
                "WARN-A03-DOC-LINKS",
                f"Found {len(broken_links)} unresolvable historical markdown links across docs/research (Advisory/Non-blocking under Section 5 Severity Matrix)."
            )
            result.metrics["broken_links_sample"] = [
                f"{src} -> {tgt}" for src, tgt in broken_links[:5]
            ]


        return checked_links, len(broken_links)


if __name__ == "__main__":
    validator = RepoValidator()
    print("=========================================================================")
    print("              MDS REPOSITORY INTEGRITY VALIDATOR (LAYER A)               ")
    print("=========================================================================")
    res = validator.validate_all()

    print(f"Canonical Directories:     {res.metrics.get('total_canonical_dirs')} checked")
    print(f"Stray Artifacts:           {len(res.metrics.get('stray_files_found', []))} found")
    print(f"NPM Artifacts in Runtime:  {len(res.metrics.get('npm_violations', []))} found")
    print(f"Markdown Files Scanned:    {res.metrics.get('markdown_files_scanned')} files")
    print(f"Intra-doc Links Checked:   {res.metrics.get('intra_doc_links_checked')} links")
    print(f"Unresolvable Links:        {res.metrics.get('broken_links_count')} links (advisory)")

    print("-------------------------------------------------------------------------")
    if res.is_valid:
        print("[PASS] Repository layout & zero-npm dependency invariants 100% VALID.")
        sys.exit(0)
    else:
        print(f"[FAIL] Found {len(res.errors)} repository integrity violations:")
        for err in res.errors:
            print(f"       └── {err}")
        sys.exit(1)
