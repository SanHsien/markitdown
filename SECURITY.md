# 安全政策

## 支援範圍

安全修正以本 fork 的最新 `main` 為主；上游微軟版本的問題也會視需要回報原作者或微軟安全回應中心（MSRC）。

## 私下回報

若發現針對本 fork 維護骨架或衍生程式的安全漏洞，請使用 GitHub Security Advisories 的 **Report a vulnerability** 私下回報：
<https://github.com/SanHsien/markitdown/security/advisories/new>。
若該入口不可用，請透過 GitHub 個人檔案聯絡維護者，不要先建立公開 Issue。

若問題屬於上游微軟核心邏輯或原生套件，請依微軟安全流程向 Microsoft Security Response Center（MSRC）通報：
<https://msrc.microsoft.com/create-report> 或寄信至 `secure@microsoft.com`。

回報請包含影響範圍、重現步驟、受影響版本與最小必要證據。請勿在回報中附上真實 API key、token、個人機密文件或帳密。

## 特別注意

- **行程權限與 I/O 邊界**：MarkItDown 會繼承執行中 Python 行程的完整檔案與網路存取權限。處理不受信任的檔案時，需注意路徑遍歷（Path Traversal）、本機敏感檔案讀取或惡意 URL 存取。
- **輸入過濾**：在伺服器端或自動化工作流程中使用 MarkItDown 時，建議呼叫限制更嚴格的函式（如 `convert_stream()`），並對輸入檔名、副檔名與來源 URL 進行白名單驗證。
- **機密資料外洩防護**：轉換結果可能包含文件內嵌的巨集、註解、隱藏工作表或詮釋資料（EXIF）。若整合 LLM 進行分析，需評估是否包含非預期傳送至雲端模型的敏感文字。
- **本專案範圍**：不要將受版權保護的測試文件、真實個人資料、含憑證的設定檔或 API key 提交進 repository。
