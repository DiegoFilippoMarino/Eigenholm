"""Reject publication mistakes that Quarto can render without failing."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRECTORIES = ("about", "colophon", "notes", "posts", "projects")

EQUATION_LABEL = re.compile(r"\{#(eq-[A-Za-z0-9_-]+)\}")
EQUATION_REFERENCE = re.compile(r"(?<![\w-])@(eq-[A-Za-z0-9_-]+)")
MANUAL_TAG = re.compile(r"\\tag\s*\{")


def public_pages() -> list[Path]:
    pages: list[Path] = []
    for directory in PUBLIC_DIRECTORIES:
        for page in (ROOT / directory).rglob("*.qmd"):
            if not any(part.startswith("_") for part in page.relative_to(ROOT).parts):
                pages.append(page)
    return sorted(pages)


def main() -> int:
    errors: list[str] = []
    global_labels: dict[str, Path] = {}

    for page in public_pages():
        relative = page.relative_to(ROOT)
        text = page.read_text(encoding="utf-8")

        for match in MANUAL_TAG.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"{relative}:{line}: manual \\tag conflicts with Quarto numbering; "
                "use a {#eq-label} after the closing $$"
            )

        labels = EQUATION_LABEL.findall(text)
        for label in labels:
            if labels.count(label) > 1:
                errors.append(f"{relative}: duplicate equation label #{label}")
            if label in global_labels and global_labels[label] != page:
                errors.append(
                    f"{relative}: equation label #{label} is already defined in "
                    f"{global_labels[label].relative_to(ROOT)}"
                )
            global_labels[label] = page

        local_labels = set(labels)
        for reference in EQUATION_REFERENCE.findall(text):
            if reference not in local_labels:
                errors.append(f"{relative}: unresolved equation reference @{reference}")

        if re.search(r"(?m)^draft:\s*true\s*$", text):
            errors.append(f"{relative}: published page is still marked draft")
        if "—" in text:
            errors.append(f"{relative}: em dash found in published copy")
        if re.search(r"(?i)placeholder|title here|replace (this|with)", text):
            errors.append(f"{relative}: placeholder copy found")

    if errors:
        print("Content validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(public_pages())} public Quarto pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
