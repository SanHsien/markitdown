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

## 2026-09-11：依賴新鮮度涵蓋維護與產品清單（R-07 擴充）

**決定**：`tools/check_dependency_freshness.py` 檢查 `requirements-dev.txt`、`requirements.txt` 與 `requirements-all.txt`（共 23 項依賴）。各套件 `pyproject.toml` 的依賴同時由 Dependabot 追蹤。

**理由**：維護工具（pytest, ruff）確保開發門禁健康；產品核心與全格式選配依賴透過 freshness-hold 明確記錄上游相容下限與 Python 3.14 調整原因，避免版本脫節。

## 2026-09-11：上游檢查涵蓋 Commit、PR 與 Issue 三面向

**決定**：`check_upstream_updates.py` 以 `--state all` 收集上游 PR 與 Issue，並追蹤 Commit SHA。`gh` 失敗時 fail closed（exit 2）。

**理由**：未合併即關閉的 PR 與待處理的 Issue 同樣可能揭露重要缺陷或需求。排程報告必須確保「未檢查」與「沒有新變更」截然分明。

## 2026-09-11：日常直接推 main

**決定**：日常維護修改在本機跑 `tools\dev_check.ps1` 後直接推 `origin/main`。Dependabot 與外部貢獻仍走 PR，合併前讀 diff。

**理由**：對齊 SanHsien 體系其他維護 fork 的治理規範。

## 2026-09-11：上游分支、PR 與 Issue 首次盤點結論（不提前引用未合併產品 PR，聚焦 Windows 維護）

**決定**：
1. **上游分支**：全部不引用。`upstream/v0.0.X`（歷史舊線）、`upstream/onenote`（停滯草稿）、`upstream/zip_formats` 與各貢獻者功能分支均不具備即時投產價值。本 fork 唯一長期跟隨分支為 `upstream/main`。
2. **上游 Open PRs（317 筆）**：全部暫不提前引入（no cherry-pick）。等待微軟官方審查通過合併進 `main` 隨 commit 抵達再同步；以避免覆蓋 fork 維護結構與產生不成熟的 API 衝突。
3. **上游 Open Issues（317 筆）**：完成分類盤點。Windows 部署問題已由本 fork 的 Windows gate 與繁中文件解決；表格 pipe 與 docx numbering 等產品缺陷維持上游追蹤。
4. **水位鎖定**：`tools/upstream_baseline.json` 鎖定 PR `#2457` 與 Issue `#2457`。

**理由**：
- 逐筆 cherry-pick 未經微軟審查定案的 PR，容易在未來上游改版時引發重複衝突與相容性破壞。
- 盤點後的非 main 分支均為舊版或停滯草稿。
- 水位鎖定在 `#2457`，確保增量檢查不會再次處理歷史 317 筆舊項目，達成「一次評估，之後只看增量」。

## 2026-09-11：版本採獨立自主維護（升為 0.2.0）

**決定**：MarkItDown 主套件版本自上游 `0.1.8b1` 升至 `0.2.0`，並建立 `v0.2.0` Git Tag。本 fork 版本由維護者自主管理，與上游版本脫鉤。

**理由**：
- 本 fork 已完成 Windows 11 原生工程骨架、繁中雙語文檔、全格式選配依賴引進，以及相容性修復，具備獨立里程碑價值。
- 上游若有新版本發佈，由維護者在每週/每月上游同步審查時依 diff 自行評估整合，並在代碼合併時保留自主版本號。


## 2026-09-30：第二輪上游審查（commit 至 b8f79c5、PR 至 #2566、issue 至 #2567）

本 fork 歷史已壓縮、與上游無共同祖先，採 `cherry-pick -x`。基準代表已審查，不代表全部合併。本輪：14 個 commit、83 筆 PR、23 筆 issue。

### commit 軸（14 筆）

- **採用（8 筆，cherry-pick -x 無衝突；`tools\test_product.ps1` 901 passed／5 skipped）**：#2462 Outlook MSG 日文 code page（CJK 類）、`f0c5d01` 與 #2464 CSV 空白列／pipe 跳脫效能、#2466 charset 偵測不切斷 UTF-8 字元（CJK 類）、#2467 docx 樣式修復保留 namespace、#2469 YouTube 無內容時回退 HTML、#2477 保留空白底線、#2476 圖片轉換器在 LLM client 失敗時擲錯（僅採程式碼與測試；README 一段與本 fork 繁中 README 衝突，保留本 fork 版本）。
- **採用待辦（adoption pending）**：#2506 OCR 轉換器改用核心管線（重構，牽動 markitdown-ocr 多檔，本機無 LLM／OCR 後端可驗證；觸發條件：本 fork 需要 OCR 修正時）；`d51937d` #2407 youtube-transcript-api 升至 >=1.2.3（依賴約束交由本 fork 的依賴新鮮度政策決定）。
- **不適用**：#2459、#2460 上游 ARM CI；#2490、#2545 上游版本 bump（本 fork 版本自主，見 2026-09-11 條目）。

### PR 軸（83 筆，#2458 至 #2566）

- MERGED 12 筆：7 筆採用（#2462、#2464、#2466、#2467、#2469、#2476、#2477）、2 筆 CI 不適用（#2459、#2460）、2 筆版本 bump 不適用（#2490、#2545）、1 筆待辦（#2506）。
- OPEN 67 筆：不 fork-ahead（上游尚未合併，本 fork 政策見 2026-09-11 條目）。涵蓋 HTML／XLSX／DOCX／PPTX／ipynb／RSS／EPUB／PDF 轉換修正、新功能（YAML、XMind、Claude OCR 後端）與效能項。CJK 或 Windows 相關者觸發條件：上游合併後隨 commit 軸抵達——#2541（Outlook MSG UTF-16 NUL）、#2543（quoted charset）、#2517（CSV 分隔符號）、#2539（阿拉伯文 RTL，非本 fork 語系）。
- CLOSED 未合併 4 筆：#2494（XMind，被 #2495 取代）、#2505（srcset）、#2512（圖片保留 PDF 轉換）、#2531（heading 夾限，被 #2555 取代）。無 Windows-first 或 CJK 缺陷，不採用。

### issue 軸（23 筆，#2461 至 #2567）

- 16 筆對應上述 OPEN PR 的缺陷（RSS、XLSX、HTML、PPTX、DOCX、code fence、PDF、OCR），隨 PR 合併後抵達。
- #2474 對應 #2475（OPEN）；#2560、#2565 PDF／OCR 缺陷，待上游修正。
- 不適用：#2487、#2542、#2551、#2561、#2567（無內容或非本專案問題）、#2544（垃圾推廣訊息）。
