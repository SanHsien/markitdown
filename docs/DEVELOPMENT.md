# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
packages/
  ├── markitdown/              核心轉換引擎與 CLI（Python >= 3.10）
  ├── markitdown-ocr/          OCR 擴充套件
  ├── markitdown-mcp/          Model Context Protocol（MCP）伺服器
  └── markitdown-sample-plugin 範例外掛模組
tools/                         fork 維護工具（Windows gate、上游檢查、相對連結檢查、依賴新鮮度）
  └── tests/                   維護契約測試
docs/                          fork 維護與治理文件
```

## 本機開發（Windows 11 原生）

### 維護骨架（必跑）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

等價一鍵指令：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

若需一併安裝全套產品轉譯依賴（Office、PDF、音訊、雲端服務等）：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1 -All
```

### 執行產品測試

本 repo 提供專用 Windows 原生產品測試腳本 `tools/test_product.ps1`，會自動載入本機原始碼目錄 `packages/markitdown/src`，避開全域 site-packages 舊版套件的污染：

```powershell
# 執行指定模組測試或全套測試
pwsh -NoProfile -File tools\test_product.ps1
pwsh -NoProfile -File tools\test_product.ps1 packages/markitdown/tests/test_file_paths.py
```

## Canonical Gate

`tools\dev_check.ps1` 會依序執行：

1. `python -m compileall`（`tools`）
2. `ruff check`（E9 + F，僅檢查 `tools`）
3. `pytest tools/tests`（使用獨立的 `tools/pytest.ini`）
4. `python tools/check_links.py`（驗證所有維護文件相對連結）

CI 專注於 Windows 原生環境，在 `windows-latest` 執行完整 Python 3.10–3.14 矩陣並跑過 gate。推至 `main` 前請務必在本機跑過 gate。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 只比對 `requirements-dev.txt` 的宣告。產品依賴在各套件的 `pyproject.toml`，由 Dependabot 開 PR。

紅燈只有兩條誠實的出口：

| 出口 | 寫在哪 | 什麼時候用 |
| --- | --- | --- |
| `# freshness-hold: <理由>` | `requirements-dev.txt` 行末 | 這個下限就是我們要的 |
| `.github/dependency-deferrals.json` 的 `deferredLatest` + `reason` | 獨立檔案 | 已看過、這個月不升；PyPI 超過該版本會恢復提醒 |

不要用調高下限讓報告變綠。

## 不要做的事

- 不要拿掉工作流程上的 `github.repository == 'microsoft/markitdown'` 閘門。
- 不要從本 fork 嘗試發布套件到 PyPI。
- 不要提交含有個人資料、機密資訊或版權爭議的文件作為測試樣本。
- 不要把 PR 指向微軟上游 `microsoft/markitdown`。
