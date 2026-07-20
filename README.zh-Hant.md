# Plugins

[English](README.md) · **繁體中文**(README.zh-Hant.md)

此倉庫收錄了個人的 Codex plugin 範例。

每個 plugin 都放在 `plugins/<name>/` 目錄下，內含必要的
`.codex-plugin/plugin.json` 清單檔，以及可選的附屬結構，例如
`skills/`、`.app.json`、`.mcp.json`、plugin 層級的 `agents/`、`commands/`、
`hooks.json`、`assets/` 等支援檔案。

預設的 Codex marketplace 位於 `.agents/plugins/marketplace.json`，並指向標準的
`plugins/` 目錄。

Claude Code marketplace metadata 位於 `.claude-plugin/marketplace.json`，因此也可以用
下列指令加入：

```bash
/plugin marketplace add jakeuj/CodexPlugins
```

## 現有 Plugins

- [`evennia`](./plugins/evennia/) — Evennia MUD 遊戲開發技能集 — 共 28 個完整技能，涵蓋型別類別、指令、屬性、標籤、腳本、鎖定、頻道、指令集合、物件、房間、出口、角色、帳號、原型、預設指令、說明系統、EvMenu、EvEditor、暱稱、程式碼工具、工作階段、訊號、計時器/監控器/條件處理常式、REST API 和 Web 管理介面。

## 建立新 Plugin

1. 使用指令稿建立 plugin 目錄：

```bash
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py <plugin 名稱>
```

2. 編輯 `plugins/<plugin 名稱>/.codex-plugin/plugin.json` 填入 Codex metadata。

3. 若 plugin 也要能從 Claude Code 安裝，加入
   `plugins/<plugin 名稱>/.claude-plugin/plugin.json`。

4. 在 `plugins/<plugin 名稱>/` 下加入 skills、assets 或其他附屬檔案。

5. 若希望 plugin 出現在個人的 Codex marketplace 中，加上 `--with-marketplace`
   參數執行：

```bash
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py <plugin 名稱> --with-marketplace
```
