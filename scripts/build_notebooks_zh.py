#!/usr/bin/env python3
"""
Append Chinese translations to Markdown cells in Jupyter notebooks.

- Keeps English source unchanged; adds --- and **中文** section after each
  non-empty Markdown cell.
- Does not modify code cells or notebook structure.
- Preserves fenced code blocks and inline `code` segments (not translated).

Optional: BRICS_GLOSSARY_REPLACEMENTS normalizes common ML/stats terms after MT.
"""
from __future__ import annotations

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
SKIP_SUBPATHS = ("Week5/data/",)

# Applied to translated Chinese only (teaching glossary).
GLOSSARY: list[tuple[str, str]] = [
    (r"\bregression\b", "回归"),
    (r"\bclassification\b", "分类"),
    (r"\bfeatures?\b", "特征"),
    (r"\blabels?\b", "标签"),
    (r"\bmodels?\b", "模型"),
    (r"\btraining\b", "训练"),
    (r"\btesting\b", "测试"),
    (r"\bdatasets?\b", "数据集"),
    (r"\bpipelines?\b", "流程"),
    (r"\btasks?\b", "任务"),
]

FENCE_RE = re.compile(r"(```[\s\S]*?```)")


def _join_source(cell: dict) -> str:
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return str(src)


def _set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True) if text else [""]


ZH_SEP = "\n\n---\n\n**中文**\n\n"


def strip_existing_zh_section(en: str) -> str:
    """Remove a previously appended bilingual block so rebuilds stay idempotent."""
    if ZH_SEP in en:
        return en.split(ZH_SEP)[0]
    alt = "\r\n\r\n---\r\n\r\n**中文**\r\n\r\n"
    if alt in en:
        return en.split(alt)[0]
    return en


def protect_segments(text: str) -> tuple[list[str], str]:
    """Replace ```...``` blocks with placeholders."""
    parts: list[str] = []

    def repl(m: re.Match) -> str:
        parts.append(m.group(1))
        return f"@@CODEBLOCK{len(parts)-1}@@"

    masked = FENCE_RE.sub(repl, text)
    return parts, masked


def unprotect_segments(parts: list[str], text: str) -> str:
    for i, block in enumerate(parts):
        text = text.replace(f"@@CODEBLOCK{i}@@", block)
    return text


INLINE_CODE_RE = re.compile(r"(`[^`\n]+`)")


def protect_inline(text: str) -> tuple[list[str], str]:
    parts: list[str] = []

    def repl(m: re.Match) -> str:
        parts.append(m.group(1))
        return f"@@INLINE{len(parts)-1}@@"

    return parts, INLINE_CODE_RE.sub(repl, text)


def unprotect_inline(parts: list[str], text: str) -> str:
    for i, p in enumerate(parts):
        text = text.replace(f"@@INLINE{i}@@", p)
    return text


def apply_glossary(zh: str) -> str:
    out = zh
    for pat, rep in GLOSSARY:
        out = re.sub(pat, rep, out, flags=re.IGNORECASE)
    return out


def translate_chunks(text: str, translator: GoogleTranslator, delay_s: float = 0.08) -> str:
    text = text.strip()
    if not text:
        return ""
    max_len = 4500
    chunks: list[str] = []
    i = 0
    while i < len(text):
        chunk = text[i : i + max_len]
        last_err: Exception | None = None
        for attempt in range(4):
            try:
                chunks.append(translator.translate(chunk))
                break
            except Exception as e:  # noqa: BLE001
                last_err = e
                time.sleep(1.5 * (attempt + 1))
        else:
            raise RuntimeError(f"Translation failed after retries: {last_err}") from last_err
        i += max_len
        time.sleep(delay_s)
    return "".join(chunks)


HEADING_LINE_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _has_cjk(s: str) -> bool:
    return any("\u4e00" <= c <= "\u9fff" for c in s)


def _translate_short(text: str, translator: GoogleTranslator) -> str:
    last_err: Exception | None = None
    for attempt in range(4):
        try:
            return translator.translate(text)
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Translation failed: {last_err}") from last_err


def translate_heading_line(line: str, translator: GoogleTranslator) -> str:
    m = HEADING_LINE_RE.match(line.strip())
    if not m:
        return line
    hashes, title = m.group(1), m.group(2)
    if not title or title.startswith("@@"):
        return line
    if _has_cjk(title):
        return line
    if re.fullmatch(r"[\d\s.\-+*/^=()]+$", title):
        return line
    zh_title = _translate_short(title, translator).strip()
    return f"{hashes} {zh_title}"


def translate_markdown_cell(en: str, translator: GoogleTranslator) -> str:
    fb_parts, masked = protect_segments(en)
    il_parts, masked2 = protect_inline(masked)
    zh = translate_chunks(masked2, translator)
    zh = unprotect_inline(il_parts, zh)
    zh = unprotect_segments(fb_parts, zh)
    zh = apply_glossary(zh)
    # Normalize Markdown headings to Chinese (machine translation often leaves English titles).
    out_lines: list[str] = []
    for line in zh.splitlines(keepends=True):
        bare = line.rstrip("\r\n")
        eol = line[len(bare) :]
        if bare.strip() and not bare.strip().startswith("```"):
            fixed = translate_heading_line(bare, translator)
            out_lines.append(fixed + eol if fixed != bare else line)
        else:
            out_lines.append(line)
    return "".join(out_lines)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    for s in SKIP_SUBPATHS:
        if rel.startswith(s):
            return True
    if path.name.endswith("_zh.ipynb"):
        return True
    return False


def process_notebook(src: Path, dst: Path, translator: GoogleTranslator) -> int:
    with src.open(encoding="utf-8") as f:
        nb = json.load(f)
    out = copy.deepcopy(nb)
    changed = 0
    for cell in out.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        en = strip_existing_zh_section(_join_source(cell))
        if not en.strip():
            continue
        zh = translate_markdown_cell(en, translator)
        if not zh.strip():
            continue
        merged = en.rstrip() + ZH_SEP + zh.strip() + "\n"
        _set_source(cell, merged)
        changed += 1
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return changed


def main() -> None:
    translator = GoogleTranslator(source="en", target="zh-CN")
    total_cells = 0
    for src in sorted(ROOT.rglob("*.ipynb")):
        if should_skip(src):
            continue
        stem = src.stem
        if stem.endswith("_zh"):
            continue
        dst = src.with_name(stem + "_zh.ipynb")
        n = process_notebook(src, dst, translator)
        rel = src.relative_to(ROOT)
        print(f"{rel}: updated {n} markdown cells -> {dst.name}")
        total_cells += n
    print(f"Done. Total markdown cells merged: {total_cells}")


if __name__ == "__main__":
    main()
