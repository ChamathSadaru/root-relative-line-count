from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def resolve_target(scan_root: str | Path, filename: str | Path) -> Path:
    """Resolve a target beneath scan_root, rejecting paths outside it."""
    root = Path(scan_root).resolve()
    target = Path(filename)

    if not target.is_absolute():
        target = root / target

    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("line-count target must be inside the scan root") from exc

    return target


def line_count(scan_root: str | Path, filename: str | Path) -> int:
    """Count lines in filename as resolved from scan_root."""
    target = resolve_target(scan_root, filename)
    if not target.is_file():
        return -1

    with target.open("r", encoding="utf-8") as source:
        return sum(1 for _ in source)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo_root_line_count",
        description="Count lines in a file relative to a scan root.",
    )
    parser.add_argument("scan_root", help="directory to scan")
    parser.add_argument("--lc", dest="filename", required=True, help="file to count")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(line_count(args.scan_root, args.filename))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
