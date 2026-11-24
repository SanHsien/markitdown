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

## 2026-10-25：第三輪上游審查（commit 至 7482c09、PR 至 #2755、issue 至 #2744）

本輪：20 個 commit、144 筆 PR、39 筆 issue。除 #2620 為手動移植外，全部 `cherry-pick -x`；`tools\test_product.ps1 -AllPackages` 等價測試（Linux 雲端，Python 3.13）1312 passed／12 skipped，僅 `test_speech_transcription`、`test_markitdown_remote` 因沙箱無對外網路失敗。

### commit 軸（20 筆）

- **採用（18 筆）**：#1511、#1850、#1656（`sys.stdout.encoding` 為 None 的 CLI 輸出，Windows 重導向情境）、#1295、#1510、#1919、#2458、#2579、#2586、#2588、#2592、#2594、#2597、#2601（測試整併與真實 fixture）、#2722（magika `>=0.6.1,<2`，對應 issue #2719）、#2729（mammoth `>=1.12.2,<2`，對應 issue #2646）、#2730（certifi CA 下限）、#1913（Doc-Intel 模型／features／query fields）。
- **部分採用**：#2731 只採產品程式碼的 Black 格式與 markitdown-ocr `Pillow>=12.1.1`；不採 `.github/actions/build-arm-cryptography`、`.github/constraints.txt`、`.pre-commit-config.yaml`（上游 ARM／pre-commit CI，本 fork 已移除，見 R-08／R-09），以及 `tests.yml` 的 ARM 步驟。#2586 在 `tests.yml` 加的 Linux 專用 apt-get 步驟同樣移除（`tests.yml` 只在 `microsoft/markitdown` 執行，且本 fork 為純 Windows，見 R-09）。其 dependabot 變更以本 fork 格式重做：補上 `markitdown-ocr`、`markitdown-sample-plugin` 兩個套件目錄。
- **不適用**：#2733 版本 bump（本 fork 版本自主）。
- **2026-09-30 待辦的 #2506 已採用**：觸發條件成立——上游 #2579／#2588 的整併測試直接依賴 #2506 的 `_xlsx_images`／`docx/_images` 與 OCR 繼承測試，不採就無法再同步上游測試。
- **#1913 README**：英文段落併進 `README.en.md`。繁中 `README.md` 是精簡入口、本來就不含 Doc-Intel 細節，不翻譯；順手把 `result.text_content`（已棄用）改成 `result.markdown`（同上游 #2591 的做法）。
- **依賴清單同步**：`requirements.txt` 加 `certifi`、magika 改 `>=0.6.1,<2`；`requirements-all.txt` mammoth 改 `>=1.12.2,<2`，並補上 markitdown-ocr 原本漏列的 `PyMuPDF>=1.24.0,<2`、`Pillow>=12.1.1`。三個需求檔合計 29 項（dev 2、核心 7、全套 20）。都是跟隨上游宣告，不是為了消紅燈調下限。

### PR 軸（144 筆，#2568 至 #2755）

狀態以 `refs/pull/*/merge` 是否存在判斷（無 merge ref = 已關閉或有衝突）。

- **MERGED 12 筆**：即上述 commit（#2579、#2586、#2588、#2592、#2594、#2597、#2601、#2722、#2729、#2730、#2731、#2733）。
- **例外移植 4 筆 OPEN PR**（先在本 fork 重現缺陷、PR 自帶測試）：
  - #2674：短的非 ASCII UTF-8 文字被 charset 偵測誤判為 UTF-16 而變亂碼（`"ok ✓"` → `"潫⃢鲓"`）。CJK／符號文字直接受害。
  - #2742：宣告 charset 時 UTF-8 BOM 會留在 Markdown 開頭，讓 `# 標題` 不再是標題。Windows 工具（PowerShell 5 `Out-File -Encoding utf8` 等）常寫 BOM。
  - #2738：Unicode MSG 字串流尾端的 NUL 被 `strip()` 保留。Windows Outlook 匯出、與 2026-09-30 記錄的 #2541 同類。
  - #2620：音訊大寫副檔名（`.MP3`／`.WAV`）通過 `accepts()` 卻跳過轉譯。Windows 檔名常見大寫；只移植邏輯與測試，不帶上游 PR 的整檔換行改寫。
  - 理由：Windows-first、繁中使用者會直接碰到，修正小且自帶測試。觸發條件：上游合併（或以不同做法合併）這些 PR 時，以上游版本為準重新 cherry-pick，衝突時採上游。
  - **本機複審（2026-10-25，Windows 11、Python 3.14.9）**：`tools/test_product.ps1 -AllPackages` 1323 passed／3 skipped，0 失敗（含四筆移植自帶的測試與先前雲端因無網路失敗的兩項）。四筆上游仍為 OPEN；缺陷已在本 fork 重現且為純邏輯修正（charset 判斷、BOM 剝除、NUL 剝除、副檔名大小寫），沒有套用上游 diff 的相依問題。結論：保留，不 revert。這不改變「其他 OPEN PR 不 fork-ahead」政策，只是四筆小修正的例外，不涉產品方向。
- **其他 OPEN 116 筆**：維持 2026-09-11 的不 fork-ahead 政策，等上游合併後隨 commit 軸抵達。值得注意者與觸發條件：
  - #2621／#2622（`convert_uri` SSRF 目的地政策）：安全性相關，但牽動 MCP 與 URI 擷取行為，屬產品取捨。觸發條件：上游合併，或本 fork 對外提供 MCP HTTP 服務時。
  - #2679／#2723（cp1252 偵測，issue #2678）：可能影響 CJK 舊碼頁偵測。觸發條件：上游合併後跑 CJK charset 測試再採。
  - #2754（加密 Office 文件錯誤訊息）、#2628（串流緩衝）、#2673（CLI MIME 參數）：一般修正，等上游合併。
  - 新格式／功能（#2676 MHTML、#2677 SRT、#2707 ODF、#2700 CLI LLM 選項、#2710、#2739、#2751 等）：等上游決定。
- **無 merge ref 12 筆**：#2568、#2599、#2630、#2631、#2632、#2635、#2636、#2647、#2656、#2699、#2720、#2748。多為同題重複 PR（已有其他 OPEN PR 或已被 #2722／#2729 取代），#2748（antiword `.doc`）需外部執行檔、非 Windows 原生。不採用。

### issue 軸（39 筆，#2569 至 #2744）

- **已由本輪修正**：#2646（mammoth）、#2719（magika）。
- **對應 OPEN PR、隨上游合併抵達**：#2569、#2571、#2573、#2580、#2610、#2642、#2644、#2667、#2678、#2688、#2690、#2701、#2724、#2728、#2743、#2744。
- **不適用**：#2581（VS Code MCP gallery 版本，上游發行管道）。
- **觸發條件**：#2740（Python 3.15）——上游 CI 加入 3.15 時，本 fork `ci.yml` 矩陣同步加入。
- **無內容或垃圾**：#2582、#2583、#2584、#2604、#2613、#2617、#2624、#2641、#2671、#2680、#2683、#2684、#2695、#2703、#2705、#2713、#2716、#2735、#2741。

### 依賴新鮮度

- ruff 0.17.2：tools 的 E9+F gate 全綠，`>=0.16` 已涵蓋，記入 `.github/dependency-deferrals.json`（`deferredLatest: 0.17.2`）。

### 同日補審（PR 至 #2765、issue 至 #2762）

推上 main 後 `Upstream check` 再列出 9 筆 PR、1 筆 issue（commit 軸無新增）。全部 OPEN、不 fork-ahead：

- #2756（ZIP 無 UTF-8 旗標的非 ASCII 檔名）：缺陷存在（目前以 cp437 顯示成亂碼），但 PR 依 charset_normalizer 猜碼，短的 Big5（cp950）檔名會被誤判成 `shift_jis_2004`：「臺灣報告.pdf」解成「ｻOﾆWｳ茈i.pdf」（「會議紀錄.docx」則正確）。對繁中 Windows 使用者不夠好，不採。觸發條件：上游合併時，先補 cp950 檔名測試，通過才採；或本 fork 改成優先試 `locale.getpreferredencoding()`／`metadata_encoding` 的版本。
- #2757（OMML 分隔符多參數，issue #2573，同題 #2574／#2636／#2654，#2665 部分重疊）、#2758（PPTX 圖表缺值顯示 None，同題 #2632／#2655／#2657）、#2760（方程式 LaTeX 被 Markdown 跳脫，issue #2744，同題 #2745／#2755）：同題重複，等上游擇一合併。
- #2759（PPTX 段落空行）、#2761（HTML 巢狀表格）、#2763（ipynb 字串 source 標題，對應 issue #2762）、#2764（XLSX 文件）、#2765（試算表空格 NaN）：一般產品修正，等上游合併。

## 2026-10-26：深度品質掃描（fork 自家程式）

修了四個維護工具缺陷（各有先失敗的重現測試）：`check_links` 在 Windows 不分大小寫而放行大小寫錯的連結、`check_links` 把連結標題算進路徑、依賴延後清單與去重沒做 PEP 503 正規化、`requirements-all.txt` 缺 hatch-test 額外依賴 `openai`／`pyyaml`。

觀察清單（不改，上游或影響極小）：

- 只含 BOM 加三個以內 ASCII 字元的 `.md` 檔（例如 `﻿# H`）：magika 對極短內容判不出類型，沒有 charset，`PlainTextConverter` 退回 charset_normalizer 而誤判成 Shift-JIS 類編碼，輸出亂碼。四個字元以上正常。觸發條件：實際遇到極短 BOM 檔再處理（可在無 charset 時先試嚴格 UTF-8）。
- `check_links` 會檢查程式碼區塊裡的範例連結；目前維護文件沒有受害者。
- `_strip_terminators` 對 `abc\x00 `（NUL 後接空白）不會去掉 NUL；常見寫入端只補 NUL，不處理。

## 2026-10-26（第二次補審）：上游 PR #2766–#2775

Commit 軸無新增（上游 `main` 仍是 `7482c09`），issue 軸無新增（仍 `#2762`）。新增 10 筆 PR，全部以 `git fetch <upstream> refs/pull/<n>/head` 取**目前的 head** 並確認與 `gh pr view` 的 `headRefOid` 相同後才讀 diff；對 10 筆的新增行、commit 訊息、PR 本文、留言與 review 掃零寬／雙向控制字元、HTML 註解與控制碼：新增行與 commit 訊息命中 0；本文與留言只有 #2768、#2770、#2773 上 CLA 機器人的 `<!-- Policy app identification ... -->` 標記，其餘無任何藏起來的內容。**全部不採用**，維持 2026-09-11 起的「OPEN 的上游 PR 不 fork-ahead」政策，唯一例外類別（Windows-first／CJK 且修正小、自帶測試）沒有命中。

### 四筆真實修正：缺陷在本 fork 都重現，但不是例外類別

重現方式：Windows 11、Python 3.14.9、本 fork `origin/main` 的 `packages/markitdown/src`，各依賴為 `requirements-all.txt`。上游這四筆的 merge-base 都是 `7482c09`（即本 fork 的 baseline），所以本 fork 對應的檔案與 PR 的 base 逐位元組相同。

| PR（對應 issue） | 本 fork 重現結果 | 結論與觸發條件 |
| --- | --- | --- |
| #2766（XLSX 錯誤值，issue #2728；+64／-4，2 檔） | 含 `#DIV/0!` 儲存格的活頁簿轉成 `\| e \| NaN \|`，與真正空白格無法區分 | 缺陷存在，影響是輸出把錯誤值當成缺值；非 Windows／CJK 專屬。做法是 pandas 轉 HTML 後用 BeautifulSoup 重解析並以 `rows[cell.row - 1][cell.column - 1]` 回填，位置推算依賴 pandas 與 openpyxl 的列欄對齊，還在 review 中（`rahul05ranjan` 留言）。觸發條件：上游合併，之後隨 commit 軸抵達並以上游版本為準。 |
| #2768（ipynb `source` 為字串，issue #2762；+57／-1，2 檔） | `source` 為字串的 notebook：`title` 為 `None`，內文仍正確（`'# My Title\nhello'`） | 缺陷存在，只掉標題；非例外類別。觸發條件：上游合併。 |
| #2774（RSS 1.0／RDF；+136／-10，2 檔） | `.rdf` 的 RSS 1.0 輸入原樣回傳 XML（前綴 `<?xml ... <rdf:RDF`），沒有轉換 | 是新增格式支援，不是回歸；非例外類別。觸發條件：上游合併，或本 fork 的使用者實際餵 RSS 1.0 來源。 |
| #2775（data URI 片段，issue #2690；+17／0，2 檔） | `parse_data_uri("data:text/plain,Hello#section")` 回 `b'Hello#section'`；base64 版 `...SGVsbG8h#AAAA` 回 `b'Hello!\x00\x00\x00'` | 缺陷存在且 base64 版會多出 NUL 位元組，但需要輸入端刻意帶 `#` 片段；非例外類別。與 #2621／#2622（`convert_uri` 目的地政策）同屬 URI 輸入面，等上游一起決定。觸發條件：上游合併，或本 fork 開始處理來源不明的 data URI。 |

四筆都已有上游測試，上游合併後 cherry-pick 的成本只有一個 commit，所以先不分叉；這與 2026-10-25 例外移植的四筆（charset、BOM、NUL、副檔名大小寫）的差別是：那四筆是 Windows 工具與繁中文字直接會碰到的輸出，這四筆不是。

### 六筆無產品價值（雜訊或重送）

- #2769（CLOSED 未合併）：標題是 `feat(doc-intel): expose models, features, query fields, and structure…`，本文是 #1913 的 squash 訊息。它的 merge-base 是較舊的 `21d9c1d`，`git diff refs/upstream-check/main refs/upstream-check/pr/2769` 只剩 `README.md` 末尾 3 行（`!!!!!!!!HELL0 W0RLD!!!!!!!`、`ejdejjnj`），也就是產品內容與上游 `main` 已有的 #1913（`7482c09`，本 fork 2026-10-25 已採用）相同，只多了垃圾文字。無新內容。
- #2767（CLOSED，README 殘留 `<<<<<<< HEAD` 衝突標記與亂碼）、#2772（CLOSED，把 README 簡介換成 "very useful tool that I can use"）、#2770（OPEN，刪 README 106 行）、#2773（OPEN，刪 README 52 行）：README 破壞性改動，本 fork 有自己的繁中／英文 README，不適用。
- #2771（OPEN）：把 `SECURITY.md` 的 MSRC 回報連結換成字串 `777`。這是上游的安全回報管道被破壞，屬破壞行為；本 fork 的 `SECURITY.md` 是自己的（GitHub Security Advisories，只在上游核心問題才指向 MSRC），不受影響，不採用。

水位：PR `#2765`→`#2775`；Issue 不變（`#2762`）；Commit 不變（`7482c09`）。

## 2026-10-28（第三次補審）：上游 PR #2776–#2780

Commit 軸無新增（上游 `main` 仍是 `7482c09`），issue 軸無新增（仍 `#2762`）。新增 5 筆 PR，全部 OPEN、未合併。審查方式與前一輪相同：`git fetch <upstream> refs/pull/<n>/head` 取**目前的 head**，確認與 `gh pr view` 的 `headRefOid` 相同後才讀 diff，五筆的 merge-base 都是 `7482c09`（本 fork 的 baseline），所以本 fork 對應檔案與 PR 的 base 逐位元組相同（`git diff upstream/main HEAD -- <三個 converter>` 無差異）。對五筆的新增行掃零寬／雙向控制字元、`\S\s{40,}\S` 空白夾內容、單行超過 200 字、`eval`／`base64`／長 hex、HTML 註解與控制碼：命中 0；PR 本文與留言只有 CLA 同意與一句 "Looks go to me"，無隱藏內容。**全部不採用**，維持「OPEN 的上游 PR 不 fork-ahead」政策；唯一例外類別（Windows-first／CJK，修正小、自帶測試）沒有命中。

重現方式：Windows 11、Python 3.14.9、本 fork `origin/main` 的 `packages/markitdown/src`，依賴為 `requirements-all.txt`（pptx 1.0.2）。五個缺陷在本 fork 都重現：

| PR（對應 issue） | 本 fork 重現結果與對應位置 | 結論與觸發條件 |
| --- | --- | --- |
| #2776（XY／氣泡圖資料點被丟掉；+82／-0，2 檔） | XY_SCATTER 圖表轉成 `\| Category \| Revenue \|` 加分隔線就結束，3 個資料點全部消失（`_pptx_converter.py:336` 以 `plots[0].categories` 建列，XY 圖沒有分類軸）。 | 缺陷存在，但只影響 PPTX 內的散佈圖與氣泡圖；PR 自述用資料點序號當列標籤，不是 x 值，作者也承認真正的 x 值要碰私有 XML。非例外類別。觸發條件：上游合併（以上游版本為準），或本 fork 使用者實際轉含散佈圖的簡報。與 2026-10-26 記錄的 #2758（PPTX 圖表缺值，同在 `_convert_chart_to_markdown`）會改同一段，等上游一起定案。 |
| #2777（ipynb 字串 `source`，issue #2762；+30／-1，2 檔） | `source` 為字串的 notebook：`title` 為 `None`，內文 `'# My Title\nhello'` 正確（`_ipynb_converter.py:79` 對字串逐字元迭代）。 | 缺陷存在，只掉標題。與 #2763、#2768、#2778 四筆同題（同一個 issue #2762），等上游擇一合併。觸發條件：上游合併。 |
| #2778（同上；+72／-1，2 檔） | 同上。 | 同上。補充：這筆新增 `_as_line_list()` 輔助函式並寫兩個測試，是四筆裡最完整的，若日後要例外移植選這筆；現在不移植的理由與 #2768 相同（非 Windows／CJK，只掉標題）。 |
| #2779（PPTX 表格後的下一個形狀被併進表格；+53／-1，2 檔） | 表格後接文字方塊轉成 `\| 1 \| 2 \|\nFollow-up analysis.`，沒有空行，渲染後那句話變成表格列（`_pptx_converter.py:321` 的 `.markdown.strip()` 之後只補一個換行）。 | 缺陷存在，影響是 PPTX 表格後面緊接其他形狀時的 Markdown 結構；非 Windows／CJK 專屬。作法是回傳 `\n\n`，簡單且與圖表路徑一致，但與 #2759（PPTX 段落空行，已記等上游）同屬 PPTX 版面空行語意，等上游一起定案較不會重工。觸發條件：上游合併，或本 fork 使用者回報簡報表格輸出被吞。 |
| #2780（無 entry 的 Atom feed；+48／-3，2 檔） | 只有 title／subtitle／author 的合法 Atom feed，不論 `.atom` 或 `.xml` 都原樣回傳 XML，沒有轉換（`_rss_converter.py:136` 要求至少一個 `<entry>`）。 | 缺陷存在，但空的 Atom feed 是邊角輸入，RFC 4287 允許但少見。非例外類別。與 #2774（RSS 1.0）同屬 `RssConverter` 辨識範圍調整。觸發條件：上游合併，或本 fork 使用者實際餵空 feed。 |

五筆各只動 1 個 converter 加 1 個測試檔，上游合併後 cherry-pick 的成本是一個 commit；這與 2026-10-25 例外移植的四筆（charset、BOM、NUL、副檔名大小寫）的差別是：那四筆是 Windows 工具與繁中文字直接會碰到的輸出，這五筆不是。

水位：PR `#2775`→`#2780`；Issue 不變（`#2762`）；Commit 不變（`7482c09`）。

## 2026-11-02（第四次審查）：上游 PR #2782–#2810、issue #2781–#2806

Commit 軸無新增（上游 `main` 仍是 `7482c09`）。新增 17 筆 PR（全部 OPEN、未合併）與 12 筆 issue。審查方式：`gh pr diff` 取**目前**的 head（下表 head 欄），對新增行掃 `\S\s{40,}\S` 空白夾內容、`eval(`／`new Function`／`globalThis`、100 字元以上的 base64／hex 串、零寬與雙向控制字元、控制碼：17 筆命中 0（#2803、#2809 各有超過 200 字元的行，內容是 CLI help 字串與 SKILL.md front matter description，非隱藏程式）。

### 採用 1 筆（Windows／CJK 例外類別，移植做法不是 diff）

- **#2803**（head `c03c939`，+424／-292，5 檔；修 issue #1219）：`markitdown input.docx > out.md` 在 stdout 為 cp950／cp1252／ascii 時，目前的 `_handle_output` 以 `errors="replace"` 把無法編碼的字元換成 `?`（本 fork `__main__.py` 的 else 分支，`encoding = sys.stdout.encoding or "utf-8"`），繁中文字直接變 `?`，而 `-o` 路徑本來就寫 UTF-8，兩條路徑不一致。缺陷在本 fork 重現（還原修正後 `test_redirected_stdout_preserves_unicode` 失敗，見下）。**只移植設計**：stdout 有 `buffer` 且非 tty 時，flush 後以 UTF-8 寫入 `buffer`；互動終端與純文字串流維持原行為。**沒照抄**：上游同一個 PR 把 CLI 參數宣告與驗證拆成 `_cli_args.py`／`_cli_options.py` 兩個私有模組（約 700 行搬移），與本缺陷無關，且會讓之後 cherry-pick 上游 `__main__.py` 的修正全部衝突，所以不搬。測試移植 4 個（cp950／cp1252／ascii 重導向、互動終端沿用終端編碼、純文字串流）；cp950 為本 fork 加的案例（繁中 Windows 的實際碼頁）。與 2026-10-25 採用的 #1656（`sys.stdout.encoding` 為 None）同一函式、互補。觸發條件：上游合併 #2803 或以不同做法修 #1219 時，以上游版本為準重新對齊，衝突時採上游。
  - **2026-11-21 更正**：上句「繁中文字直接變 `?`」不正確。實測 cp950 能編碼一般繁中字（`中文測試`、`’“”` 原樣保留），只有碼頁外的字元變 `?`（`é`、emoji、`堃` 等 Big5 外的字）。而「非 tty 一律 UTF-8」讓 PowerShell 擷取與接 cmdlet 變亂碼，規則已改寫，見下方 2026-11-21 條目。

### 不採用（維持「OPEN 的上游 PR 不 fork-ahead」政策；非 Windows／CJK 專屬）

| PR（head） | 內容與本 fork 對應位置 | 結論與觸發條件 |
| --- | --- | --- |
| #2782（`aa1b0da`，+25／-2）、issue #2781 | 無 entry 的合法 Atom feed 被拒；`_rss_converter.py:136` 仍要求至少一個 `<entry>`。 | 與 2026-10-28 記錄的 #2780 同題（同一個 `RssConverter` 辨識條件），等上游擇一合併。 |
| #2783（`99dd030`，+12，README） | 只加 shell 函式範例到上游英文 README。 | 文件，不適用。 |
| #2785（`be177df`，+4／-4） | `actions/setup-python` 7.0.0 → 7.1.0，改 `pre-commit.yml`、`tests.yml`。 | 這兩個 workflow 在本 fork 只對 `microsoft/markitdown` 執行；本 fork 以 SHA 釘版（`.github/workflows/*.yml` 現為 v7.0.0 的 `5fda3b9`），升級走本 fork 自己的 Dependabot。不適用。 |
| #2787（`f9da749`，+27／-11） | PDF 文字閱讀順序 fallback；`_pdf_converter.py:562-584` 的 `extract_text` 路徑。 | 一般產品修正，非 CJK 專屬。等上游合併。 |
| #2788（`95966dd`，+92／-4） | CSV 內字面 HTML／字元參照被轉換。 | 一般修正，等上游合併。 |
| #2794（`34b28fc`，+294／-7） | 音訊轉譯的 ffmpeg 解碼加 timeout 與 protocol whitelist，並附三個 stub ffmpeg 可執行檔。 | 本 fork 的 `_transcribe_audio.py` 沒有 ffmpeg 呼叫（`:19` 只是 warnings 過濾），攻擊面依賴 pydub 內部。測試靠 POSIX stub 可執行檔，Windows 原生跑不了。等上游合併。 |
| #2795（`1348426`，+94／-9）、#2807（`1511970`，+41／-3，issue #2806） | DOCX 數學：單一方程式失敗隔離、未知 limit 函式 fallback；`degHide` 被忽略（`omml.py:307` `do_rad` 不讀 `degHide`）。 | 與 2026-10-25 已記錄的 OMML 同題 PR（#2757 等）屬同一檔案同一區域，等上游一起定案。 |
| #2796（`fd4e545`，+95／-3） | ragged PDF 表格、HTML link/image title 內換行、非正頁寬。 | 一般修正，等上游合併。 |
| #2797（`b2be1d2`，+421／-5） | ZipConverter 資源上限、ExifTool timeout、HTTP 抓取 timeout 與大小上限。 | 安全硬化、牽動 `_markitdown.py` 抓取行為，屬產品取捨，與 #2621／#2622 同類。觸發條件：上游合併，或本 fork 對外提供 MCP HTTP 服務時。 |
| #2801（`a452bcb`，+66／-2） | 新功能：可省略試算表 sheet 標題（`_xlsx_converter.py:152` 目前固定輸出 `## sheet`）。 | 新功能，等上游決定。 |
| #2802（`2de105b`，+34） | 新增 conda 打包 workflow。 | 本 fork 為純 Windows 維護線且不發佈套件，不適用。 |
| #2805（`98945e6`，+75／-10）、#2810（`aaf26e7`，+162／-4）、issue #2804 | ipynb 的 `accepts()` 只檢查 `nbformat` 與 `nbformat_minor` 子字串（`_ipynb_converter.py:38-39`），一般 JSON 提到這兩個字會被吞成空 Markdown。 | 缺陷存在，但兩筆同題（等上游擇一合併），且與 #2763／#2768／#2777／#2778 同為 ipynb 辨識區域。非 Windows／CJK 專屬。 |
| #2808（`de8d7bb`，+112） | HTML／DOCX 表格儲存格內的 `\|` 跳脫（`_markdownify.py` 無表格儲存格跳脫）。 | 一般修正，等上游合併。 |
| #2809（`ed51314`，+56） | 新增 `skills/` 目錄（CLI 與 desktop 兩份 SKILL.md 及 md.sh）。 | 新增上游產品內容，等上游決定；md.sh 為 POSIX shell，Windows 原生不可用。 |

### issue 軸

- #2781、#2804、#2806：各對應上表 PR（#2782、#2805／#2810、#2807），隨上游合併抵達。
- 無內容或垃圾（無重現步驟、只有附檔或與本專案無關）：#2784、#2786、#2790、#2791、#2792、#2793、#2798、#2799、#2800。

水位：PR `#2780`→`#2810`；Issue `#2762`→`#2806`；Commit 不變（`7482c09`）。

## 2026-11-05：Ruff 新鮮度採版本限定延後，保留相容下限

**決定**：將 `.github/dependency-deferrals.json` 的 Ruff `deferredLatest` 由 `0.17.2` 更新為 `0.17.3`（出口 c），保留 `requirements-dev.txt` 的 `ruff>=0.16`。

**理由**：本 repo 宣告相容範圍而非精確釘版，0.17.3 已在範圍內，沒有必須提高下限的相容性需求。[官方發行說明](https://github.com/astral-sh/ruff/releases/tag/0.17.3) 的變更包含預覽規則、UP032 修正、效能及文件調整，未要求更動本 repo 的 E9+F gate；PyPI metadata 的 Python 下限為 3.7，涵蓋本 repo 的 3.10–3.14。使用本機 Ruff 0.17.3、pytest 9.2.0 與 Python 3.14 執行完整 Windows 維護 gate；本次只更新審視版本，不變更產品依賴或 workflow。沙箱無法存取共用 pytest 暫存目錄，先建立 worktree 內的 `.pytest_cache`，再以 `$env:PYTEST_ADDOPTS="--basetemp=.pytest_cache/freshness-20261105"` 執行 `pwsh -NoProfile -File tools/dev_check.ps1`，42 項測試通過。

**重評條件與限制**：PyPI 出現高於 0.17.3 的版本時自動恢復提醒。其餘既有 freshness-hold 維持原裁決；本機 gate 不代表多版本 CI 或遠端 workflow 已轉綠，workflow 另檢查開放中的 Dependabot PR。

## 2026-11-07：Ruff 0.17.4 發行重審，維持版本限定延後與相容下限

**決定**：將 `.github/dependency-deferrals.json` 的 Ruff `deferredLatest` 由 `0.17.3` 更新為 `0.17.4`，保留 `requirements-dev.txt` 的 `ruff>=0.16`。

**理由**：本 repo 宣告相容範圍而非精確釘版，0.17.4 已在範圍內，沒有必須提高下限的相容性需求。[官方發行說明](https://github.com/astral-sh/ruff/releases/tag/0.17.4)（2026-11-05 發布）包含預覽功能（`flake8-logging-format` G004 修正、`tarfile-ignore-zeros-true`）、錯誤修正（分號前的 bare raise、分號後的 match 標識符、BOM 開頭檔案的診斷渲染器 panic、SIM102）、診斷修正 diff 顯示更多不可列印字元、效能調整（含 pyflakes F601/F602）、`__debug__` 屬性寫入的語法錯誤檢查及文件更新，未引入破壞性變更，亦未要求更動本 repo 的 E9+F gate；PyPI metadata 的 Python 下限為 3.7，涵蓋本 repo 的 3.10–3.14。使用本機 Ruff 0.17.3、pytest 9.2.0 執行完整 Windows 維護 gate（`pwsh -NoProfile -File tools/dev_check.ps1`），42 項測試通過，`check_dependency_freshness.py --strict` exit 0；另以 `uvx ruff@0.17.4 check --select E9,F --target-version py310 tools` 實跑 Ruff 0.17.4，結果 All checks passed。另將 `.github/dependency-deferrals.json` 加入 workflow 的 push paths，使 deferral 更新後重跑檢查。

**重評條件與限制**：PyPI 出現高於 0.17.4 的版本時自動恢復提醒。其餘既有 freshness-hold 維持原裁決。

## 2026-11-09（第五次審查）：上游 commit ed17895、PR #2811–#2852、issue #2807–#2850

上游 `main` 自 `7482c09` 推進至 `ed178952a6672abdfd35b5f9e76a80b6cefc086e`（短 SHA `ed17895`，共 3 筆 commit）。新增 31 筆 PR（3 筆 MERGED、3 筆 CLOSED、25 筆 OPEN）與 9 筆 issue。

### commit 軸（3 筆，全部採用）

- **ed17895**（2026-11-07，+55／-1，2 檔，PR #2837）：`fix: match ExifTool directories case-insensitively on Windows`。Windows 原生環境下 `shutil.which` 保留 PATH 拼法（如 `C:\WINDOWS\system32`），與受信任目錄列表（`C:\Windows\System32`）直接比對字串會失敗，導致自動偵測 ExifTool 靜默遺失。採用 `os.path.normcase` 統一大小寫比對；POSIX 系統維持精確大小寫。一併採用上游自帶測試。
- **3ae4f03**（2026-11-06，+33／-3，3 檔，PR #2846）：`Override default SpeechRecognition endpoint (#2846)`。在 `_transcribe_audio.py` 呼叫 `recognize_google` 時明確指定 `endpoint="https://www.google.com/speech-api/v2/recognize"`，避免明文 HTTP 傳輸，並在 `pyproject.toml` 將 `SpeechRecognition` 相容下限升至 `>=3.10.4`。本 fork 同步採用並更新 `requirements-all.txt` 宣告。
- **1dccd83**（2026-11-06，+5／-1，1 檔，PR #2845）：`Clarify hosted service requirements in README (#2845)`。說明圖片說明生成與語音轉文字依賴網路託管服務，並於安全注意事項加註純本機運作指引。已將英文變更併入 `README.en.md` 並翻譯至繁中 `README.md`。

### PR 軸（31 筆，#2811 至 #2852）

審查方式：25 筆 OPEN 逐筆以 `gh pr diff <n> -R microsoft/markitdown` 取**目前**的 head 讀 diff（head 見下），讀前讀後各以 `gh pr view --json headRefOid` 確認 head 沒變（25 筆皆未變）；對新增行、commit 訊息、PR 本文與留言掃零寬／雙向控制字元、`\S\s{40,}\S` 空白夾內容、`eval(`／`new Function`／`globalThis`／`exec(`、100 字元以上的 base64、100 個十六進位字元以上的 hex 串、控制碼與 HTML 註解。新增行命中 0（零寬、雙向、控制碼、空白夾內容、base64、hex、`eval` 類皆 0）；另有三類字面命中，逐一讀過皆非隱藏內容：#2828 有 4 行超過 200 字元（1 行是重生成 `test_docx.md` 的 `python -c` 指令，3 行是測試文件 `test_docx.md` 的 AutoGen 論文摘要文字）；#2818 與 #2843 的新增行含 `<!-- Slide number -->`／`<!-- Hidden slide -->`，是 PPTX 轉換器輸出的標記與其測試斷言。本文與留言只有 #2813、#2822、#2826、#2827、#2828 上 CLA 機器人的 `<!-- Policy app identification ... -->` 標記，其餘無任何藏起來的內容。25 筆都不屬 Windows／CJK 例外類別：#2811／#2813 的 ipynb 驗證順帶去掉 BOM，但主題是頂層 JSON 結構驗證；#2830 的測試含 `café` 與 `中文`，主題是 User-Agent 與傳輸驗證；其餘與 Windows 路徑、碼頁、繁中輸出無關，所以沒有改判。25 筆目前 head：#2811 `6b8f579`、#2812 `05ca764`、#2813 `b128da5`、#2814 `fdef206`、#2818 `2a2b936`、#2821 `52b92e9`、#2822 `ba377c6`、#2823 `003cc2e`、#2824 `9687008`、#2825 `063bc10`、#2826 `b580312`、#2827 `e03b867`、#2828 `7bfc72a`、#2830 `dfdaf85`、#2831 `e7e233b`、#2832 `259c58e`、#2833 `538c2ee`、#2835 `13bfb37`、#2836 `b98a87d`、#2840 `ff7340f`、#2843 `7104ac6`、#2844 `86991af`、#2849 `1485223`、#2851 `6c2d71b`、#2852 `7f657d7`。各筆新增／刪除行數與檔數以 `gh pr list --json additions,deletions,changedFiles` 核對，與下列條目一致。

- **MERGED 3 筆**：即上述 commit（#2837、#2845、#2846），全部採用。
- **CLOSED 未合併 3 筆**：#2838（PDF OCR 數學公式 prompt；+78／-15，4 檔，關閉未合併、無說明）、#2847（ipynb 結構驗證重送，關閉）、#2848（表格 pipe 跳脫重送，關閉）。均不採用。
- **OPEN 未合併 25 筆**：維持「OPEN 的上游 PR 不 fork-ahead」政策，等上游合併後隨 commit 抵達：
  - #2811（+94／-4，2 檔）、#2813（+109／-4，2 檔）：ipynb 頂層 JSON 結構驗證（修 issue #2804），同題競合，等上游擇一合併。
  - #2812（+172／-1，3 檔）：外掛轉換器 CLI 選項，等上游決定。
  - #2814（+94／-2，2 檔）：DOCX OMML radical `degHide`（修 issue #2806），等上游合併。
  - #2818（+47／-0，2 檔）：PPTX 隱藏投影片標記（修 issue #2817），等上游合併。
  - #2821（+35／-1，2 檔）、#2830（+140／-1，3 檔）：HTTP 請求自訂 User-Agent 與傳輸驗證（修 issue #2820），等上游決定。
  - #2822（+2／-2，2 檔）：actions/checkout 5 升 6，本 fork CI 獨立維護且以 SHA 釘版，不適用。
  - #2823（+52／-0，3 檔）：HTML 表格儲存格內 pipe 跳脫，等上游合併。
  - #2824（+82／-4，2 檔）：XLSX/XLS 空白儲存格與 NA 類文字保留，等上游合併。
  - #2825（+112／-1，2 檔）：DOCX OMML n-ary 隱藏極限，等上游合併。
  - #2826（+138／-60，3 檔）：移除 ImageConverter 重複之 LLM caption helper，等上游合併。
  - #2827（+93／-2，2 檔）：略過 PdfConverter 重複之 pdfminer 解析，等上游合併。
  - #2828（+117／-0，3 檔）：新增 test.docx 期望輸出測試，等上游合併。
  - #2831（+2／-5，1 檔）：markitdown-ocr README 移除無效之 CLI 範例，等上游合併。
  - #2832（+139／-1，2 檔）：DOCX 保留腳註連結與格式化定義，等上游合併。
  - #2833（+72／-0，2 檔）：HTML template 元素 inert 隱藏可見度，等上游合併。
  - #2835（+4／-0，1 檔）、#2851（+86／-0，2 檔）：DOCX 無方程式時略過 math XML 往返預處理（修 issue #2834），同題競合，等上游擇一合併。
  - #2836（+112／-8，2 檔）：DOCX 依 package relationships 解析主文件 part，等上游合併。
  - #2840（+116／-23，2 檔）：PPTX 複合圖表保留多 plot 類別資料（修 issue #2839），等上游合併。
  - #2843（+261／-4，2 檔）：PowerPoint 文字保留超連結目標，等上游合併。
  - #2844（+11／-4，5 檔）：Python 3.15 支援（Draft），觸發條件：上游 CI 正式納入後本 fork 同步更新矩陣。
  - #2849（+146／-10，2 檔）：限制 ZIP 解壓縮大小、項目數與巢狀深度，屬產品安全取捨，等上游決定。
  - #2852（+15／-3，2 檔）：XLSX 修復具前綴 sheet views 之 legacy attributes，等上游合併。

### issue 軸（9 筆，#2807 至 #2850）

- #2817（PPTX 隱藏投影片轉換）：對應 PR #2818，等上游合併。
- #2819（تحويل PDF）：無內容或非本專案問題（阿拉伯文標題、無內文）。不適用。
- #2820（URL fetch 缺少 User-Agent 導致 Wikipedia 403）：對應 PR #2821 / #2830，等上游合併。
- #2829（nefro）：無內容或垃圾。不適用。
- #2834（DOCX math 預處理無方程式仍重複解析）：對應 PR #2835 / #2851，等上游合併。
- #2839（PPTX 複合圖表遺漏後續 plot 資料）：對應 PR #2840，等上游合併。
- #2841（trabajo unidad 4）：無內容或作業。不適用。
- #2842（unidad 4）：無內容或作業。不適用。
- #2850（jurnal tugas akhir bab 1 2 3）：學生論文上傳，已關閉。不適用。

水位：PR `#2810`→`#2852`；Issue `#2806`→`#2850`；Commit `7482c09`→`ed17895`（完整 SHA：`ed178952a6672abdfd35b5f9e76a80b6cefc086e`）。

## 2026-11-21：新增 fork 自有產品測試 workflow（`product-tests.yml`）

**決定**：新增 `.github/workflows/product-tests.yml`，在本 fork 實際執行產品測試套件。`push`／`pull_request`（`main`）與手動觸發，權限 `contents: read`，不使用 `pull_request_target`，actions 以與 `ci.yml` 相同的 SHA 釘版。三個 job 對應上游 `tests.yml`，Python 同為 3.10–3.13：

- `core`：`packages/markitdown`，`pipx install hatch` 後 `hatch test -py=<版本>`；`ubuntu-latest` 與 `windows-latest` 各跑一輪。Ubuntu 沿用上游 PR #2586 的 apt 步驟安裝 `exiftool`、`ffmpeg`，否則相關測試只會被跳過。
- `ocr`：`markitdown-ocr`，從本機 checkout 安裝核心與外掛後跑 `pytest`（ubuntu）。
- `mcp`：`markitdown-mcp`，安裝 `markitdown[all]` 與 MCP 後跑 `pytest`（ubuntu）。

**理由**：`tests.yml` 有 `github.repository == 'microsoft/markitdown'` 閘門（2026-09-11 決定），`ci.yml` 只跑維護 gate（compile／ruff／`tools/tests`／連結檢查），所以在此之前產品測試從不在 fork 的 CI 跑，只能在本機跑受影響的檔案。不改 `tests.yml`（上游檔，改它會讓之後 cherry-pick 衝突）；也不把產品依賴塞進 `ci.yml`（維護 gate 刻意只裝 pytest 與 ruff）。

**對「純 Windows」的修正**：2026-09-11 起「所有非 Windows CI 已移除」。本次只在 `product-tests.yml` 加 Ubuntu 作為較快、較便宜的第二訊號；Windows 仍是維護者的主要環境，`core` 在 Windows 跑完整 3.10–3.13。`ci.yml` 維持純 Windows（`test_ci_covers_python_314` 仍斷言它不含 `ubuntu`）。OCR 與 MCP 只跑 Ubuntu，與上游 `tests.yml` 的 Windows 設定不同，Windows 上的這兩個套件仍靠本機 `tools	est_product.ps1 -AllPackages` 驗收。

**實測的坑**：上游 `tests.yml` 的 `hatch test -py=<版本>` 在 Windows 預設 shell（PowerShell）下會被拆成 `-py=3` 與 `.12`，hatch 回報 `No environments were selected`；本 fork 把該 workflow 轉成 `windows-latest` 後從未實際跑過，所以直到本次才暴露。本 workflow 改用 `hatch test --python <版本>`，並有測試禁止 `run:` 行出現 `-py=`。

**限制**：Python 3.14 不在本 workflow 內（上游 `tests.yml` 也沒有），3.14 只有維護 gate。產品測試紅燈要先分辨是否本次改動造成，不能用跳過測試消音。

## 2026-11-21：增量審查（`aa9b84c..c8377f4`）修正

### CLI 重導向輸出編碼改依消費端選擇（F-2；F-3 未驗證）

PowerShell 7 把原生程式的 stdout 一律接成 pipe，`$x = markitdown f`、`markitdown f | Select-String`、`markitdown f > out.md` 三者在 Python 端都是 `GetFileType == FILE_TYPE_PIPE`，無法區分；cmd.exe 的 `>` 則給磁碟檔。PowerShell 擷取與接 cmdlet 時以 `[Console]::OutputEncoding`（主控台輸出碼頁）解碼。規則：

1. 明確指定的 Python I/O 編碼優先：`PYTHONIOENCODING`，或 UTF-8 mode（`PYTHONUTF8=1`／`-X utf8`）。
2. Windows 且 stdout 是 pipe、有主控台：用主控台輸出碼頁（`GetConsoleOutputCP()`；65001 即 UTF-8），碼頁外字元以 `?` 取代。
3. 其他（磁碟檔、沒有主控台、非 Windows）：UTF-8，與 `-o` 相同（保留 #1219 對 cmd.exe `>` 的修正）。

實測（PowerShell 7.7.0，`[Console]::OutputEncoding` = 950，docx 內文 `中文測試 hello`；「舊」為 `c4b726c` 之前，「c4b726c」為改前 HEAD）：

| 情境 | 舊 | c4b726c | 本次 |
| --- | --- | --- | --- |
| `$x = markitdown f.docx` 含 `中文測試` | 是 | 否（亂碼） | 是 |
| `markitdown f.docx \| Select-String 中文測試` | 命中 | 未命中 | 命中 |
| pwsh `markitdown f.docx > out.md` 檔案位元組 | cp950 | UTF-8 | cp950 |
| cmd.exe `markitdown f.docx > out.md` 檔案位元組 | cp950 | UTF-8 | UTF-8 |

`[Console]::OutputEncoding` = 65001 時本次四種情境都是 UTF-8 且讀回正確。取捨：pwsh 的 `>` 回到碼頁輸出（`Get-Content -Encoding 950` 讀回正確，預設 UTF-8 讀回亂碼），因為 Python 端看不出它和擷取的差別；要 UTF-8 檔案用 `-o out.md`，或設 `PYTHONIOENCODING=utf-8`。Windows PowerShell 5.1（`powershell.exe`）在本機呼叫一律卡住，**未驗證**；依其 `>` 先以 OutputEncoding 解碼再寫 UTF-16 的行為推論，本次規則對它也較正確，但沒有實測證據。觸發條件：上游合併 #2803 或以其他做法修 #1219 時，重新比對本規則，與上游衝突時以上游為準並重跑上表。

### OCR plugin 沒有 OCR service 時不解析 XLSX 圖片（F-1、H-1）

`XlsxConverterWithOCR` 在沒有 `ocr_service`（建構參數或呼叫參數皆無）時直接委派給原生 `XlsxConverter`：hook 本來就會對每張圖回 None，所以輸出不變，但不再讀取、也不會因缺圖或斷掉的關聯（`KeyError`）而失敗，也不把所有嵌入圖讀進記憶體。核心 `_XlsxImages` 不改：上游 #2506 的 `test_malformed_image_reference_does_not_become_silent_native_fallback` 刻意讓壞參照在 converter 層丟例外、由 dispatcher 退回內建 converter；上游 `main`（`ed17895`）沒有後續修正。~~有 OCR service 時遇壞圖仍照上游行為（整份退回原生輸出）。~~（2026-11-21 由下一條取代）觸發條件：上游改動 `_xlsx_images.py` 的錯誤處理時，改採上游。

### OCR plugin 有 OCR service 時跳過壞圖、其餘圖片照常 OCR（F-1 後續，fork divergence）

獨立驗收發現：有 `ocr_service` 時，`MarkItDown(enable_builtins=False)` 或直接呼叫 `XlsxConverterWithOCR` 遇到圖片關聯指向不存在的媒體檔（或關聯 id 不存在）仍丟 `KeyError`，沒有內建 converter 可退回，整份活頁簿連表格一起失敗；有內建 converter 時也只是整份退回原生、其他圖片的 OCR 全部消失。做法：核心新增 `XlsxConverter._unreadable_image(reference, error)` hook，`_XlsxImages` 讀圖（關聯查找與 `archive.read`）遇 `KeyError`／`BadZipFile`／`zlib.error` 時呼叫它；**沒覆寫此 hook 的 converter 仍以 `_XlsxImages(workbook_stream)` 原樣呼叫、壞參照照常丟例外**（預設 hook 本身也是 re-raise），上游 #2506 的 `test_malformed_image_reference_does_not_become_silent_native_fallback` 照舊通過。`XlsxConverterWithOCR` 覆寫成發 `RuntimeWarning`（與既有「OCR 回報錯誤就警告並保留原生」慣例一致）後只跳過那張圖，不論有沒有內建 converter 可退回都一樣——上游該測試防的是「靜默」退回，警告不是靜默，且保留的輸出比整份退回多。與上游差異：核心多一個預設等同上游行為的 hook；plugin 行為改為跳過壞圖。測試：`test_broken_image_is_skipped_with_warning_and_other_images_still_ocr[missing-media-part|dangling-relationship]`。觸發條件：上游改動 `_xlsx_images.py` 的錯誤處理或 OCR plugin 的壞圖策略時，改採上游並移除此 hook。

**2026-11-21 補兩個缺口（獨立驗收發現）**：(1) 工作表關聯指向不存在的 drawing part 時，同一 hook 也會被呼叫，跳過整個 drawing、表格照常輸出（原本 `enable_builtins=False`／直接呼叫仍整份 `KeyError`）。(2) 沒有大小上限：200 MB 嵌入圖會整張讀進記憶體（峰值約 449 MB）再送 OCR。`XlsxConverterWithOCR(max_image_bytes=20 MiB)`（預設 `DEFAULT_MAX_IMAGE_BYTES`，`None` 關閉）先看 zip member 宣告的解壓後大小 `file_size`，超過就不讀、經同一 hook 發 RuntimeWarning 並跳過；宣告值未超過時改用 `archive.open()` 每次 64 KiB 分段讀，累計超過上限就放棄。

**更正（2026-11-21，`8d4eded` 的說法錯誤）**：`8d4eded` 只檢查宣告的 `file_size`、之後用 `archive.read()` 整段讀，並宣稱「`zipfile` 讀取以 `file_size` 為上限」。實測：`ZipFile.read()` 會在一次 `decompress` 呼叫裡把整個壓縮內容解開，之後才截到宣告大小——驗收用 300 MB 圖、宣告值偽造成 1000，峰值 616 MB 後才因 CRC 錯誤跳過；本機 64 MB 版本 tracemalloc 峰值 148 MB。現在實際保證的是：每張圖解壓過程最多保留約 `max_image_bytes` 加一個 64 KiB 區塊（加上 zlib 內部緩衝）；宣告值偽造偏小的 member 會在讀到宣告大小時以 CRC 錯誤（`BadZipFile`）結束並跳過，不會整段解開。不保證的是：上限內的圖仍整張讀進記憶體再送 OCR，組合分段時與 OCR 端各再保留一份，所以剛好在上限的圖整體峰值約為上限的 2 倍（驗收實測 20 MiB 上限、峰值約 42 MB）；上限以外的其他 package part（工作表、drawing XML）不受此限。核心 `XlsxConverter._max_image_bytes` 預設 `None`，且只在覆寫 `_unreadable_image` 的路徑生效，基底 converter 與未覆寫的子類別行為仍與上游相同（測試 `test_base_hook_without_skip_override_keeps_upstream_raise`）。測試：`test_missing_drawing_part_warns_and_keeps_tables_without_fallback`、`test_images_over_the_byte_limit_are_skipped_before_reading`、`test_oversized_image_is_never_read_into_memory`（宣告值超限時完全不讀）、`test_forged_declared_size_does_not_decompress_the_whole_member`（偽造宣告值，tracemalloc 峰值須低於 16 MB）、`test_bounded_read_stops_after_limit_plus_one_bytes`、`test_default_byte_limit_is_20_mib_and_none_disables_it`。

### DOCX styles.xml 不是 well-formed 時仍正規化雙刪除線（H-2）

`_pre_process_styles` 嚴格解析失敗時，以 `recover=True` 重試，仍保留 `resolve_entities=False, no_network=True`，取回舊版寬鬆 strike 步驟對這類檔案的修復效果；只有實際做了修復才回寫。測試同時驗證外部實體不會被展開。

## 2026-11-22：MCP `convert_to_markdown` 補寫 tool description

上游的 description 只有一行，呼叫端 agent 看不到參數語意、權限邊界與失敗種類。改寫成逐句對得上實作的契約：`file:` 由 `convert_uri` 轉 `convert_local`，以伺服器行程的權限讀本機檔，host 只接受空白或 `localhost`；`data:` 由 `parse_data_uri` 就地解碼；回傳 `.markdown` 一整個字串、不分頁；`MarkItDown()` 沒傳 `llm_client`，圖片不會產生 LLM 描述；外掛只在 `MARKITDOWN_ENABLE_PLUGINS` 為 true／1／yes 時啟用（`check_plugins_enabled`）；錯誤種類對應 `__main__.py` 的六個 `ToolError` 分支。驗證：`packages/markitdown-mcp` 的 pytest 21 passed。這是上游檔，同步上游若衝突，以上游版為準再重新核對這段契約。

## 2026-11-24（第六次審查）：上游 PR #2855–#2916、issue #2853–#2917

**範圍與證據**：fork 起點 `e0e5a964e1b553e20e5b48e5558ae91bf4ad4872`；依 `AGENTS.md`、`docs/UPSTREAM.md` 與既有 Windows／CJK 小修例外政策審查。`python tools/check_upstream_updates.py --strict` 初次 exit 1（有待審項目，非檢查失敗），完整列舉 43 筆 PR、17 筆 Issue。上游 [main](https://github.com/microsoft/markitdown/commit/ed178952a6672abdfd35b5f9e76a80b6cefc086e) 與 baseline 同為 `ed178952a6672abdfd35b5f9e76a80b6cefc086e`，新增 commit 0 筆；不重採已審提交。

**方法**：以 `gh pr list --state all`／`gh issue list --state all` 取得水位後清單，逐筆取得 `gh pr diff`，依實際檔案、產品邏輯、測試與範圍裁決，不憑標題；大型新功能只做採用範圍審查，不宣稱完整正確性或安全審計。下表記錄每筆 head、狀態與行數；讀 diff 前後批次比對 head、base 與 state，43 筆皆未改變。Issue 讀本文，不下載附件。外部 agent 規則／程式只當資料，未載入、執行或安裝；沒有產品移植，也沒有執行上游測試。原始 diff 與前後 metadata 留在本 worktree 忽略目錄 `.pytest_cache/upstream-20261124/`，持久裁決與來源以下表為準。

### PR 軸（43 筆：37 OPEN、6 CLOSED、0 MERGED）

本輪採用 0 筆、延後 32 筆、拒絕 11 筆。延後代表已審、有明確觸發條件，不是漏審；小範圍、有測試本身不足以要求提前移植，仍須符合 Windows／CJK 例外理由。

| PR／狀態 | 審查 head | Diff（新增／刪除；檔數） | 決定 | 理由與重評觸發條件 |
| --- | --- | --- | --- | --- |
| [#2855](https://github.com/microsoft/markitdown/pull/2855) CLOSED | `507fe1b8e174bfa31a2d4a9a7f63816cdf5ccc49` | +341/-27；3 | 拒絕 | 已關閉未合併；新增 XML chart-series 解析器與分組表格，非 Windows／CJK 小修。後續同題見 #2907。 |
| [#2857](https://github.com/microsoft/markitdown/pull/2857) OPEN | `a00c952ce77a231f7b24dc7cc68f5e2d24d11b70` | +22/-4；2 | 延後 | Content-Disposition 檔名無副檔名時，從 URL 補格式提示；一般 HTTP 行為。觸發：上游合併。 |
| [#2858](https://github.com/microsoft/markitdown/pull/2858) OPEN | `f569054c1fd0008daa501508bd3c9e28fd42d675` | +64/-2；2 | 延後 | 空 Atom feed 以 namespace 或必要 metadata 辨識；與 #2780／#2782／#2861 競合。觸發：上游擇一合併，或實際輸入命中既有空 feed 裁決。 |
| [#2859](https://github.com/microsoft/markitdown/pull/2859) OPEN | `65d0c4cf8ef7e06ed93d17bdf8f50514302071fb` | +316/-32；2 | 延後 | 以 namespace URI 複製 OMML 節點，改寫 DOCX 數學前處理；有 namespace／Unicode 測試，但不是 Windows／CJK 專屬且範圍較廣。觸發：上游合併。 |
| [#2861](https://github.com/microsoft/markitdown/pull/2861) OPEN | `0734b44b2774746a0f318842b71427cd51605209` | +35/-3；2 | 延後 | 有 Atom namespace 即允許零 entry，無 namespace 仍要求 entry；與 #2858 的無 namespace metadata 規則不同。觸發：上游擇一合併，或實際空 feed 輸入。 |
| [#2863](https://github.com/microsoft/markitdown/pull/2863) OPEN | `1f90fe3aee398095b6fc3e473bb4716b96fa3acb` | +2/-2；2 | 延後 | 兩份 README 的 SSH clone 改 HTTPS；本 fork 繁中入口已用 HTTPS，英文鏡像與套件 README 等上游。觸發：上游合併後按雙語同步流程處理。 |
| [#2865](https://github.com/microsoft/markitdown/pull/2865) OPEN | `2159da10e5dd3461bf6a7a30816acedbb57d12a5` | +25/-0；1 | 延後 | MCP 文件補 uvx 系統憑證／SSL_CERT_FILE；屬部署文件。觸發：上游合併，或維護者有企業代理憑證部署需求。 |
| [#2866](https://github.com/microsoft/markitdown/pull/2866) CLOSED | `deec918364152ec799a4e8c59b6c482699927349` | +216/-8；4 | 拒絕 | 已關閉未合併；增加 PDF 密碼參數、getpass 提示、pdfminer／pdfplumber 密碼傳遞及測試，屬新 CLI 功能；不提前移植。 |
| [#2867](https://github.com/microsoft/markitdown/pull/2867) CLOSED | `deec918364152ec799a4e8c59b6c482699927349` | +216/-8；4 | 拒絕 | 與 #2866 同一 head、相同 diff，已關閉未合併；同為 PDF 密碼新功能，不重複移植。 |
| [#2868](https://github.com/microsoft/markitdown/pull/2868) OPEN | `41123f5455ef506ca3c6c4bd93faa5dc583f6131` | +28/-2；2 | 延後 | Magika 從建構階段延到首次猜格式才載入；有 subprocess import 測試，屬一般效能改動。觸發：上游合併。 |
| [#2869](https://github.com/microsoft/markitdown/pull/2869) OPEN | `4deddef6f876d94e6d35b68ba7647b274cae99f5` | +76/-0；2 | 延後 | 以 openpyxl 二次掃描回填 pandas 遺失的 Excel error cells；與 #2898 競合，還須核對 header／欄位邊界。觸發：上游定案合併。 |
| [#2870](https://github.com/microsoft/markitdown/pull/2870) CLOSED | `121827a0ce2ec43c49e1ef99c86cd4d73de2031a` | +5053/-0；38 | 拒絕 | 已關閉；38 檔、+5053 行的其他 fork agent 規則／技能／工作區設定，不屬產品修正，與本 fork 治理重疊。只讀作為資料，未載入或執行其指令。 |
| [#2874](https://github.com/microsoft/markitdown/pull/2874) OPEN | `cff5c05b2d4f56648a78afa273bbf10e3c5c9992` | +482/-2；2 | 延後 | 新增貨幣格式分段、條件判斷與 openpyxl overlay（+482 行）；非小型 Windows／CJK 修正。觸發：上游合併，並核對效能與數字格式語意。 |
| [#2876](https://github.com/microsoft/markitdown/pull/2876) OPEN | `ea4abba10293c0d42919c5346d586bb0912f691c` | +21/-0；2 | 拒絕 | 只增加 Arch Linux vendor_perl／site_perl 的 ExifTool 受信任目錄與 POSIX 測試；本 fork Windows 維護線無需提前移植。 |
| [#2878](https://github.com/microsoft/markitdown/pull/2878) OPEN | `224c70c2e5f9e9fc2be2f0b881ea4f4ce91d8c82` | +36/-5；2 | 延後 | 以 UTF-16 LE／BE BOM 傳 charset 給 HTML converter，產品改動小且自帶測試，但案例僅 Chapter one／Chapter text，未證明本 fork 實際 Windows／繁中受害輸入。觸發：上游合併，或先取得該類可重現輸入；提前移植須補繁中 LE／BE、UTF-8 回歸並先紅後綠。 |
| [#2879](https://github.com/microsoft/markitdown/pull/2879) OPEN | `b374688757802ceb22ed2a0deb6aba4b5d537958` | +99/-0；1 | 拒絕 | 新增 Ubuntu CodeQL 範本，actions 以 tag 引用；本 fork 已有 SHA 釘版 CodeQL workflow，不覆蓋現有安全與 Windows 維護設定。 |
| [#2880](https://github.com/microsoft/markitdown/pull/2880) OPEN | `1afd362d2809437cf7e284d91ef95a5c7d431eff` | +1/-1；1 | 延後 | 只改上游根 README 的 clone URL，與 #2863 重複。觸發：上游合併後同步英文鏡像及繁中入口。 |
| [#2881](https://github.com/microsoft/markitdown/pull/2881) OPEN | `50d8381accba83a2055ae024f0221fa7184b476a` | +12/-0；1 | 延後 | MCP README 增 pip 安裝的 Claude Desktop command 設定；屬文件。觸發：上游合併，或本 fork 有該部署需求。 |
| [#2882](https://github.com/microsoft/markitdown/pull/2882) OPEN | `834668539e995b904e210670258f37c20a954909` | +286/-6；2 | 延後 | 新增 PDF 視覺順序 RTL 重排及 Arabic／Hebrew 測試（+286 行），不是 CJK 或 Windows 小修。觸發：上游合併。 |
| [#2883](https://github.com/microsoft/markitdown/pull/2883) OPEN | `1f27bb9e2fe50acf4dd055f7773865a99c7971f3` | +27/-4；2 | 延後 | ZIP Markdown 由反覆串接改單次 join，附多 member 順序測試；不改檔名碼頁，非 #2756 的 cp950 修正。觸發：上游合併。 |
| [#2884](https://github.com/microsoft/markitdown/pull/2884) OPEN | `cddcaa248c6390863ea5912a28ed632a191fb225` | +267/-5；4 | 延後 | MCP 延遲 import、重用 converter、thread lock、anyio 執行緒與 HTTP timeout，另關閉 debug；牽動資源／併發模型及依賴，不能當小修，且須保留本 fork 11-22 tool description。觸發：上游合併，或本 fork 重現記憶體／事件迴圈問題。 |
| [#2885](https://github.com/microsoft/markitdown/pull/2885) OPEN | `112e9a02f2fcbf5ab768268bc03fae989bc55395` | +566/-27；6 | 延後 | MiniCPM-OCR 模型選擇、專用 prompt、OTSL 轉表格與後處理（6 檔、+566 行）；新增後端而非例外 bug fix。觸發：上游合併且本 fork 有後端需求。 |
| [#2886](https://github.com/microsoft/markitdown/pull/2886) CLOSED | `df1dceb7ad72a42628249243ed2cf8774213d18c` | +763/-0；12 | 拒絕 | 已關閉；新增其他組織的內部 HTTP API、Docker／worker／認證與 service CI，超出本 fork 範圍。 |
| [#2887](https://github.com/microsoft/markitdown/pull/2887) CLOSED | `5844a5cdbdc2ea3f74aa21d1399383b43befce6e` | +97/-9；7 | 拒絕 | 已關閉；diff 混入已採用的 HTTPS transcription／ExifTool／README 提交，另升上游 setup-python。維護 workflow 獨立且 SHA 釘版，不重複引進舊修正。 |
| [#2888](https://github.com/microsoft/markitdown/pull/2888) OPEN | `c3cbd5fd77d4afb18e273e3d858014407bbd3cab` | +43/-3；2 | 延後 | XLSX／XLS 的 float_format 與 na_rep 改整數／空白輸出；一般格式政策，非 Windows／CJK。觸發：上游合併。 |
| [#2889](https://github.com/microsoft/markitdown/pull/2889) OPEN | `68a890c11a28ce2f906743d02f88e388192944f9` | +124/-1；2 | 延後 | PPTX 從 connector XML 輸出形狀間 Connections，辨識箭頭／重名／隱藏線；新增輸出語意。觸發：上游合併。 |
| [#2890](https://github.com/microsoft/markitdown/pull/2890) OPEN | `4adc71a3d5c25079d4e208566845faf3dea10d03` | +1225/-0；4 | 延後 | PDF opt-in 多行程、shared memory、Windows Job／Linux cgroup 資源探測與 fallback（+1225 行）；雖含 Windows 測試，仍是跨平台功能擴充，不符合小修例外。觸發：上游合併且有明確效能需求。 |
| [#2891](https://github.com/microsoft/markitdown/pull/2891) OPEN | `1122619cc5f8afac19a0fc62d1198479793f419a` | +22/-0；2 | 延後 | RSS 無標題項目的日期前補空行，附回歸測試；一般版面修正。觸發：上游合併。 |
| [#2892](https://github.com/microsoft/markitdown/pull/2892) OPEN | `4bfcef963ea09fa9aa6fe73dd4a872d91f797b3f` | +27/-1；2 | 延後 | HTML metadata 排除 SVG title，附測試；一般標題辨識修正。觸發：上游合併。 |
| [#2894](https://github.com/microsoft/markitdown/pull/2894) OPEN | `76da2deadf7afa54f6fbde1ccc2cdf16e0db00be` | +25/-1；2 | 延後 | ipynb 的字串 source 先 splitlines 再取標題；與 #2763／#2768／#2777／#2778 同題。觸發：上游擇一合併。 |
| [#2895](https://github.com/microsoft/markitdown/pull/2895) OPEN | `8a8e83ccb513ce307114072f83d3d68bb304769c` | +1/-0；1 | 延後 | 測試文件索引加 test_docintel_converter.py；不改測試行為。觸發：上游合併後核對本 fork 檔案是否存在再同步。 |
| [#2898](https://github.com/microsoft/markitdown/pull/2898) OPEN | `1ce04caf6d53b4983f25bbec927c91c34f4009b8` | +46/-2；2 | 延後 | 暫改 pandas 私有 OpenpyxlReader._convert_cell 以保留 error cells；finally 會還原，但共用類別的修改期間仍可能污染併發讀取，不能當安全的逐呼叫修正。與 #2869 同題。觸發：上游定案合併，且回歸涵蓋併發、欄位及空值語意。 |
| [#2901](https://github.com/microsoft/markitdown/pull/2901) OPEN | `688364f2ef9f0ced585372047464952ab6c6f987` | +71/-2；3 | 延後 | 首次 HTTP host DNS 解析後阻擋私網並設 timeout；requests 仍自動重新導向，且檢查後會再解析，未涵蓋 redirect／DNS 變化，不能宣稱完整 SSRF 防護。觸發：上游定案合併，或本 fork 對外提供 MCP HTTP／接收不可信 URI；需先定義目的地政策。 |
| [#2905](https://github.com/microsoft/markitdown/pull/2905) OPEN | `832ce9dfb3f909d321fe89d9624ed049ac870a99` | +196/-9；8 | 拒絕 | 標題 MAINNET_RPC_URL，實際 diff 是 CodeQL 範本、上游 setup-python 及已採用的產品／README 歷史修正；非 RPC 功能。與現有治理重複，不能按標題採用。 |
| [#2907](https://github.com/microsoft/markitdown/pull/2907) OPEN | `17fdff1b548accaa7cd630e358ed50914f37435d` | +123/-23；2 | 延後 | PPTX 依 plot 比較 categories，相同合表、不同分表；與 #2840／#2855 同題。觸發：上游擇一合併，或使用者實際簡報命中既有複合圖表裁決。 |
| [#2908](https://github.com/microsoft/markitdown/pull/2908) OPEN | `38fffe8c6d54d04dc466870c0e15a08f35345152` | +1635/-6；14 | 延後 | 新增 ConversionWarning 公開 API、PDF 曲線偵測、診斷文件與 binary fixtures（14 檔、+1635 行）；屬輸出契約擴充，不是例外小修。觸發：上游合併且有診斷需求。未下載或執行 binary fixtures。 |
| [#2910](https://github.com/microsoft/markitdown/pull/2910) OPEN | `832ce9dfb3f909d321fe89d9624ed049ac870a99` | +103/-4；3 | 拒絕 | 與 #2905 同一 head、不同 base；diff 是 CodeQL 與 setup-python，不是名為 MUDX-tech 的產品功能。現有 workflow 獨立維護，不採用。 |
| [#2911](https://github.com/microsoft/markitdown/pull/2911) OPEN | `356b90ee25d39778e3079cc07d139db9a3259cb8` | +102/-0；2 | 拒絕 | 重複 CodeQL 範本另帶空白 @Mikke84 檔；現有 SHA 釘版掃描已覆蓋，不採用額外 workflow／無關檔案。 |
| [#2912](https://github.com/microsoft/markitdown/pull/2912) OPEN | `25b3f8e541f2e0dc1f76e894aea5c5bd7e9221ca` | +106/-0；3 | 延後 | markdownify 預設 table_infer_header=True，影響 HTML 與 DOCX，附 opt-out 測試；一般輸出預設變更。觸發：上游合併。 |
| [#2913](https://github.com/microsoft/markitdown/pull/2913) OPEN | `38c557bc5b3553e23cb757db6380b683aca116f2` | +72/-1；2 | 延後 | CLI --extract-images 寫 base64 圖到輸出旁並改連結，新增落地副作用與檔名政策；非 Windows／CJK 小修。觸發：上游合併且本 fork 有明確需求。 |
| [#2914](https://github.com/microsoft/markitdown/pull/2914) OPEN | `de049e2f5ee97846ad59a95f9c7343d89f68fc7d` | +51/-3；3 | 延後 | 保留被 fragment 連結引用的空 anchor，影響 HTML／DOCX 書籤，附跳脫測試；一般結構修正。觸發：上游合併。 |
| [#2915](https://github.com/microsoft/markitdown/pull/2915) OPEN | `eb0703b6f9e3434ce3c31b69c86850ed0f636047` | +8/-0；1 | 延後 | README 補 stdin --extension／--charset 使用方式；不是碼頁修正。觸發：上游合併後按雙語入口流程同步。 |
| [#2916](https://github.com/microsoft/markitdown/pull/2916) OPEN | `0e06a5cac0e7c8156c2af16c0011a4575e1aa9dc` | +357/-10；2 | 延後 | PPTX 改逐 run 超連結、段落清單與表格 cell／notes 格式（+357 行），牽動共用 converter 輸出；與 #2843 同題，非小修例外。觸發：上游擇一合併。 |

### Issue 軸（17 筆）

| Issue | 決定 | 理由與觸發條件 |
| --- | --- | --- |
| [#2853](https://github.com/microsoft/markitdown/issues/2853) CLOSED | 拒絕 | 本文為空，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2856](https://github.com/microsoft/markitdown/issues/2856) CLOSED | 拒絕 | 只有文件上傳失敗註記，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2860](https://github.com/microsoft/markitdown/issues/2860) CLOSED | 拒絕 | 本文為空，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2862](https://github.com/microsoft/markitdown/issues/2862) OPEN | 延後 | 上游 clone URL 使用 SSH 的文件問題，對應 #2863／#2880；繁中入口已用 HTTPS。觸發：上游合併後同步英文鏡像與套件 README。 |
| [#2864](https://github.com/microsoft/markitdown/issues/2864) CLOSED | 拒絕 | 要求把簡報轉 Markdown，未提供錯誤或重現步驟。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2872](https://github.com/microsoft/markitdown/issues/2872) CLOSED | 拒絕 | 本文為空，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2873](https://github.com/microsoft/markitdown/issues/2873) CLOSED | 拒絕 | 本文為空，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2877](https://github.com/microsoft/markitdown/issues/2877) CLOSED | 拒絕 | 只有 PDF 附件，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2893](https://github.com/microsoft/markitdown/issues/2893) OPEN | 拒絕 | 只有 PDF 附件，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2896](https://github.com/microsoft/markitdown/issues/2896) OPEN | 拒絕 | 要求把簡報轉成可供 AI 使用的 Markdown，沒有產品錯誤。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2897](https://github.com/microsoft/markitdown/issues/2897) OPEN | 拒絕 | 與 #2896 相同轉檔請求與附件，沒有產品錯誤。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2902](https://github.com/microsoft/markitdown/issues/2902) OPEN | 拒絕 | 只有 PDF 附件，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2903](https://github.com/microsoft/markitdown/issues/2903) OPEN | 拒絕 | 本文為空，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2904](https://github.com/microsoft/markitdown/issues/2904) OPEN | 拒絕 | 只有 PDF 附件，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2906](https://github.com/microsoft/markitdown/issues/2906) OPEN | 拒絕 | 本文只有 Google，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2909](https://github.com/microsoft/markitdown/issues/2909) OPEN | 拒絕 | 詢問如何把 PDF 轉成較省 AI 額度的檔案，沒有可重現缺陷。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |
| [#2917](https://github.com/microsoft/markitdown/issues/2917) OPEN | 拒絕 | 只有招標文件附件清單，沒有缺陷描述。不下載附件；若後續補可重現缺陷與可公開最小輸入，再重評。 |

**水位決定**：驗證完成後，PR `#2852` → `#2916`、Issue `#2850` → `#2917`；commit 水位維持 `ed178952a6672abdfd35b5f9e76a80b6cefc086e`，`reviewed_date` 更新為 2026-11-24。本輪列舉到的增量無未審項；舊水位以下的 OPEN PR 與非 main 分支不重做全面盤點，仍依既有合併／輸入觸發條件追蹤。

**路線圖**：刪除「無近期工作」的過時佔位，保留既有觸發條件並加入本輪 EPUB／MCP／URI 裁決；補回 REVIEW 已記錄的 Windows 全套產品驗收與 PowerShell 5.1 未驗證事項。11-21 修復、自有產品 CI 與 11-22 MCP 文件已完成，不再列為待做。本輪未查遠端安全 alerts、CI 或 PyPI，未沿用舊狀態宣稱它們已通過。

**驗證**：`pwsh -NoProfile -File tools/dev_check.ps1` exit 0（43 passed，Ruff 與文件連結檢查通過），完成後才推進 PR／Issue 水位。產品程式未變，未執行 `tools/test_product.ps1 -AllPackages`，不宣稱本輪補齊歷史產品驗收。
