# Mirror, sync & memory (maintainers)

## What this repo is

- **Purpose**: Public, **English-first** archive of RadarAI’s weekly editorial (`Weekly AI Hotspots`), paired with **Chinese** in `reports/zh-CN/`.
- **Product source of truth**: The Flask app generates `weekly_report` data (Qwen + optional Bocha). This repo **only mirrors** exported Markdown for GitHub / LLM citation — it does not run the pipeline by itself.

## Relationship to the main project

| Artifact | Main project | This repo |
|----------|--------------|-----------|
| Generation | `POST /api/weekly-report/generate` (cron) | — |
| Storage | SQLite + optional `data/weekly_report.json` (gitignored in main) | Git-tracked `reports/en`, `reports/zh-CN` |
| English body | `content_en` in saved JSON (filled on generate) | `reports/en/<slug>.md` |
| Chinese body | `content` | `reports/zh-CN/<slug>.md` |

Main project path (typical): `radarai.top/` next to or above this folder as `radarai-weekly-reports/`.

## Sync steps (after a new weekly issue exists on the server)

1. Copy or ensure `weekly_report.json` reflects the latest issue (or use DB export if you only have SQLite).
2. From **this** repo root:

   ```bash
   python3 scripts/sync_from_weekly_report_json.py --translate
   ```

   - `--translate` calls the same Qwen translator as `services/app_core._translate_weekly_report_to_en` when `content_en` is empty (requires parent `.env` with `QWEN_API_KEY`).

3. Commit and push this repository.

## Why English-first

- **ChatGPT / Perplexity / academic tools** cite English sources more reliably.
- The live canonical EN page is `https://radarai.top/en/weekly-report`; YAML `canonical` in EN files matches that.

## Git layout note

The RadarAI **main** repo lists `radarai-weekly-reports/` in `.gitignore` so this directory can use its **own** `git` remote without nested-repo confusion. Clone or copy this folder when working on the mirror.

**GitHub 推送、与主项目 `origin` 对齐、Token 安全**：见 [GITHUB_SYNC_PLAYBOOK.md](GITHUB_SYNC_PLAYBOOK.md)。

## License reminder

Content: **CC BY 4.0**. Keep `LICENSE` in sync with the README credit line.
