#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import time
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Install: pip install deep-translator", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
SKIP_SUBPATHS: tuple[str, ...] = ()

FENCE_RE = re.compile(r"(```[\s\S]*?```)")
INLINE_CODE_RE = re.compile(r"(`[^`\n]+`)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
MD_AUTOLINK_RE = re.compile(r"<https?://[^>\s]+>")
MD_LINK_RE = re.compile(r"!?(\[[^\]]*\]\([^)]+\))")
MD_NESTED_BADGE_RE = re.compile(r"\[\s*!\[[^\]]*\]\([^)]+\)\s*\]\([^)]+\)")
HTML_TAG_LINE_RE = re.compile(r"^\s*<[^>]+>\s*$")
HTML_DIV_BLOCK_RE = re.compile(r"<div\b[^>]*>[\s\S]*?</div>", re.IGNORECASE)


def _join_source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def _set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True) if text else [""]


def _has_cjk(s: str) -> bool:
    return any("\u4e00" <= c <= "\u9fff" for c in s)


def _protect(pattern: re.Pattern[str], text: str, token: str) -> tuple[list[str], str]:
    items: list[str] = []

    def repl(m: re.Match[str]) -> str:
        items.append(m.group(0))
        return f"@@{token}{len(items)-1}@@"

    return items, pattern.sub(repl, text)


def _unprotect(items: list[str], text: str, token: str) -> str:
    out = text
    for i, v in enumerate(items):
        out = out.replace(f"@@{token}{i}@@", v)
    return out


def _translate(text: str, translator: GoogleTranslator, delay: float = 0.08) -> str:
    text = text.strip()
    if not text:
        return ""
    max_len = 4500
    out: list[str] = []
    i = 0
    while i < len(text):
        chunk = text[i : i + max_len]
        last_err: Exception | None = None
        for a in range(4):
            try:
                res = translator.translate(chunk)
                # Some providers may return None for edge chunks; keep pipeline robust.
                out.append(res if isinstance(res, str) and res else chunk)
                break
            except Exception as e:  # noqa: BLE001
                last_err = e
                time.sleep(1.2 * (a + 1))
        else:
            raise RuntimeError(f"Translation failed: {last_err}") from last_err
        i += max_len
        time.sleep(delay)
    return "".join(out)


def _translate_heading(line: str, translator: GoogleTranslator) -> str:
    m = HEADING_RE.match(line.strip())
    if not m:
        return line
    prefix, title = m.group(1), m.group(2).strip()
    title = re.sub(r"（[^）]+）\s*$", "", title).strip()
    if not title or _has_cjk(title):
        return f"{prefix} {title}".rstrip()
    zh = _translate(title, translator, delay=0.03).strip()
    return f"{prefix} {title}（{zh}）"


def _is_link_like(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return bool(MD_NESTED_BADGE_RE.fullmatch(s) or MD_LINK_RE.fullmatch(s) or MD_AUTOLINK_RE.fullmatch(s))


def _is_nontext(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith("```") or s.startswith("@@FENCE"):
        return True
    if HTML_TAG_LINE_RE.fullmatch(s):
        return True
    if _is_link_like(s):
        return True
    return False


def _translate_text_block(text: str, translator: GoogleTranslator) -> str:
    fence, masked = _protect(FENCE_RE, text, "FENCE")
    html, masked = _protect(HTML_DIV_BLOCK_RE, masked, "HTML")
    badge, masked = _protect(MD_NESTED_BADGE_RE, masked, "BADGE")
    links, masked = _protect(MD_LINK_RE, masked, "LINK")
    autolinks, masked = _protect(MD_AUTOLINK_RE, masked, "AUTO")
    inline, masked = _protect(INLINE_CODE_RE, masked, "INLINE")

    zh = _translate(masked, translator)
    zh = _unprotect(inline, zh, "INLINE")
    zh = _unprotect(autolinks, zh, "AUTO")
    zh = _unprotect(links, zh, "LINK")
    zh = _unprotect(badge, zh, "BADGE")
    zh = _unprotect(html, zh, "HTML")
    zh = _unprotect(fence, zh, "FENCE")
    return zh.strip()


def _split_blocks(md: str) -> list[str]:
    text = md.strip("\n")
    html, masked = _protect(HTML_DIV_BLOCK_RE, text, "HTML")
    fence, masked = _protect(FENCE_RE, masked, "FENCE")
    parts = [p for p in re.split(r"\n\s*\n", masked) if p.strip()]
    out: list[str] = []
    for p in parts:
        p = _unprotect(fence, p, "FENCE")
        p = _unprotect(html, p, "HTML")
        out.append(p.strip("\n"))
    return out


def _merge_blocks(blocks: list[str]) -> str:
    return "\n\n".join(b for b in blocks if b.strip()).rstrip() + "\n"


def translate_markdown(md: str, translator: GoogleTranslator) -> str:
    out: list[str] = []
    last_link: str | None = None
    for block in _split_blocks(md):
        lines = block.splitlines()
        if len(lines) == 1 and HEADING_RE.match(lines[0].strip()):
            out.append(_translate_heading(lines[0], translator))
            continue

        if len(lines) == 1 and _is_link_like(lines[0]):
            link = lines[0].strip()
            if link != last_link:
                out.append(link)
            last_link = link
            continue

        out.append(block.rstrip())

        text_lines = [ln for ln in lines if not _is_nontext(ln)]
        if text_lines:
            zh = _translate_text_block("\n".join(text_lines), translator)
            if zh:
                out.append(zh)

    return _merge_blocks(out)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return path.name.endswith("_zh.ipynb") or any(rel.startswith(s) for s in SKIP_SUBPATHS)


def process_notebook(src: Path, translator: GoogleTranslator) -> int:
    dst = src.with_name(src.stem + "_zh.ipynb")
    with src.open(encoding="utf-8") as f:
        nb = json.load(f)
    out = copy.deepcopy(nb)
    changed = 0
    md_cells = [c for c in out.get("cells", []) if c.get("cell_type") == "markdown"]
    md_total = len(md_cells)
    md_idx = 0
    for cell in out.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        md_idx += 1
        print(f"    - markdown cell {md_idx}/{md_total}", flush=True)
        en = _join_source(cell)
        if not en.strip():
            continue
        _set_source(cell, translate_markdown(en, translator))
        changed += 1
    with dst.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="optional source notebooks")
    args = ap.parse_args()

    translator = GoogleTranslator(source="en", target="zh-CN")
    sources = [ROOT / p for p in args.paths] if args.paths else sorted(ROOT.rglob("*.ipynb"))
    total = 0
    valid_sources: list[Path] = []
    for src in sources:
        src = src.resolve()
        if src.exists() and not should_skip(src):
            valid_sources.append(src)

    print(f"Total files to process: {len(valid_sources)}", flush=True)

    for idx, src in enumerate(valid_sources, start=1):
        print(f"[{idx}/{len(valid_sources)}] {src.relative_to(ROOT)}", flush=True)
        n = process_notebook(src, translator)
        print(
            f"  done: updated {n} markdown cells -> {src.stem}_zh.ipynb",
            flush=True,
        )
        total += n
    print(f"Done. Total markdown cells processed: {total}", flush=True)


if __name__ == "__main__":
    main()
