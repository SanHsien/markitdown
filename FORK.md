# Fork 維護說明

本 repo fork 自 [`microsoft/markitdown`](https://github.com/microsoft/markitdown)，
沿用 MIT License 與完整 Git 歷史。

## 為什麼維護 fork

- 保留微軟原作者持續更新的文件轉 Markdown 核心引擎、各類格式外掛與 MCP 伺服器支援。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整驗收環境。
- 公開入口改以繁體中文為主，英文鏡像放 `README.en.md`。
- 建立可重現的 Windows 開發 gate、Windows CI job，以及逐筆審查的上游追蹤（涵蓋 commit、PR 與 issue 水位）。
- 版本採本 fork 自主管理（主版本已升為 0.2.0，標記 Windows 11 原生維護與全依賴完備），發行與標籤依本線推進，維護同步時主動處理上游衝突。不發佈第三方 PyPI 套件取代官方管道。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**
回貢前必須在當次對話取得維護者明確同意；「fork」「建開發環境」「開 PR」都不是同意。

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 繁中主檔；上游英文移到 `README.en.md` |
| `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` | 本 fork 的 AI 維護單一真相源 |
| `NOTICE.md` / `FORK.md` | 來源、授權與同步說明 |
| `tools/dev_check.ps1` | Windows 本機一鍵 gate（維護工具，不安裝重型產品依賴） |
| `tools/bootstrap_dev.ps1` | Windows 本機一鍵初始化與驗收（支援 `-All` 參數安裝全套產品依賴） |
| `tools/test_product.ps1` | Windows 原生產品測試執行腳本（自動載入本機 source 避免 site-packages 污染） |
| `requirements.txt` / `requirements-all.txt` | MarkItDown 核心與全套格式（Office、PDF、音訊、雲端）產品依賴清單 |
| `.github/workflows/ci.yml` | 純 Windows 原生 CI (windows-latest Python 3.10–3.14 矩陣)：compile / ruff / 維護測試 / 連結檢查 |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit、PR、issue 水位檢查 |
| `.github/workflows/dependency-freshness.yml` | 每月依賴新鮮度檢查 |
| 產品 CI workflow 閘門 | 上游 `tests.yml`、`pre-commit.yml` 加上 `if: github.repository == 'microsoft/markitdown'` 防護 |
| `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`docs/DEVELOPMENT.md` | fork 維護文件 |
| `REVIEW.md` | 全庫風險與安全快照 |

產品程式碼在 `packages/` 底下，以上游為準。

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 日常修改在本機跑 gate 後直接推 `origin/main`。
- `upstream/main`：microsoft 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

上游更新英文 `README.md` 時，把新內容併進 `README.en.md`，再把對應段落翻進本 fork 的繁中 `README.md`。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/markitdown.git
cd markitdown
# `gh repo clone` 已會加上 `upstream` remote；若沒有：
# git remote add upstream https://github.com/microsoft/markitdown.git
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

要實際測試個別套件或安裝完整轉換格式，見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。
