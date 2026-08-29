#!/usr/bin/env python3
"""Render the blog source tree into the portfolio handoff directory."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

FALLBACK_MARKERS = (
    b'class="TypMark-math-inline--error',
    b'class="TypMark-math-block--error',
    b'<figure class="TypMark-typst-block TypMark-typst-error',
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("site"))
    parser.add_argument("--typmark", type=Path, default=Path("typmark-cli"))
    return parser.parse_args()


def render_site(root: Path, output: Path, typmark: Path) -> int:
    root = root.resolve()
    raw_output = Path(
        os.path.abspath(root / output if not output.is_absolute() else output)
    )
    try:
        relative_output = raw_output.relative_to(root)
    except ValueError as error:
        raise SystemExit(
            f"Output must be below the source root: {raw_output}"
        ) from error
    if not relative_output.parts:
        raise SystemExit(f"Output must be below the source root: {raw_output}")

    current = root
    for part in relative_output.parts:
        current /= part
        if current.is_symlink():
            raise SystemExit(f"Output path must not contain a symlink: {current}")

    output = raw_output.resolve()
    typmark = (
        (root / typmark).resolve() if not typmark.is_absolute() else typmark.resolve()
    )
    if not typmark.is_file():
        raise SystemExit(f"TypMark executable not found: {typmark}")

    try:
        if output.exists():
            shutil.rmtree(output)
    except OSError as error:
        raise SystemExit(
            f"Unable to clear output directory {output}: {error}"
        ) from error

    content_dir = output / "blogs-content"
    assets_dir = output / "blogs" / "assets"
    content_dir.mkdir(parents=True)
    assets_dir.mkdir(parents=True)

    def is_ignored(path: Path) -> bool:
        return any(part in {".git", ".github", output.name} for part in path.parts)

    info_paths = sorted(
        path for path in root.rglob("info.json") if not is_ignored(path)
    )
    if not info_paths:
        raise SystemExit("No info.json found")

    index: dict[str, dict[str, dict[str, object]]] = {"folders": {}}
    folder_keys: list[str] = []
    rendered_count = 0

    for info_path in info_paths:
        folder = info_path.parent
        rel_folder = folder.relative_to(root)
        folder_key = "" if rel_folder == Path(".") else rel_folder.as_posix()
        folder_keys.append(folder_key)

        try:
            info = json.loads(info_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise SystemExit(f"Unable to read {info_path}: {error}") from error
        if not isinstance(info, dict):
            raise SystemExit(f"Invalid info.json object: {info_path}")
        display = info.get("display") or (folder_key or "Blog")
        if not isinstance(display, str):
            raise SystemExit(f"Invalid display value in {info_path}")
        folder_description = info.get("description")
        articles = info.get("articles")
        if not isinstance(articles, dict):
            raise SystemExit(f"Invalid info.json: {info_path}")

        pages: list[dict[str, str]] = []
        for slug, meta in articles.items():
            if not isinstance(slug, str) or not slug:
                raise SystemExit(f"Invalid article key in {info_path}")

            title = meta.get("title") if isinstance(meta, dict) else None
            description = meta.get("description") if isinstance(meta, dict) else None
            if title is not None and not isinstance(title, str):
                raise SystemExit(f"Invalid title for {slug} in {info_path}")
            tmd_path = folder / f"{slug}.tmd"
            if not tmd_path.is_file():
                raise SystemExit(f"Missing tmd file: {tmd_path}")

            out_rel = f"{folder_key}/{slug}" if folder_key else slug
            out_path = content_dir / f"{out_rel}.html"
            out_path.parent.mkdir(parents=True, exist_ok=True)

            rendered = subprocess.run(
                [
                    str(typmark),
                    "--render",
                    "--theme",
                    "dark",
                    "--diagnostics",
                    "pretty",
                    str(tmd_path),
                ],
                capture_output=True,
                check=False,
                env=os.environ,
            )
            if rendered.returncode != 0 or rendered.stderr:
                raise SystemExit(
                    f"TypMark failed for {tmd_path}:\n"
                    + rendered.stderr.decode("utf-8", errors="replace")
                )
            if any(marker in rendered.stdout for marker in FALLBACK_MARKERS):
                raise SystemExit(f"TypMark fallback in {tmd_path}")

            out_path.write_bytes(rendered.stdout)
            page = {"slug": slug, "title": title or slug, "path": out_rel}
            if isinstance(description, str) and description.strip():
                page["description"] = description.strip()
            pages.append(page)
            rendered_count += 1

        folder_entry: dict[str, object] = {
            "display": display,
            "pages": pages,
            "folders": [],
        }
        if isinstance(folder_description, str) and folder_description.strip():
            folder_entry["description"] = folder_description.strip()
        index["folders"][folder_key] = folder_entry

    folder_keys = sorted(set(folder_keys))
    for folder_key in folder_keys:
        prefix = f"{folder_key}/" if folder_key else ""
        children: list[dict[str, str]] = []
        for child in folder_keys:
            if child == folder_key or not child.startswith(prefix):
                continue
            rest = child[len(prefix) :]
            if "/" in rest:
                continue
            child_info = index["folders"].get(child, {})
            display = child_info.get("display") or rest
            entry = {"name": rest, "path": child, "display": str(display)}
            description = child_info.get("description")
            if isinstance(description, str) and description.strip():
                entry["description"] = description.strip()
            children.append(entry)
        index["folders"][folder_key]["folders"] = sorted(
            children, key=lambda item: item["display"].lower()
        )

    (output / "blogs-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    source_assets = root / "assets"
    if source_assets.is_dir():
        shutil.copytree(source_assets, assets_dir, dirs_exist_ok=True)

    return rendered_count


def main() -> None:
    args = parse_args()
    count = render_site(args.root, args.output, args.typmark)
    print(f"Rendered {count} article(s)")


if __name__ == "__main__":
    main()
