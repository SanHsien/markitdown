# Repository review（Windows-only）

- Review date: 2026-11-20（增量審查）
- Review range: `aa9b84c..c8377f4`（52 commits，111 檔）
- Remediation: 2026-11-21，fork-local（不回貢）
- Upstream reviewed through: `ed178952a6672abdfd35b5f9e76a80b6cefc086e`（PR 水位 `#2852`，見 `tools/upstream_baseline.json`）
- Primary environment: Windows 11、PowerShell 7.7、Python 3.14.10；產品 Python 要求 `>=3.10`
- Status: 本輪 F-1、F-2、H-1、H-2 已修；F-3 未驗證。前一輪全庫審查（2026-09-11，baseline `9480644`）的 R-01～R-10 已全數修復，紀錄見 git 歷史。

## 結論

產品行為跟隨上游，加上本 fork 的 Windows／CJK 例外移植。本輪增量審查找到兩個實際缺陷：OCR plugin 啟用時 XLSX 缺圖會讓 OCR converter 整份失敗；CLI 管線輸出一律 UTF-8 讓繁中 PowerShell 擷取與接 cmdlet 變亂碼。兩者都已修並補上修前會失敗的測試。

## 已修 findings

| ID | 嚴重度 | 問題 | 修正 | Commit（2026-11-21） |
|---|---|---|---|---|
| F-1 | P2 | 啟用 OCR plugin（即使沒設 LLM）時，XLSX 的圖片關聯指向不存在的媒體檔，`XlsxConverterWithOCR` 丟 `KeyError` | 沒有 OCR service 時直接委派原生 `XlsxConverter`，完全不解析圖片；核心 `_XlsxImages` 照上游 #2506 設計不改（有 service 時壞參照仍由 dispatcher 退回內建 converter）。測試：`test_no_service_never_parses_images_so_broken_media_stays_native`、`test_plugin_without_llm_converts_workbook_with_missing_image_directly` | `ea28184` |
| H-1 | hardening | plugin 啟用時不論有無 service 都把所有嵌入圖讀進記憶體 | 與 F-1 同一修正：沒有 service 不建 `_XlsxImages` | `ea28184` |
| F-2 | P2 | `c4b726c` 讓非 tty stdout 一律寫 UTF-8；PowerShell（OutputEncoding 950）的 `$x = markitdown f`、`\| Select-String` 變亂碼 | 依消費端選編碼：`PYTHONIOENCODING`／UTF-8 mode 優先；Windows pipe 用主控台輸出碼頁；檔案與其他情況 UTF-8。實測表與取捨見 `docs/DECISIONS.md` 2026-11-21。測試：`test_redirected_encoding_follows_the_consumer_without_explicit_override`、`test_explicit_python_encoding_overrides_the_console_code_page`、`test_explicit_pythonioencoding_is_honored_for_redirected_output`、`test_stdout_redirected_to_a_file_is_utf8`、`test_piped_output_in_a_code_page_replaces_unencodable_text` | `c0f3ad6` |
| H-2 | hardening | `_pre_process_styles` 改嚴格 lxml 解析後，styles.xml 不是 well-formed 時雙刪除線正規化一起失效 | 嚴格解析失敗改用 `recover=True` 重試，保留 `resolve_entities=False, no_network=True`。測試：`test_not_well_formed_styles_still_normalize_double_strike`、`test_recovering_malformed_styles_does_not_expand_external_entities` | `8c0d54b` |

修復過程額外更正：`docs/DECISIONS.md` 2026-11-02 #2803 條目「cp950 讓繁中文字直接變 `?`」與實測不符（cp950 可編碼一般繁中字，只有碼頁外字元變 `?`），已加更正註記（DECISIONS 更正與本 REVIEW 同一 commit）。

## 未驗證

| ID | 內容 | 狀態 |
|---|---|---|
| F-3 | Windows PowerShell 5.1（`powershell.exe`）的 `markitdown f > out.md` | 本機呼叫 `powershell.exe` 一律卡住，未取得輸出。依 5.1 `>` 先以 OutputEncoding 解碼再寫 UTF-16 的行為推論，F-2 的新規則對它較正確，但沒有實測證據 |

## 接受、不改契約

| ID | 處理 |
|---|---|
| pwsh 7 `>` 輸出碼頁 | PowerShell 7 的 `>` 對 Python 而言與擷取同為 pipe，無法區分；pwsh `>` 得到主控台碼頁位元組（與 `c4b726c` 之前相同）。要 UTF-8 檔案用 `-o` 或 `PYTHONIOENCODING=utf-8`，README 已寫明 |

## 驗證證據

- 新測試在未修的原始碼上失敗（F-1 3 個、F-2 12 個、H-2 2 個），修正後通過；`test_stdout_redirected_to_a_file_is_utf8` 與 `PYTHONIOENCODING=utf-8` 案例修前修後都過，是保護 #1219 修正的回歸測試。
- 聚焦套件（`packages/markitdown-ocr/tests`、`packages/markitdown-sample-plugin/tests`、核心 `test_docx.py`、`test_cli_misc.py`、`test_xlsx.py`）：279 passed、1 skipped。核心與 MCP 全套未跑完（核心全套在本機約 15 分鐘只跑到 5%，預估逾一小時，中途停止），不宣稱全套綠燈。
- `pwsh -NoProfile -File tools\dev_check.ps1`：WINDOWS DEV CHECK GREEN。
- 環境：全新 venv，`requirements-dev.txt`＋`requirements-all.txt`＋四個套件 editable 安裝（mammoth 1.13.0，滿足 `>=1.12.2`）。

## 尚未宣稱範圍

- **沒有**測試跨平臺音訊硬體裝置或雲端即時 Document Intelligence 授權轉譯。
- **沒有**驗證 Windows PowerShell 5.1 的 CLI 輸出（F-3）。
- **不宣稱** 本 fork 發佈獨立 PyPI 套件取代官方發行（本 fork 採 0.2.0 自主維護里程碑版號，不對外發佈 PyPI）。
- **不宣稱** 已將任何修改提交回微軟上游。
