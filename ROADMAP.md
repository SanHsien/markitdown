# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-11-24 依本 worktree 起點 `e0e5a964e1b553e20e5b48e5558ae91bf4ad4872` 與當日上游查詢的快照；不代表未來的 GitHub 狀態。

## 現況
這是多格式文件轉 Markdown 的 Windows 維護型 fork，產品與維護工具的安裝、驗收分開（[FORK](FORK.md)、[開發指引](docs/DEVELOPMENT.md)）。2026-11-24、fork SHA `e0e5a964e1b553e20e5b48e5558ae91bf4ad4872`：上游 main 仍為 `ed178952a6672abdfd35b5f9e76a80b6cefc086e`，commit 水位後新增 0 筆；新增 PR 43 筆（37 OPEN、6 CLOSED、0 MERGED）與 Issue 17 筆已逐筆裁決，PR 水位至 #2916、Issue 至 #2917，未移植產品修正（[本輪決策](docs/DECISIONS.md)）。

截至同一 fork SHA，11-21 的 PowerShell 管線編碼、DOCX styles 容錯、XLSX OCR 壞圖跳過與分段大小限制已完成；fork 自有產品 CI 已加入，MCP 工具說明已補齊。產品 CI 的核心套件涵蓋 Windows／Ubuntu、Python 3.10–3.13；OCR／MCP CI 只跑 Ubuntu，Windows 仍靠本機驗收。最近全套產品驗收未完成，PowerShell 5.1 輸出仍未驗證（[風險快照](REVIEW.md)）。本輪未重查 Dependabot、Code scanning 與遠端 CI，不沿用舊的綠燈數字。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 補齊 11-21 修復後的 Windows 產品全套驗收 | 既有聚焦測試已通過，但核心與 MCP 全套未跑完，不能宣稱全套綠燈 | 執行 `pwsh -NoProfile -File tools/test_product.ps1 -AllPackages`，保存各套件結果與 exit code；逾時只記 incomplete，依已完成批次續跑 | Codex | REVIEW.md「驗證證據」；docs/DECISIONS.md 2026-11-21 |
| 驗證 PowerShell 5.1 的 CLI 輸出（F-3） | `powershell.exe` 先前卡住，尚無實測證據 | 先以有逾時的最小啟動確認環境，再驗證繁中擷取、管線與 `>`；卡住即記阻礙，不宣稱成功 | Codex | REVIEW.md「未驗證」；docs/DECISIONS.md 2026-11-21 CLI 條目 |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 採用 ZIP／文字／EPUB 編碼修正 | 上游合併 #2756、#2679／#2723／#2878；EPUB 若先有實際 Windows／繁中受害輸入，依例外政策重評 | ZIP 測 cp950 檔名，文字測 CJK charset，EPUB 測 UTF-16 LE／BE BOM、繁中內容及 UTF-8 不退步；每次移植須先紅後綠，再跑 Windows 全套產品測試 | Codex | docs/DECISIONS.md 2026-10-25、2026-11-24 #2878 |
| 隨上游採用 PPTX／DOCX／ipynb／RSS／XLSX／HTML 轉換修正 | 上游定案合併，或使用者輸入命中既有裁決允許重評的缺陷 | 按合併版本補回歸，核對複合圖表／超連結、數學 namespace、notebook 標題、空 feed、Excel 錯誤值與表頭；#2898 的全域 monkeypatch 須避免併發污染；Windows 全套測試通過 | Codex | docs/DECISIONS.md 2026-10-26、2026-10-28、2026-11-09、2026-11-24 逐筆裁決 |
| 重評 URI 目的地與 data URI 輸入政策 | 上游合併 #2621／#2622／#2775／#2901，或 fork 對外提供 MCP HTTP／接收來源不明 URI | 先定義允許目的地及拒絕案例；測試內網目的地、重新導向與 DNS 解析變化，合法本機轉換不退步；#2901 目前只檢查首次目的地，不能視為完整防護 | Codex | docs/DECISIONS.md 2026-10-25、2026-11-24 #2901；README.md 安全提示 |
| 重評 MCP 資源與非同步修正 #2884 | 上游合併，或本 fork 出現可重現的記憶體／事件迴圈阻塞問題 | 驗證 converter 重用、轉換互斥、HTTP timeout、取消行為與既有 tool description；Windows MCP 測試及全套產品測試通過 | Codex | docs/DECISIONS.md 2026-11-24 #2884；2026-11-22 MCP 契約 |
| 擴充 Python／OCR 驗收 | 上游 CI 加入 Python 3.15，或 fork 確有 OCR 修正需求與可用後端 | Python 按上游支援更新矩陣且 Windows gate 通過；OCR 以維護者授權的測試輸入驗證，不把 mock 當雲端成功 | Codex | docs/DECISIONS.md:69、121；REVIEW.md「尚未宣稱範圍」 |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 全收尚未合併的上游修正或重做已保留的例外移植 | 例外政策與採用理由見 docs/DECISIONS.md 2026-10-25 | 新修正明確屬 Windows／CJK、小範圍且自帶可驗測試，或上游合併 |
| 提前加入 MiniCPM-OCR、PDF 多行程／向量診斷、圖片落地等新功能 | #2885／#2890／#2908／#2913 是新後端、資源模型或 API／CLI 擴充，不是小型 Windows／CJK 修正 | 上游合併且本 fork 有明確需求時重評；不得只因測試存在就提前移植 |
| 匯入第三方 agent 規則、內部 HTTP service 或重複 CodeQL workflow | #2870／#2886 是其他 fork 的工作流與服務；#2879／#2905／#2910／#2911 與本 fork 現有安全掃描重複 | 維護者明確改變產品／治理範圍；第三方技能另依安全審計流程 |
| 預先修極短 BOM、NUL 後空白與程式碼區塊連結檢查 | 觀察項尚無實際受害輸入，見 docs/DECISIONS.md:140-144 | 使用者輸入或維護文件出現可重現錯誤 |
| 為歷史無共同祖先強推，或發佈 fork PyPI 套件 | 歷史形態已知；發佈邊界見 AGENTS.md、FORK.md | 維護者另行授權政策變更 |

## 維護方式
Ruff 的版本限定 deferral 仍記錄 2026-11-07 審視的 0.17.4，保留 `>=0.16` 相容下限；這是既有裁決，不代表本輪已查 PyPI 最新版本（[維護決策](docs/DECISIONS.md)）。
每週依 [上游流程](docs/UPSTREAM.md) 與 `tools/upstream_baseline.json` 逐筆審查；水位代表已審，不代表全部採用，No common ancestor 以既有 patch 審查方式處理。
每月依賴新鮮度、遇安全公告即重查；維護變更跑 `pwsh -NoProfile -File tools/dev_check.ps1`，產品改動再按 [開發指引](docs/DEVELOPMENT.md) 跑 Windows 產品測試，不提高下限消音。
