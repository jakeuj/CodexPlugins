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
- [`bahamut-post`](./plugins/bahamut-post/) — 使用編輯器安全的原始碼標記，建立、重寫、轉換與修復繁體中文巴哈姆特／Gamer.com.tw 論壇文章。
- [`gw2-blish-hud`](./plugins/gw2-blish-hud/) — 開發、稽核與在地化 Guild Wars 2 Blish HUD、模組及 Pathing/TacO 標記包，特別著重繁體中文與 CJK 支援。

## 將技能發布到 Marketplace

使用 repo 技能 `$publish-skill-to-marketplace` 盤點目前 marketplace，將技能加入
唯一明確匹配的 local plugin；若沒有合適 plugin，則透過系統內建的
`$plugin-creator` 建立新 plugin。

```text
使用 $publish-skill-to-marketplace，將 $bahamut-post 加入此 repo 的 marketplace。
```

若指定技能尚不存在，請提供技能名稱、行為與幾個具體範例。工作流程會先使用系統
內建的 `$skill-creator` 建立並驗證技能，再進行封裝。

## 建立新 Plugin

1. 在 Codex 中使用系統內建的 `$plugin-creator` 技能，在此 repo 的
   `plugins/` 目錄下建立 plugin：

```text
使用 $plugin-creator，在此 repo 的 plugins/ 目錄下建立 <plugin 名稱>。
```

2. 編輯 `plugins/<plugin 名稱>/.codex-plugin/plugin.json` 填入 Codex metadata。

3. 若 plugin 也要能從 Claude Code 安裝，加入
   `plugins/<plugin 名稱>/.claude-plugin/plugin.json`。

4. 在 `plugins/<plugin 名稱>/` 下加入 skills、assets 或其他附屬檔案。

5. 若希望 plugin 出現在此 repo 的 Codex marketplace 中，請系統內建技能加入：

```text
使用 $plugin-creator，將 plugins/<plugin 名稱> 加入此 repo 的 .agents/plugins/marketplace.json。
```
