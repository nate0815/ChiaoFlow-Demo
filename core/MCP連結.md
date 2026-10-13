# MCP 連結

> **選用。** 讓 AI 除了讀 `doc/` 與程式碼之外，還能讀到**編輯器的即時狀態**
> 或**還留在其他平台的內容**。
> **前提**：先完成 [安裝.md](安裝.md)。
> **預計耗時**：15 分鐘。

---

## 1. 先確認 AI CLI 可用

在專案根目錄開啟終端機：

```bash
cd <專案路徑>
claude          # 或 codex
```

> **兩種工具都支援 MCP，但設定方式不同**：Claude Code 用 `claude mcp add` 指令
> 寫進 `.mcp.json`；Codex 則是在 `.codex/config.toml` 裡寫 `[mcp_servers.<名稱>]` 區塊。
> 下面各節的**伺服器本身與用途完全一樣**，只有註冊那一步要看你用哪個工具。
> ⚠ Codex 的 MCP 設定語法請以 `codex` 官方文件為準 —— 本文沒有實機驗證過那一段。

---

## 2. Unity MCP

Unity 官方的 MCP Server 包含在 AI Assistant 套件中：

1. Unity Editor → **Edit → Project Settings → AI → Unity MCP**
2. 依照該頁面指示啟用 bridge 並設定要連接的 AI client

啟用後，Claude Code 可即時存取場景階層、GameObject、component 數值、
Console 輸出與編譯錯誤。

> Unity 的 AI 工具仍在 beta 階段，設定介面可能與本文件不同。以官方文件為準：
> https://unity.com/blog/unity-ai-mcp-how-to-get-started

---

## 3. Notion MCP（選用）

如果專案管理還留在 Notion（看板、待辦），可以讓 AI 讀得到：

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

然後在 Claude Code 中執行 `/mcp` 完成瀏覽器 OAuth 登入。

> ⚠️ **權限提醒**：Notion MCP 以**你本人的完整權限**運作 —— AI 看得到你這個帳號
> 看得到的所有內容，也能修改。需要更小的權限範圍的話，
> 建立一個受限的 Notion 帳號專門給它使用。

> **捷徑**：如果你已經在 claude.ai 的設定裡連接過 Notion 連接器，
> 且 Claude Code 是用同一個 claude.ai 帳號登入，該連接器會**自動出現在 Claude Code**，
> 不需要再跑上面的指令。用 `/mcp` 確認。

---

## 4. 驗證

```bash
claude mcp list
```

應看到各 server 顯示 `✔ Connected`。顯示 `! Needs authentication` 的話，
在 Claude Code 內執行 `/mcp` 完成登入。

> **OAuth 只能在互動式 session 裡完成。** 排程或 headless 執行的 Claude Code
> 跑不了登入流程，會看到 server 一直是未授權狀態 —— 那不是設定壞了，
> 是需要先在互動式 session 裡授權一次。

接著在 Claude Code 中測試一個**同時需要兩邊資訊**的問題：

```
讀 doc/DESIGN.md，然後檢查目前 Unity 場景的階層，
告訴我文件描述的系統有哪些還沒實作
```

能同時回答兩邊 = 環境建置完成。

---

## 5. scope：要不要讓團隊共用

`claude mcp add` 預設寫入 **local scope**（只有你、只有這個專案）。

要讓團隊共用設定，加 `--scope project`，設定會寫進專案根目錄的 `.mcp.json` 並可 commit：

```bash
claude mcp add --transport http --scope project notion https://mcp.notion.com/mcp
```

**注意**：`.mcp.json` 只存 URL 與設定，**不存 token**，每個人仍需各自完成 OAuth。
基於安全考量，Claude Code 在使用專案層級的 server 前會要求你確認。

---

## 6. 接上之後：反向產文件

接手舊模組時特別有用 —— AI 同時看得到編輯器狀態和程式碼，產出的文件比人工回想準確：

```
用 Unity MCP 檢查目前場景的階層和所有 script，
把 Player 相關的架構整理成筆記寫進 doc/TECH.md 的模組契約章節，
用相對路徑連結指向相關的決策檔
```

> ⚠️ **產出的是草稿，不是正本。** 它描述的是「現在的實作長什麼樣」，
> 而 `doc/DESIGN.md` 是「應該長什麼樣」。兩者不一致時**不要讓 AI 自己把 DESIGN
> 改成符合實作** —— 那正是這套體系要擋的事。照升報流程走。

---

## 7. 完成檢查清單

- [ ] `claude mcp list` 全部顯示 `✔ Connected`
- [ ] Unity MCP 已在 Project Settings 啟用（如果是 Unity 專案）
- [ ] 跨系統測試問題能同時回答文件與編輯器兩邊
- [ ] 知道 Notion MCP 是用你的完整權限在跑

---

## 8. 常見問題

**Q：`claude mcp list` 顯示 Needs authentication**
在 Claude Code 內執行 `/mcp`，選擇該 server 完成 OAuth。必須是互動式 session。

**Q：在 claude.ai 連了 Notion，但 Claude Code 看不到**
執行 `/status` 確認目前使用的認證方式。若環境變數中設有 `ANTHROPIC_API_KEY`，
claude.ai 的連接器不會載入。取消該變數後執行 `/login` 選擇 claude.ai 帳號。

**Q：一定要接 MCP 嗎？**
不用。`doc/` 與程式碼本來就在同一個 repo 裡，AI 讀得到 —— 那是這套體系的基礎。
MCP 加的是「編輯器即時狀態」與「repo 外的內容」，是加分不是必要。
