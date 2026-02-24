#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".JPG", ".JPEG", ".PNG", ".WEBP", ".AVIF", ".GIF"}


def image_dimensions(path: Path) -> tuple[int, int]:
    proc = subprocess.run(
        ["/usr/bin/sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    width = 0
    height = 0
    for line in proc.stdout.splitlines():
        if "pixelWidth:" in line:
            width = int(line.split(":", 1)[1].strip())
        elif "pixelHeight:" in line:
            height = int(line.split(":", 1)[1].strip())
    return width, height


def limit_for(path: Path) -> tuple[int, int]:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("static/processed/project/"):
        return 2_300_000, 2600
    if rel.startswith("static/images/hero/"):
        return 4_000_000, 3800
    if rel.startswith("static/images/"):
        return 4_500_000, 4600
    return 4_500_000, 4600


def iter_images() -> list[Path]:
    files: list[Path] = []
    for base in (ROOT / "static" / "images", ROOT / "static" / "processed" / "project"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in IMAGE_EXTS:
                files.append(path)
    return sorted(files)


def main() -> int:
    if len(sys.argv) > 1:
        files: list[Path] = []
        for raw in sys.argv[1:]:
            path = ROOT / raw
            if not path.exists() or not path.is_file() or path.suffix not in IMAGE_EXTS:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel.startswith("static/images/") or rel.startswith("static/processed/project/"):
                files.append(path)
        targets = sorted(files)
    else:
        targets = iter_images()

    if not targets:
        print("Image policy check passed (no target images).")
        return 0

    violations: list[str] = []
    for path in targets:
        size_limit, max_dim = limit_for(path)
        size = path.stat().st_size
        width, height = image_dimensions(path)

        if size > size_limit:
            violations.append(
                f"{path.relative_to(ROOT)} size {size/1024/1024:.2f}MB exceeds {size_limit/1024/1024:.2f}MB"
            )
        if max(width, height) > max_dim:
            violations.append(
                f"{path.relative_to(ROOT)} dimensions {width}x{height} exceed max edge {max_dim}px"
            )

    if violations:
        print("Image policy check failed:")
        for item in violations:
            print(f"- {item}")
        return 1

    print("Image policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
