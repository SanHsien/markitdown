# 維護決策

## 2026-09-11：建立 Windows-first 維護型 fork

**決定**：fork `microsoft/markitdown`，保留 MIT License 與完整歷史。本線預設分支用 `main`。本線聚焦繁中文件、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：MarkItDown 是微軟開源的多格式文件轉 Markdown 實用工具，在搭配大型語言模型（LLM）的文字萃取流程中非常關鍵。本 fork 補足 Windows 11 原生開發／驗收骨架、繁體中文入口，以及可審計的上游追蹤機制。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者、微軟商標與官方連結。
- 不發佈 PyPI 取代官方 `markitdown` 套件。
- 維護 gate 不預設安裝龐大的產品 optional 依賴。
- 上游更新必須逐筆審查。

## 2026-09-11：產品 CI workflow 加上游 repo 閘門

**決定**：在 `tests.yml` 與 `pre-commit.yml` 加上 `if: github.repository == 'microsoft/markitdown'`。

**理由**：避免在本 fork 上的 PR 觸發上游重量級多版本矩陣與環境測試。本 fork 擁有自己的專屬維護 CI（`ci.yml`）。

## 2026-09-11：依賴新鮮度只看維護工具

**決定**：`tools/check_dependency_freshness.py` 只讀 `requirements-dev.txt`。各套件 `pyproject.toml` 的產品依賴交給 Dependabot。

**理由**：產品依賴（如 pdfminer、mammoth、openpyxl、azure-ai-* 等）範圍廣泛，若與維護門禁混在一起會造成噪音。保持維護工具（pytest, ruff）的相容性檢查清晰可讀。

## 2026-09-11：上游檢查涵蓋 Commit、PR 與 Issue 三面向

**決定**：`check_upstream_updates.py` 以 `--state all` 收集上游 PR 與 Issue，並追蹤 Commit SHA。`gh` 失敗時 fail closed（exit 2）。

**理由**：未合併即關閉的 PR 與待處理的 Issue 同樣可能揭露重要缺陷或需求。排程報告必須確保「未檢查」與「沒有新變更」截然分明。

## 2026-09-11：日常直接推 main

**決定**：日常維護修改在本機跑 `tools\dev_check.ps1` 後直接推 `origin/main`。Dependabot 與外部貢獻仍走 PR，合併前讀 diff。

**理由**：對齊 SanHsien 體系其他維護 fork 的治理規範。
