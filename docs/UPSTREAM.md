# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/markitdown.git`（預設分支 `main`）
- 原作者：`upstream` → `https://github.com/microsoft/markitdown.git`（預設分支 `main`）
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交、PR 與 Issues。
有新變更或檢查失敗時，`--strict` 回傳非零；排程 workflow 也會因此明確亮紅燈提醒。

CI 沒有 `upstream` remote，所以 baseline 的 `repo` 寫完整 clone URL，不要寫遠端短名。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案（open PR 必須讀 diff，禁止只憑標題結案）。
2. 判斷是否與繁中 README、Windows gate、發佈閘門或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
5. 在 `docs/DECISIONS.md` 記錄採用／略過理由。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA 與更新 PR/Issue 水位。

Baseline 代表「已審查」，不代表「全部已合併」。

## 2026-09-11：fork 起點

本 fork 自上游 `main` `9480644d9c3b7397b9bf0156f858fa3a5aad7d2c`
（`Added file paths tests. (#2454)`）建立。此 SHA 設為第一個 `reviewed_through`（短 SHA 為 `9480644`）。
之後的上游 commit 才需要進入審查清冊。

---

## 2026-09-11：上游 PR、Issue、分支全面盤點（一次評估，之後只看增量）

2026-09-11 對微軟官方 [`microsoft/markitdown`](https://github.com/microsoft/markitdown) 進行完整盤點：
**6 個非 main 分支、317 個 open PR、317 個 open Issue**。
評估結論與盤點原則如下，記錄於本檔與 [`docs/DECISIONS.md`](DECISIONS.md)，避免未來重複評估。

### 一、上游分支盤點：全面比對，不盲目引進

上游 remote 共有 6 個非 main 分支，經由 `git log upstream/main..<branch>` 逐一對照：

| 分支名稱 | 內容摘要與相對於 main 的差異 | 本輪評估結論與理由 |
|---|---|---|
| `upstream/v0.0.X` | 0.1.X 套件化架構重組前的歷史維護線，最後 commit 為 `abe9752` / `#1105` | **不引進**。屬於歷史過期分支，上游 0.1.X 已重構為 `packages/` monorepo 架構，所有功能皆已在 `main` 演進。 |
| `upstream/onenote` | 僅 1 個 commit `da73d64`（`Initial work to port #55 to MarkItDown 0.1.X`，2025 年） | **不引進**。屬未完成的 OneNote 試驗草稿，長期無更新，不具備可用度。 |
| `upstream/zip_formats` | 僅 1 個 commit `f17bc21`（`If files use zip packaging, be smarter about inspecting their types.`） | **不引進**。ZIP 格式偵測邏輯已在上游 `main` 的 `ZipConverter` 具備等效實現。 |
| `upstream/gagb/add-github-issue-conversion` | 社群貢獻者分支，新增直接自 GitHub URL 抓取 Issue/PR 轉為 Markdown 的功能 | **不引進**。屬於特定平台的外部 HTTP 抓取外掛，未經微軟審查進 `main`，非核心文件轉換範疇。 |
| `upstream/joshbradley/add-file-input-support` | 早期分支，嘗試替轉換器加入多型 file input wrapper | **不引進**。其概念已在上游 `convert_stream()` 與 `StreamInfo` 架構中標準化吸收。 |
| `upstream/kennyzhang/add-file-object-support` | 早期分支，嘗試支援檔案物件與串流 | **不引進**。同上，已由上游現行架構覆蓋。 |

**分支追蹤策略**：本 fork **唯一長期跟隨分支為 `upstream/main`**。其餘分支均為未完成草稿或歷史產物，日常 `git fetch upstream main` 即可，不拉取其他遠端分支。

---

### 二、上游 PR 盤點：分類評估原則（共 317 筆）

317 個 open PRs **全部** 基於 `main` 提交。
本 fork 的審查單位為 **`main` 上的 commit**，原則上不提前 cherry-pick 尚未合併的 open PR，避免破壞上游純淨度或引入尚在變動的程式碼。

代表性 PR 分類評估結果如下：

| 類別 | 代表性 PR 編號與摘要 | 對本 fork 的意義與本輪結論 |
|---|---|---|
| **A. Windows 相容性與編碼** | `#2175`（stdout Unicode 轉發）、`#1864`（stdout reconfigure）、`#1955`（file URI non-ASCII）、`#1573`（UNC path 防護） | **等進 main**。微軟官方已於近期（2026-09-10）陸續合併 UNC 路徑防護（`e99a726`）與 Windows 測試矩陣（`73a26da`、`9480644`）。此外，本 fork 的 `dev_check.ps1` 與維護環境已全面強制 `PYTHONUTF8=1`，本機 gate 運作正常。待上游官方審查通過進 `main` 後再由 commit 追蹤同步。 |
| **B. 表格與 Pipe 字元轉義** | `#2441`（HTML 表格 pipe）、`#2439`（HTML 表格 pipe）、`#2437`（XLSX 表格 pipe） | **不提前引進**。Issue `#2436` 與 `#2438` 提出表格內含有 `|` 會破壞 Markdown 表格語法。社群目前有多個競合 PR，微軟尚未定案。此時 cherry-pick 容易在未來合併時產生嚴重衝突，維持上游追蹤。 |
| **C. MCP 模組與輕量依賴** | `#2448`（MCP 轉譯器改為 opt-in，對應 Issue `#2440`）、`#2202`（MCP file output）、`#2183`（MCP stdio 容錯） | **不提前引進**。解決 ARM64 或輕量容器環境下強制安裝 heavy dependencies 的問題。本 fork 維護門禁已獨立（不安裝產品 heavy optional dependencies），待上游官方重構完成。 |
| **D. 格式轉換細部修復** | `#2457`（DOCX numbering 修復）、`#2456`（XLSX 隱藏工作表篩選）、`#2455`（Doc-Intel stdin）、`#2451`（PDF 頁面分隔標記）、`#2450`（CSV 空行效能）、`#2445`（DOCX 方程式） | **不提前引進**。屬上游格式轉換器細部修復，不影響本 fork 維護骨架與文件。 |
| **E. 新格式擴充與重構** | `#2206` / `#1503`（EML 郵件）、`#2151`（RTF 轉換）、`#2112`（DICOM 醫療影像）、`#2161`（TwelveLabs 影片）、`#1309`（Async 重構） | **不引進**。擴展龐大相依套件與非核心格式，由上游官方決定是否納入產品矩陣。 |

---

### 三、上游 Issue 盤點：分類清冊（共 317 筆）

317 個 open Issues 大致分為四大維度：

| Issue 分類 | 代表性案例 | 本 fork 處置與狀態 |
|---|---|---|
| **Windows 部署與使用** | `#2106`（Win11 使用方式）、`#1289`（Windows 安裝說明）、`#1216`（Win 下安裝）、`#204`（路徑問題） | **已由本 fork 解決**。非上游程式缺陷，而是缺乏 Windows-first 原生指引。本 fork 提供繁中 `README.md`、`docs/DEVELOPMENT.md` 與一鍵啟動腳本 `tools\bootstrap_dev.ps1`，本機環境立即可用。 |
| **控制台編碼問題** | `#1802`（charmap codec error）、`#1788`、`#240`、`#227`（GBK / CP950 解碼錯誤） | **已在本 fork 硬化**。本 fork 之 `tools\dev_check.ps1` 與工作流程已明確注入 `$env:PYTHONUTF8 = "1"` 與 `$env:PYTHONIOENCODING = "utf-8"`。使用者端於文檔中提供設定指引。 |
| **表格與轉換缺陷** | `#2436` / `#2438`（表格內含 pipe 字元破損）、`#2449`（CSV 開頭空行轉換緩慢）、`#2400`（XLSX showZeroes 視圖例外）、`#2383` / `#2382`（DOCX 多圖 OCR 標記覆蓋） | **記錄追蹤**。屬核心產品缺陷，已有社群 PR 在上游排隊審查中。不私自 patch，維持與上游官方代碼一致性。 |
| **MCP 與代理人整合** | `#2440`（ARM64 強裝全相依性破損）、`#2365`（Copilot CLI 連線例外）、`#2386`（Autonomous Agents 提案） | **記錄追蹤**。持續觀察微軟對 MCP 伺服器的架構決策。 |

---

### 四、防重複評估機制（Watermark & Incremental Strategy）

為避免每次巡檢重複評估既有 317 筆 Issues 與 PRs，本專案實施嚴格的水位線（Watermark）機制：

1. **基準水位鎖定**：
   - Commit 水位：`9480644d9c3b7397b9bf0156f858fa3a5aad7d2c`（短 SHA `9480644`）
   - PR 水位：`2457`
   - Issue 水位：`2457`
   - 記錄於 [`tools/upstream_baseline.json`](../tools/upstream_baseline.json)。

2. **增量巡檢機制**：
   - 每次執行 `tools/check_upstream_updates.py` 或 GitHub Actions 每週排程時，檢查器會自動過濾 `number <= watermark` 的項目。
   - 只有編號大於 **#2457** 的新開 PR / Issue，或 `main` 上高於 `9480644` 的新 Commit，才會出現在待審報告中。
   - 當新項目被審查完畢並於 `docs/DECISIONS.md` 記錄結論後，再遞增更新 baseline 水位。
