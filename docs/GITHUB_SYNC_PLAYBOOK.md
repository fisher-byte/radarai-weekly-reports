# GitHub 同步手记（主项目 + 周报镜像）

本文记录 **RadarAI 主仓** 与 **周报公开仓** 在 GitHub 上的关系、推送习惯与安全注意，便于以后换机器或交接时照做。

---

## 1. 主项目（本体）怎么对上 GitHub

主仓库当前约定（以你机器上 `git remote -v` 为准）：

- `origin` → `https://github.com/fisher-byte/auto-firm.git`（GitHub）
- 另有 `gongfeng` → 腾讯工蜂（备份/第二远程，按需使用）

日常「跟 GitHub 同步」一般指：

```bash
cd /path/to/radarai.top
git status
git add … && git commit -m "…"
git push origin <当前分支名>
```

分支名按你们习惯（例如 `backup-…` 或 `main`），**以 `origin` 为准**推到 GitHub。

---

## 2. 周报镜像仓（本目录）为什么单独一个 repo

- 周报仓路径：`radarai.top/radarai-weekly-reports/`（物理上可在主项目里，但 **主项目 `.gitignore` 已忽略本目录**）。
- 本目录 **自带独立 `.git`**，远程为 **另一个** GitHub 仓库，与 `auto-firm` 分离，避免把公开 Markdown 和私有应用代码绑在同一发布节奏里。
- **线上地址**：https://github.com/fisher-byte/radarai-weekly-reports  
- **默认分支**：`main`

---

## 3. 新建远程仓库的两种方式

**A. 网页**：GitHub → New repository → 名称 `radarai-weekly-reports` → 空仓库（不要勾选自动 README）。

**B. API**（适合自动化；需要 `GITHUB_TOKEN`，权限含 `repo` 或至少 `public_repo`）：

```bash
# 在雷达项目根目录且已配置 .env 时示例（勿把 token 写进命令历史或截图）
set -a && . ./.env && set +a
curl -sS -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{"name":"radarai-weekly-reports","private":false,"homepage":"https://radarai.top/en/weekly-report"}'
```

---

## 4. 周报仓推送（推荐习惯）

**推荐：SSH（与「本机已配密钥」一致）**

```bash
cd radarai-weekly-reports
git remote -v   # 应为 git@github.com:fisher-byte/radarai-weekly-reports.git 或等价 HTTPS
git push -u origin main
```

**HTTPS**：可用 macOS 钥匙串 / `gh auth login` 缓存凭据，**不要把 `https://oauth2:TOKEN@github.com/...` 写进 `git config` 或长期留在 `branch.*.remote`**，否则容易泄露；若曾误配，立刻改回 `origin` 的干净 URL，并 **轮换 GitHub Token**。

---

## 5. 内容同步后再推送（每期周报）

```bash
cd radarai-weekly-reports
python3 scripts/sync_from_weekly_report_json.py --translate   # 需主项目 .env 里 Qwen Key
git add reports/ README.md CITATION.cff llms.txt  # 按需
git commit -m "sync weekly-YYYY-MM-DD"
git push origin main
```

---

## 6. 安全经验（务必记住）

1. **Token 视为密码**：出现在终端输出、录屏、Issue、聊天记录里 = 作废，到 GitHub → Settings → Developer settings → 撤销并新建。  
2. **推送成功后**检查 `radarai-weekly-reports/.git/config`：`[branch "main"]` 的 `remote` 应是 **`origin`**，不是带 token 的完整 URL。  
3. **自动化脚本**里若必须用 token，优先用环境变量 + `curl`，避免 `git push https://…token…` 被 Git 回显到 stdout。  
4. 主项目 `.env` 里的 `GITHUB_TOKEN` 仅用于 API（如速率限制、建库），**不要提交到仓库**（已在 `.gitignore`）。

---

## 7. 与主项目文档的交叉引用

- 同步逻辑与数据关系：`MIRROR_AND_SYNC.md`  
- Agent 侧一句话入口：主项目根目录 `CLAUDE.md`  

---

*最后更新：与 `fisher-byte/radarai-weekly-reports` 首次建库、推 `main` 的流程对齐。*
