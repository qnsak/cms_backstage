from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LAYER_RULES = {
    "domain": ("cms.application", "cms.infrastructure", "cms.interfaces"),
    "application": ("cms.infrastructure", "cms.interfaces"),
}


def iter_python_files(base: Path) -> list[Path]:
    return [path for path in base.rglob("*.py") if path.is_file()]


def collect_imports(tree: ast.AST) -> list[str]:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            if node.level and node.module.startswith("."):
                continue
            imports.append(node.module)
    return imports


def check_layer(layer: str) -> list[str]:
    base = ROOT / layer
    forbidden = LAYER_RULES[layer]
    violations: list[str] = []
    for path in iter_python_files(base):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for module in collect_imports(tree):
            for rule in forbidden:
                if module.startswith(rule):
                    rel = path.relative_to(ROOT)
                    violations.append(f"{rel}: {module}")
    return violations


def main() -> int:
    errors: list[str] = []
    for layer in LAYER_RULES:
        errors.extend(check_layer(layer))

    if errors:
        print("Layer dependency violations found:")
        for error in errors:
            print(f"  - {error}")
        print("\nRule: domain/app cannot depend on infrastructure or interfaces.")
        return 1

    print("Layer dependency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
