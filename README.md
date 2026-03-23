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

`https://github.com/fisher-byte/radarai-weekly-reports/blob/main/reports/en/weekly-2026-03-06.md`

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

## GitHub remote (already live)

- **Repository**: [github.com/fisher-byte/radarai-weekly-reports](https://github.com/fisher-byte/radarai-weekly-reports)  
- **Default branch**: `main`  
- First-time setup / rotation / 与主项目对齐的推送方式见 [docs/GITHUB_SYNC_PLAYBOOK.md](docs/GITHUB_SYNC_PLAYBOOK.md)。

---

## 中文说明（次要）

本仓库是 RadarAI「每周 AI 热点」的 **公开 Markdown 镜像**：**以英文为主**（`reports/en/`），中文同步在 `reports/zh-CN/`。便于在 ChatGPT 等场景用 **英文原文 + 固定 GitHub 链接** 引用；阅读体验仍以 [主站周报页](https://radarai.top/weekly-report) 为准。

维护说明、与主项目关系、同步记忆见 [docs/MIRROR_AND_SYNC.md](docs/MIRROR_AND_SYNC.md)。
