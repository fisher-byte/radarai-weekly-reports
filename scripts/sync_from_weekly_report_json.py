#!/usr/bin/env python3
"""
Export RadarAI weekly report JSON to Markdown: English-first (reports/en/), Chinese (reports/zh-CN/).

Usage:
  python3 scripts/sync_from_weekly_report_json.py [--translate] [path/to/weekly_report.json]

  --translate   If content_en is empty, call Qwen via main project (requires ../.env with QWEN_API_KEY
                and services/app_core.py import path). Omit if you only sync existing content_en.

Default JSON path: ../data/weekly_report.json when this repo lives inside the RadarAI project.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _load_dotenv(env_path: Path) -> None:
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def _resolve_src(repo_root: Path, arg: str | None) -> Path | None:
    if arg:
        p = Path(arg).expanduser().resolve()
        return p if p.exists() else None
    candidates = [
        repo_root.parent / "data" / "weekly_report.json",
        repo_root.parent.parent / "radarai.top" / "data" / "weekly_report.json",
    ]
    for p in candidates:
        if p.exists():
            return p.resolve()
    return None


def _translate_zh_to_en(zh: str, main_root: Path) -> str:
    """Use RadarAI app_core translator when available."""
    sys.path.insert(0, str(main_root))
    _load_dotenv(main_root / ".env")
    from services.app_core import _translate_weekly_report_to_en  # noqa: E402

    key = os.environ.get("QWEN_API_KEY") or os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        return ""
    return (_translate_weekly_report_to_en(zh, key) or "").strip()


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    main_project = repo_root.parent

    ap = argparse.ArgumentParser(description="Sync weekly report JSON to en/zh Markdown.")
    ap.add_argument(
        "json_path",
        nargs="?",
        default=None,
        help="Path to weekly_report.json",
    )
    ap.add_argument(
        "--translate",
        action="store_true",
        help="Fill English from Qwen when content_en is empty (needs main project + .env)",
    )
    args = ap.parse_args()

    src = _resolve_src(repo_root, args.json_path)
    if not src:
        print("weekly_report.json not found. Pass path explicitly.", file=sys.stderr)
        return 1

    data = json.loads(src.read_text(encoding="utf-8"))
    slug = data.get("slug") or "weekly-unknown"
    period = data.get("period", "")
    gen = data.get("generated_at", "")
    zh_body = (data.get("content") or "").strip()
    en_body = (data.get("content_en") or "").strip()

    if not en_body and args.translate:
        if not (main_project / "services" / "app_core.py").is_file():
            print("Cannot --translate: main project app_core.py not found next to this repo.", file=sys.stderr)
            return 1
        print("Translating to English (Qwen)...", file=sys.stderr)
        en_body = _translate_zh_to_en(zh_body, main_project)
        if not en_body:
            print("Translation failed or empty.", file=sys.stderr)
            return 1

    en_dir = repo_root / "reports" / "en"
    zh_dir = repo_root / "reports" / "zh-CN"
    en_dir.mkdir(parents=True, exist_ok=True)
    zh_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "slug": slug,
        "period": period,
        "generated_at": gen,
        "brief_count": data.get("brief_count", 0),
        "bocha_used": data.get("bocha_used", False),
    }

    fm_en = f"""---
title: "Weekly AI Hotspots"
lang: en
slug: {meta["slug"]}
period: "{period}"
generated_at: "{gen}"
brief_count: {meta["brief_count"]}
bocha_used: {str(meta["bocha_used"]).lower()}
canonical: https://radarai.top/en/weekly-report
mirror_zh: reports/zh-CN/{slug}.md
---

"""
    fm_zh = f"""---
title: 每周 AI 热点
lang: zh-CN
slug: {meta["slug"]}
period: "{period}"
generated_at: "{gen}"
brief_count: {meta["brief_count"]}
bocha_used: {str(meta["bocha_used"]).lower()}
canonical: https://radarai.top/weekly-report
mirror_en: reports/en/{slug}.md
---

"""
    en_path = en_dir / f"{slug}.md"
    zh_path = zh_dir / f"{slug}.md"

    if en_body:
        en_path.write_text(fm_en + en_body + "\n", encoding="utf-8")
        print(f"Wrote {en_path.relative_to(repo_root)}")
    else:
        print(f"Skip EN (no content_en); use --translate or generate on server. {en_path.name} not written.", file=sys.stderr)

    if zh_body:
        zh_path.write_text(fm_zh + zh_body + "\n", encoding="utf-8")
        print(f"Wrote {zh_path.relative_to(repo_root)}")
    else:
        print("Skip ZH (no content).", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
