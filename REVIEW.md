# Repository review（Windows-only）

- Review date: 2026-09-11
- Review baseline: `9480644d9c3b7397b9bf0156f858fa3a5aad7d2c`
- Remediation: 同日 fork-local overlay（不回貢）
- Upstream reviewed through: `9480644d9c3b7397b9bf0156f858fa3a5aad7d2c`
- Primary environment: Windows 11、PowerShell、Python 3.14.7（本機 gate）；產品 Python 要求 `>=3.10`
- Status: 維護骨架與產品相依環境全面可用。R-01～R-10 已全數修復解決。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 MarkItDown 線。產品行為跟隨 `microsoft/markitdown` `9480644`，再加上本線維護骨架：繁體中文文件、Windows 原生 1-click gate、純 Windows 原生維護 CI、每週上游水位追蹤（commit、PR、issue）以及每月依賴新鮮度檢查。

針對 R-07（產品選配重型依賴），已正式引進 `requirements.txt`（核心格式）與 `requirements-all.txt`（全套 Office、PDF、音訊、雲端服務依賴），納入每月新鮮度追蹤，並修復了 Python 3.14 下 `youtube-transcript-api` 的相容性門檻，搭配 `tools/test_product.ps1` 提供可重現的 Windows 本地產品驗收能力。

上游既有之 `tests.yml` 與 `pre-commit.yml` 已加上 `if: github.repository == 'microsoft/markitdown'` 閘門，避免在本 fork 上的任何 PR 觸發不必要的未閘門建置與權限測試。

## 本輪實證

### 審查當下（`9480644`）

```text
git rev-parse HEAD
→ 9480644d9c3b7397b9bf0156f858fa3a5aad7d2c

gh repo set-default --view
→ SanHsien/markitdown
```

實查結果：
- 上游 repository 為微軟官方 `microsoft/markitdown`，採 MIT License。
- 上游 PR 水位為 `#2457`，Issue 水位為 `#2449`（編號空間對應最高至 `#2457`）。
- 根目錄包含四個 Python 套件：`markitdown`、`markitdown-ocr`、`markitdown-mcp`、`markitdown-sample-plugin`。
- 上游 workflow（`tests.yml`、`pre-commit.yml`）原本僅監聽 `pull_request`，無 repository 限制。
- 維護工具無 `os.system`／`shell=True`／`eval(`／`exec(`。

## 已修 findings

| ID | 嚴重度 | 做了什麼 |
|---|---|---|
| R-01 | P2 | `.gitignore` 加入 `.env`、`.venv`、`upstream-review-report.md`、`dependency-freshness-report.md`、`.ruff_cache/` |
| R-02 | P2 | 上游 `tests.yml`、`pre-commit.yml` 加上 `if: github.repository == 'microsoft/markitdown'` 防護閘門 |
| R-03 | P2 | 建立獨立維護測試目錄 `tools/tests/` 與獨立 `tools/pytest.ini`，避免產品環境污染 |
| R-04 | P2 | 建立 `FORK.md`、`NOTICE.md`、`SECURITY.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`，寫明對外邊界與安全性 |
| R-05 | P3 | `README.md`（繁體中文）與 `README.en.md`（上游英文鏡像）雙向互指，並標明微軟 upstream 與 MIT 條款 |
| R-06 | P2 | 建立 `tools/dev_check.ps1` 與 `tools/bootstrap_dev.ps1`，規範 Windows 11 原生 PowerShell 驗收門禁 |
| R-07 | P2 | 引進 `requirements.txt` 與 `requirements-all.txt`，涵蓋核心、Office/PDF/音訊及 OCR/MCP/Plugin 擴充套件依賴（共 26 項）；修復 Python 3.14 下 `youtube-transcript-api` 相容性；納入新鮮度檢查並提供 `tools/test_product.ps1` 支援多套件隔離驗收 |
| R-08 | P2 | 清理殘留之根目錄與 `packages/markitdown-mcp/` 之 `Dockerfile`、`.dockerignore`、`.devcontainer/` 與 `.pre-commit-config.yaml`，去除 Docker 指引改為 Windows 原生配置，落實純 Windows 維護標準 |
| R-09 | P2 | 移除非 Windows 平台設定與 CI 矩陣，全面收斂為純 Windows 原生維護（`ci.yml`、`codeql.yml`、`tests.yml` 等） |
| R-10 | P2 | 修復 `tools/check_upstream_updates.py` 未捕獲 `OSError`（如未安裝 `gh` CLI）導致例外中斷的缺陷，使其安全返回 `None` 並標示 `Not checked` |

## 接受、不改契約

| ID | 嚴重度 | 處理 |
|---|---|---|
| - | - | （無。所有已識別項目皆已妥善處理完畢） |

## 尚未宣稱範圍

- **沒有**測試跨平臺音訊硬體裝置或雲端即時 Document Intelligence 授權轉譯。
- **沒有**在未設 `PYTHONUTF8` 的舊版主控台驗證 CLI 中文輸出。
- **不宣稱** 本 fork 發佈獨立 PyPI 套件取代官方發行（本 fork 採 0.2.0 自主維護里程碑版號，不對外發佈 PyPI）。
- **不宣稱** 已將任何修改提交回微軟上游。
