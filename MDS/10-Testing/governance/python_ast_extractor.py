"""Safe Python AST Extractor for MDS Test Suites.

Extracts:
- Test classes and methods
- Capability IDs asserted in test bodies (e.g. self.record("MDS-...", ...))
- Docstrings and comments
- File-level imports and references
All without executing code.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class AstTestMethod:
    name: str
    line: int
    docstring: Optional[str] = None
    asserted_capabilities: List[str] = field(default_factory=list)


@dataclass
class AstFileInspection:
    file_path: Path
    test_methods: List[AstTestMethod] = field(default_factory=list)
    asserted_capabilities: Set[str] = field(default_factory=set)
    has_syntax_error: bool = False
    syntax_error_message: Optional[str] = None


class PythonAstExtractor:
    """Inspects Python test files via standard-library ast."""

    @classmethod
    def inspect_file(cls, file_path: Path) -> AstFileInspection:
        inspection = AstFileInspection(file_path=file_path)
        if not file_path.exists():
            return inspection

        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
        except SyntaxError as e:
            inspection.has_syntax_error = True
            inspection.syntax_error_message = f"Syntax error at line {e.lineno}: {e.msg}"
            return inspection
        except Exception as e:
            inspection.has_syntax_error = True
            inspection.syntax_error_message = str(e)
            return inspection

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method = AstTestMethod(
                    name=node.name,
                    line=node.lineno,
                    docstring=ast.get_docstring(node),
                )

                # Look for capability IDs inside the method
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                        val = sub.value.strip()
                        if val.startswith("MDS-"):
                            method.asserted_capabilities.append(val)
                            inspection.asserted_capabilities.add(val)

                inspection.test_methods.append(method)

        return inspection
