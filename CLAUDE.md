# CLAUDE.md

請先完整閱讀並遵守 [`AGENTS.md`](AGENTS.md)。本檔只補充 Claude Code 的最小入口：

- 這是保留上游歷史的 fork；不要移除 `upstream`、原作者或 MIT License 授權標示。
- 產品程式在 `packages/`，以上游為準。
- 預設全自動推進（Full Auto）：所有 session 均完全授權代理人自主判斷並自動執行，無須中途重複確認授權。
- 提交前跑 `pwsh -NoProfile -File tools\dev_check.ps1`。不要把 gate 改成完整產品依賴安裝。
- 測試檔案、使用者專有文件、`.env` 一律不可提交。
- 使用繁體中文，直接交付可驗證結果，避免冗長背景鋪陳。
- PR、push、release 一律指向 `SanHsien/markitdown`，嚴禁未經當次許可打向 `microsoft/markitdown`。
