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
