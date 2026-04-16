#!/usr/bin/env python3
"""
Export RadarAI weekly report data to Markdown: English-first (reports/en/), Chinese (reports/zh-CN/).

Usage:
  python3 scripts/sync_from_weekly_report_json.py [--translate] [path/to/weekly_report.json|path/to/radarai.db]

  --translate   If content_en is empty, call Qwen via main project (requires ../.env with QWEN_API_KEY
                and services/app_core.py import path). Omit if you only sync existing content_en.

Default source priority when this repo lives inside the RadarAI project:
  1. ../data/server_snapshots/<latest>/radarai.db
  2. ../data/radarai.db
  3. ../data/weekly_report.json
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
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


def _latest_snapshot_db(main_root: Path) -> Path | None:
    snapshot_root = main_root / "data" / "server_snapshots"
    if not snapshot_root.exists():
        return None
    candidates = sorted(snapshot_root.glob("20*/radarai.db"), reverse=True)
    return candidates[0].resolve() if candidates else None


def _resolve_src(repo_root: Path, arg: str | None) -> Path | None:
    main_root = repo_root.parent
    if arg:
        p = Path(arg).expanduser().resolve()
        return p if p.exists() else None
    candidates = [
        _latest_snapshot_db(main_root),
        main_root / "data" / "radarai.db",
        main_root / "data" / "weekly_report.json",
        main_root.parent / "radarai.top" / "data" / "weekly_report.json",
    ]
    for p in candidates:
        if p and p.exists():
            return p.resolve()
    return None


def _load_weekly_from_db(db_path: Path) -> dict | None:
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute("SELECT data FROM weekly_report WHERE id = 1").fetchone()
    finally:
        conn.close()
    if not row or not row[0]:
        return None
    return json.loads(row[0])


def _load_historical_weeklies_from_db(db_path: Path) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT slug, created_at, content, content_en
            FROM updates
            WHERE type = 'weekly_report'
            ORDER BY created_at ASC
            """
        ).fetchall()
    finally:
        conn.close()

    items: list[dict] = []
    for row in rows:
        items.append(
            {
                "slug": row["slug"],
                "period": "",
                "generated_at": row["created_at"] or "",
                "brief_count": 0,
                "bocha_used": False,
                "content": (row["content"] or "").strip(),
                "content_en": (row["content_en"] or "").strip(),
            }
        )
    return items


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
        print("weekly report source not found. Pass JSON or DB path explicitly.", file=sys.stderr)
        return 1

    reports: list[dict]
    if src.suffix.lower() == ".db":
        latest = _load_weekly_from_db(src)
        reports = _load_historical_weeklies_from_db(src)
        if latest:
            merged = {item.get("slug"): item for item in reports}
            merged[latest.get("slug") or "weekly-unknown"] = latest
            reports = [merged[k] for k in sorted(merged.keys())]
        if not reports:
            print(f"weekly_report not found in DB: {src}", file=sys.stderr)
            return 1
    else:
        reports = [json.loads(src.read_text(encoding="utf-8"))]

    en_dir = repo_root / "reports" / "en"
    zh_dir = repo_root / "reports" / "zh-CN"
    en_dir.mkdir(parents=True, exist_ok=True)
    zh_dir.mkdir(parents=True, exist_ok=True)

    for data in reports:
        slug = data.get("slug") or "weekly-unknown"
        period = data.get("period", "")
        gen = data.get("generated_at", "")
        zh_body = (data.get("content") or "").strip()
        en_body = (data.get("content_en") or "").strip()

        if not en_body and args.translate:
            if not (main_project / "services" / "app_core.py").is_file():
                print("Cannot --translate: main project app_core.py not found next to this repo.", file=sys.stderr)
                return 1
            print(f"Translating to English (Qwen) for {slug}...", file=sys.stderr)
            en_body = _translate_zh_to_en(zh_body, main_project)
            if not en_body:
                print(f"Translation failed or empty for {slug}.", file=sys.stderr)
                return 1

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
            print(f"Skip ZH (no content) for {slug}.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
