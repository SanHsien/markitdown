# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `28901f550c6d` 查的快照，開工前先重查 GitHub。

## 現況
這是多格式文件轉 Markdown 的 Windows 維護型 fork，產品與維護工具的安裝、驗收分開（[FORK](FORK.md)、[開發指引](docs/DEVELOPMENT.md)）。2026-10-29 `gh` 查詢顯示 Dependabot／Code scanning 均為 0、CI／CodeQL／Upstream check 最近成功；未採用的上游轉換修正已有重現與觸發條件，不代表沒有已知邊角缺陷（2026-10-29 `gh` 查詢；`docs/DECISIONS.md:171-185`）。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 無：維持現狀，僅在既有觸發條件成立時開工 | 維護缺陷已修，剩餘上游 OPEN PR 不符合例外移植條件 | 開工先查 `gh api repos/SanHsien/markitdown/dependabot/alerts?state=open`、`gh api repos/SanHsien/markitdown/code-scanning/alerts?state=open`，再按 tools/upstream_baseline.json 重查上游；未命中條件就不改產品 | Claude Haiku | 2026-10-29 `gh` 查詢；docs/DECISIONS.md:108、171-185 |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 採用 ZIP／文字編碼修正 | 上游合併 #2756、#2679／#2723，或出現實際繁中輸入問題 | ZIP 修正必測 cp950 檔名不亂碼；文字修正必跑 CJK charset 回歸，再執行 `pwsh -NoProfile -File tools/test_product.ps1 -AllPackages` | Codex | docs/DECISIONS.md:111、132 |
| 隨上游採用 PPTX／ipynb／RSS／XLSX 轉換修正 | 上游定案合併，或使用者輸入命中既有裁決允許重評的缺陷 | 按合併版本補對應回歸，核對圖表資料點、表格邊界、notebook 標題及 feed 辨識，受影響套件與 Windows 全套測試通過 | Codex | docs/DECISIONS.md:133-134、156-159、179-185 |
| 重評 URI 目的地與 data URI 輸入政策 | 上游合併 #2621／#2622／#2775，或 fork 對外提供 MCP HTTP／接收來源不明 URI | 先定義允許目的地及拒絕案例；測試內網目的地、重新導向與片段處理，合法本機轉換不退步 | Claude Opus | docs/DECISIONS.md:110、159；README.md 安全提示 |
| 擴充 Python／OCR 驗收 | 上游 CI 加入 Python 3.15，或 fork 確有 OCR 修正需求與可用後端 | Python 按上游支援更新矩陣且 Windows gate 通過；OCR 以維護者授權的測試輸入驗證，不把 mock 當雲端成功 | Codex | docs/DECISIONS.md:69、121；REVIEW.md「尚未宣稱範圍」 |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 全收尚未合併的上游修正或重做已保留的例外移植 | 例外政策與採用理由見 docs/DECISIONS.md:103-108 | 新修正明確屬 Windows／CJK、小範圍且自帶可驗測試，或上游合併 |
| 預先修極短 BOM、NUL 後空白與程式碼區塊連結檢查 | 觀察項尚無實際受害輸入，見 docs/DECISIONS.md:140-144 | 使用者輸入或維護文件出現可重現錯誤 |
| 為歷史無共同祖先強推，或發佈 fork PyPI 套件 | 歷史形態已知；發佈邊界見 AGENTS.md、FORK.md | 維護者另行授權政策變更 |

## 維護方式
每週依 [上游流程](docs/UPSTREAM.md) 與 `tools/upstream_baseline.json` 逐筆審查；水位代表已審，不代表全部採用，No common ancestor 以既有 patch 審查方式處理。
每月依賴新鮮度、遇安全公告即重查；維護變更跑 `pwsh -NoProfile -File tools/dev_check.ps1`，產品改動再按 [開發指引](docs/DEVELOPMENT.md) 跑 Windows 產品測試，不提高下限消音。