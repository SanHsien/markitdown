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

這套 gate **不安裝** heavy dependencies（如 `azure-ai-documentintelligence`、`SpeechRecognition` 等）。它證明維護文件、工具與契約測試能穩定執行。

### 開發與測試產品程式（選配）

若需要對 `markitdown` 核心功能進行修改或測試：

```powershell
# 建議另開獨立環境或以 editable 方式安裝
pip install -e "./packages/markitdown[all]"
pip install pytest
pytest packages/markitdown/tests
```

## Canonical Gate

`tools\dev_check.ps1` 會依序執行：

1. `python -m compileall`（`tools`）
2. `ruff check`（E9 + F，僅檢查 `tools`）
3. `pytest tools/tests`（使用獨立的 `tools/pytest.ini`）
4. `python tools/check_links.py`（驗證所有維護文件相對連結）

CI 在 Ubuntu 跑 3.10–3.14 矩陣，並搭配 Windows Python 3.14 job 執行同一套 gate。推至 `main` 前請務必在本機跑過 gate。

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
