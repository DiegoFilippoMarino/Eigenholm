"""Reject publication mistakes that Quarto can render without failing."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRECTORIES = ("about", "colophon", "notes", "posts", "projects", "replications")

EQUATION_LABEL = re.compile(r"\{#(eq-[A-Za-z0-9_-]+)\}")
EQUATION_REFERENCE = re.compile(r"(?<![\w-])@(eq-[A-Za-z0-9_-]+)")
MANUAL_TAG = re.compile(r"\\tag\s*\{")

# An executable cell and the `#| key: value` options directly beneath its fence.
PYTHON_CELL = re.compile(r"^```\{python\}\n((?:#\|[^\n]*\n)*)(.*?)^```", re.M | re.S)
CREATES_FIGURE = re.compile(r"plt\.(subplots|figure)\(")
VISIBILITY_OPTION = re.compile(r"^#\|\s*(code-fold|code-summary|echo)\s*:", re.M)

# House style lives in eigenholm.mplstyle. Repeating it inline is the noise the
# code policy exists to remove, so the validator rejects it rather than trusting
# the next article to remember.
STYLE_IN_STYLE_FILE = (
    (re.compile(r"spines\[\["), "axes.spines.top / axes.spines.right"),
    (re.compile(r"tight_layout\("), "figure.autolayout"),
    (re.compile(r"frameon\s*=\s*False"), "legend.frameon"),
)


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

        for cell in PYTHON_CELL.finditer(text):
            options, body = cell.group(1), cell.group(2)
            line = text.count("\n", 0, cell.start()) + 1

            if CREATES_FIGURE.search(body) and not VISIBILITY_OPTION.search(options):
                errors.append(
                    f"{relative}:{line}: this cell draws a figure but declares no "
                    "code-fold, code-summary, or echo; say whether a reader should "
                    "see the plotting code"
                )

            for pattern, replacement in STYLE_IN_STYLE_FILE:
                if pattern.search(body):
                    errors.append(
                        f"{relative}:{line}: figure styling belongs in "
                        f"eigenholm.mplstyle ({replacement}), not in the cell"
                    )

        if re.search(r"(?m)^draft:\s*true\s*$", text):
            errors.append(f"{relative}: published page is still marked draft")
        if "—" in text:
            errors.append(f"{relative}: em dash found in published copy")
        if re.search(r"(?i)placeholder|title here|replace (this|with)", text):
            errors.append(f"{relative}: placeholder copy found")

    freeze_root = ROOT / "_freeze"
    if freeze_root.exists():
        for frozen_result in sorted(freeze_root.rglob("html.json")):
            text = frozen_result.read_text(encoding="utf-8")
            if MANUAL_TAG.search(text):
                errors.append(
                    f"{frozen_result.relative_to(ROOT)}: frozen notebook output "
                    "contains a manual equation tag; refresh or remove the stale result"
                )

    if errors:
        print("Content validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(public_pages())} public Quarto pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
