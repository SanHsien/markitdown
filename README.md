# MarkItDown（SanHsien 維護 fork）

<p align="center">
  <a href="README.md"><strong>繁體中文</strong></a> ·
  <a href="README.en.md">English</a>
</p>

<div align="center">

[![CI](https://github.com/SanHsien/markitdown/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/markitdown/actions/workflows/ci.yml)
[![Upstream tests](https://github.com/microsoft/markitdown/actions/workflows/tests.yml/badge.svg)](https://github.com/microsoft/markitdown/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

本專案 fork 自微軟開源的 [`microsoft/markitdown`](https://github.com/microsoft/markitdown)，沿用 MIT License。主要定位為 **Windows-first 維護型 fork**，提供可重現的 Windows 開發環境驗收門禁、繁體中文入口文件與上游變更追蹤。上游原版英文說明請見 [`README.en.md`](README.en.md)，fork 維護取捨與差異清單見 [`FORK.md`](FORK.md)。

> [!IMPORTANT]
> MarkItDown 會以目前行程（process）的權限執行 I/O 操作。如同 `open()` 或 `requests.get()`，它會存取該行程有權限存取的本機資源或網路位址。在處理不受信任的輸入時，請務必先做好過濾與清理，並依需求呼叫範圍最小的轉換函式（例如 `convert_stream()` 或 `convert_local()`）。

---

## 什麼是 MarkItDown？

MarkItDown 是一套輕量級的 Python 工具庫與命令列工具，專門用來將各類檔案與 Office 辦公文件轉換為 Markdown 格式，以便供大型語言模型（LLM）與文字分析流程處理。

其核心優勢在於能盡可能保留文件的關鍵結構與語義：
- 標題（Headings）
- 列表（Lists）
- 表格（Tables）
- 超連結（Links）
- 程式碼區塊（Code blocks）

支援轉換的格式包含：
- **PDF 文件**（包含文字層解析與選配的 OCR）
- **PowerPoint**（`.pptx`）
- **Word**（`.docx`）
- **Excel**（`.xlsx`, `.xls`）
- **圖片**（EXIF 詮釋資料抽取與 OCR）
- **音訊**（EXIF 詮釋資料與語音轉文字）
- **HTML 網頁**
- **純文字與結構化資料**（CSV、JSON、XML）
- **壓縮檔**（ZIP 封裝檔案逐項遞迴處理）
- **YouTube 網址**（字幕抓取與轉換）
- **EPUB 電子書**
- **Bing 搜尋結果** 與 **Azure Document Intelligence** 整合

---

## 為什麼轉成 Markdown？

1. **LLM 原生親和**：現代語言模型（如 GPT-4o、Claude 3.5、Gemini 1.5/2.0）深度理解 Markdown 結構，甚至在輸出時會自動使用 Markdown 語法呈現。
2. **Token 經濟實惠**：相較於龐大的 HTML 或 XML 標籤，Markdown 格式精簡，佔用極少無效 token，大幅節省 context window 與推理成本。
3. **結構保留完整**：保留純文字遺失的多層次標題、表格欄位關係與列表階層。

---

## 換一台電腦怎麼開發（Windows 11 原生）

本 fork 採 **Windows 11 + PowerShell 原生環境** 作為第一驗收標準。一鍵初始化本機維護與測試環境：

```powershell
git clone https://github.com/SanHsien/markitdown.git
cd markitdown

# 一鍵建立 .venv、安裝維護依賴並執行 Windows gate
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

日常修改後，在提交前執行本機品質門禁：

```powershell
pwsh -NoProfile -File tools\dev_check.ps1
```

詳細說明請見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

---

## 安裝與快速上手

### 安裝方式

使用 pip 安裝基礎套件：

```bash
pip install markitdown
```

若需要完整外掛格式支援（Word, PPT, Excel, PDF, 音訊轉錄等）：

```bash
pip install "markitdown[all]"
```

選配安裝個別擴充模組：

```bash
pip install "markitdown[docx]"       # 支援 Word (.docx)
pip install "markitdown[pptx]"       # 支援 PowerPoint (.pptx)
pip install "markitdown[xlsx]"       # 支援 Excel (.xlsx)
pip install "markitdown[pdf]"        # 支援 PDF
pip install "markitdown[az-doc-intel]" # 支援 Azure Document Intelligence
```

### CLI 命令列使用

```bash
# 轉換檔案並直接印出 Markdown
markitdown path/to/document.pdf

# 轉換並輸出至指定檔案
markitdown path/to/document.docx -o output.md

# 管道（Pipe）輸入
cat document.html | markitdown > output.md
```

### Python API 使用

```python
from markitdown import MarkItDown

md = MarkItDown()

# 轉換本機檔案
result = md.convert("quarterly_report.xlsx")
print(result.text_content)

# 搭配 LLM 提供更進一步的內容詮釋（以 OpenAI 範例）
# from openai import OpenAI
# client = OpenAI()
# md_with_llm = MarkItDown(llm_client=client, llm_model="gpt-4o")
# result = md_with_llm.convert("sample_image.jpg")
# print(result.text_content)
```

---

## 與上游的關係

- 上游 repository：[`microsoft/markitdown`](https://github.com/microsoft/markitdown)
- 本 fork repository：[`SanHsien/markitdown`](https://github.com/SanHsien/markitdown)
- 所有 PR、commit、release 均指向 `SanHsien/markitdown`；未獲當次明確指示前不打向微軟上游。
- 同步機制與審查紀錄請見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

---

## 授權條款

本專案沿用上游的 [MIT License](LICENSE)。第三方相依套件依其個別授權規範，詳見 [`NOTICE.md`](NOTICE.md)。
