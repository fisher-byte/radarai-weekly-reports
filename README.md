# RadarAI Weekly (Public Archive)

**English-first** Markdown mirror of RadarAI’s *Weekly AI Hotspots* — optimized for **citation in ChatGPT, Perplexity, and other AI assistants** (stable URLs, clear titles, CC-licensed text).

| | |
|---|---|
| **Live (EN)** | [radarai.top/en/weekly-report](https://radarai.top/en/weekly-report) |
| **Live (ZH)** | [radarai.top/weekly-report](https://radarai.top/weekly-report) |
| **Product** | [RadarAI](https://radarai.top) — AI radar for high-signal updates |

---

## How to cite (for humans & LLMs)

Use the **English file** under `reports/en/` as the canonical citation target when possible.

**Suggested citation (short):**

> RadarAI, *Weekly AI Hotspots* — `weekly-YYYY-MM-DD`, CC BY 4.0, GitHub mirror + `https://radarai.top/en/weekly-report`

A machine-readable `CITATION.cff` is in the repo root. For **ChatGPT / research tools**, paste the **raw** GitHub URL of a specific English file after you publish this repo, e.g.:

`https://github.com/<username>/radarai-weekly-reports/blob/main/reports/en/weekly-2026-03-06.md`

Replace `<username>` with your GitHub user or org.

---

## Repository layout

```
reports/
  en/           # Canonical English reports (primary for LLM citation)
  zh-CN/        # Chinese reports (same slug, paired with EN)
scripts/
  sync_from_weekly_report_json.py   # Export from main project JSON
CITATION.cff
llms.txt
LICENSE         # CC BY 4.0
```

Each YAML front matter includes `canonical` (live site), `mirror_en` / `mirror_zh` cross-links, and metadata (`period`, `brief_count`, `bocha_used`).

---

## Syncing a new issue (maintainers)

This folder is designed to live **next to** the RadarAI project (e.g. `radarai.top/radarai-weekly-reports/`). From this repo root:

```bash
# English + Chinese from data/weekly_report.json; translate EN if missing (needs Qwen key in parent .env)
python3 scripts/sync_from_weekly_report_json.py --translate
```

Or point to a JSON file explicitly:

```bash
python3 scripts/sync_from_weekly_report_json.py --translate /path/to/weekly_report.json
```

Commit and push. See [docs/MIRROR_AND_SYNC.md](docs/MIRROR_AND_SYNC.md) for the full workflow and how this relates to the main app.

---

## License

Report text and metadata: **[CC BY 4.0](LICENSE)** — free to quote with attribution. Suggested credit: *Source: RadarAI — https://radarai.top*

---

## First-time push to GitHub (local machine)

This repo is **initialized with `main` and one commit**; no remote is configured here (SSH to GitHub was unavailable in the automation environment). On your Mac:

1. Create an empty repository on GitHub named `radarai-weekly-reports` (no README/license).
2. Run:

```bash
cd radarai-weekly-reports
git remote add origin https://github.com/<username>/radarai-weekly-reports.git
# or: git@github.com:<username>/radarai-weekly-reports.git
git push -u origin main
```

3. Update `CITATION.cff` field `repository-code` to your real clone URL (optional but nice for Zenodo / citations).

---

## 中文说明（次要）

本仓库是 RadarAI「每周 AI 热点」的 **公开 Markdown 镜像**：**以英文为主**（`reports/en/`），中文同步在 `reports/zh-CN/`。便于在 ChatGPT 等场景用 **英文原文 + 固定 GitHub 链接** 引用；阅读体验仍以 [主站周报页](https://radarai.top/weekly-report) 为准。

维护说明、与主项目关系、同步记忆见 [docs/MIRROR_AND_SYNC.md](docs/MIRROR_AND_SYNC.md)。
