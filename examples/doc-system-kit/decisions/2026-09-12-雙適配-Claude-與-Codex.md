---
type: decision
date: 2026-09-12
status: 生效
supersedes:
affects: [文件體系, 移植包, 手冊]
code: [core/starter/AGENTS.md, core/starter/.agents/hooks/doc-sync-check.mjs, core/starter/.agents/hooks/design-guard.mjs, core/starter/.codex/config.toml, core/安裝.md, setup/CodexCLI環境.md]
---

# 同一份 starter 同時支援 Claude Code 與 Codex CLI，不另開 repo

**問題是什麼**

starter 原本是純 Claude Code 的形態：守則在 `CLAUDE.md`、三層裝置綁在
`.claude/settings.json`、`.claude/hooks/`、`.claude/skills/`。
要讓 Codex CLI 也跑同一套流程，第一個要回答的是**共用還是分家**。

分家（另開一個 Codex 專用 repo）看起來乾淨，但代價落在**最有價值的那部分**：
四份文件的分工、DESIGN 唯一參照、回填路由表、commit body 規矩 —— 全是紙上流程，
與工具無關。分家等於把它們維護兩份，而**兩份文字的漂移不會有任何工具報錯**。

**查證到什麼**

實際耦合比看起來小：78 個檔裡真正綁 Claude 的只有 3 個加 `CLAUDE.md`。
而且關鍵的一層可以零修改共用：

| 事實 | 影響 |
|---|---|
| Codex 的 Stop hook stdin 給 `cwd` 與 `stop_hook_active`，stdout 吃 `{"decision":"block","reason":…}` | **與 Claude 契約相同**，`doc-sync-check.mjs` 一個字都不用改 |
| Codex 讀 `AGENTS.md`，不讀 `CLAUDE.md` | 需要一份工具中立的守則正本 |
| Anthropic 官方文件明講：repo 已有 `AGENTS.md` 就寫 `CLAUDE.md` 用 `@AGENTS.md` 匯入 | 正好是本包自己的「同一件事不寫在兩處」 |
| SKILL.md 是開放標準，兩邊都吃；但 Claude 只掃 `.claude/skills/` | 正本可中立擺放，Claude 端補一個 stub |
| Codex 的 PreToolUse 只支援 `allow`／`deny` | **權威層無法等價移植**，見下 |

**選了什麼**

正本集中在工具中立的位置，`.claude/` 與 `.codex/` 只留接線：

| 層 | Claude Code | Codex CLI | 共用 |
|---|---|---|---|
| 守則 | `CLAUDE.md`（`@AGENTS.md`） | `AGENTS.md`（原生） | ✅ 正本一份 |
| 觸發 | `hooks.Stop` | `[[hooks.Stop]]` | ✅ **同一支腳本** |
| 流程 | `.claude/skills/`（stub） | `.agents/skills/`（正本） | ✅ 內容一份 |
| 權威 | `permissions.ask` 跳框 | 硬擋 ＋ `doc/.design-unlock` | ❌ 刻意不同 |

**沒選的路**

| 沒選 | 為什麼 |
|---|---|
| **另開 Codex 專用 repo** | SOP 要維護兩份，而漂移沒有症狀。耦合只有 3 檔，不值得 |
| **`CLAUDE.md` 做成 `AGENTS.md` 的 symlink** | Windows 建 symlink 要管理員權限或開發者模式 —— 與當初選 Node 不選 `.ps1` 是同一個理由。官方文件也建議這種情況改用 `@` 匯入 |
| **hook 腳本留在 `.claude/hooks/`，讓 Codex 指過去** | 那樣 Codex 的設定要指向對手工具的目錄。往後任何人「清掉不用的 `.claude/`」就會無聲拆掉 Codex 的收工檢查 |
| **`.codex/skills/` 也放一份完整 SKILL.md** | 複製出來就會漂移。要就放 stub |
| **Codex 那邊照抄 `permissionDecision: "ask"`** | 它不支援，而且**不報錯**。見 [../gotchas/2026-09-12-Codex-的-PreToolUse-不支援-ask.md](../gotchas/2026-09-12-Codex-的-PreToolUse-不支援-ask.md) |
| **Extras 也做雙適配** | Route A 與 diagram-design 是 Claude Code plugin，沒有對等路線。改成在文件裡標明哪些通用，不假裝等價 |

**權威層為什麼刻意不對稱**

Codex 給不了「跳框問人」，只能 allow 或 deny。硬擋之後「人點頭」需要一個出口，
所以定成 `doc/.design-unlock` 解鎖檔：人建 → AI 改 → 人刪。

換掉之後多了一個好處：**「人點頭」從一個沒有痕跡的按鍵，變成一個具體、
看得見、留得下痕跡的動作。** 代價是人要多做一步，而且那個檔
**必須永遠留在 `.gitignore` 裡** —— 被 commit 的話這層保護就對所有人永久失效，
而且沒有症狀（已列入 [../TECH.md](../TECH.md)「不變式」第 8 條）。

> ⚠️ **2026-09-12 修正**：初版把解鎖檔描述成「AI 自己建不出來」，那是**過度宣稱** ——
> 有 shell 與寫入權限的 agent 可以自己 `touch` 出來。Codex 在驗證時指出這一點。
> 現在 `design-guard.mjs` 會額外擋掉「用工具建立解鎖檔」，但它仍然是
> **協作慣例與防呆，不是安全邊界**。文件措辭已全部改掉。

**留下的未完項**

`.codex/config.toml` 有兩個標了 `⚠ 待實機確認` 的值（`CODEX_PROJECT_DIR` 存不存在、
PreToolUse 的 `matcher` 實際工具名），因為**寫這則時本機沒有可測的 Codex CLI**。
`design-guard.mjs` 設計成「比對不到就放行」，所以填錯的後果是擋不到而不是誤擋 ——
但擋不到沒有症狀，所以標記留在檔案裡，不移除。
探測步驟寫在 [../../../setup/CodexCLI環境.md](../../../setup/CodexCLI環境.md) 第 6 節。
