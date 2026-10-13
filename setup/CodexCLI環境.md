# Codex CLI 環境

> **與 [ClaudeCode環境.md](ClaudeCode環境.md) 二擇一**（兩個都裝也行）。
> [Core](../core/) 的三層自動化裝置在兩種工具上都能跑，**共用同一份守則、
> 同一支收工檢查腳本、同一份回填流程**。
> **預計耗時**：15 分鐘（含登入與驗證）。

> ## 驗證狀態（2026-09-12，Codex CLI `0.154.0-alpha.6.2`）
>
> **已實機驗證** ✅
> - `.codex/config.toml` 可被嚴格解析
> - `.agents/skills/doc-sync` 會出現在 model-visible skills 清單 —— **不需要 `.codex/skills` stub**
> - `design-guard.mjs` 擋下 DESIGN 寫入；非目標檔與唯讀 shell 指令正常放行
> - `doc-sync-check.mjs` 在 git fixture 中正確擋下與放行
>
> **仍未驗證** ⚠️
> - `${CODEX_PROJECT_DIR}` 這個變數是否存在。當時的 session 連不到 OpenAI 端點，
>   走不到 Stop 階段。**兩個 hook 都依賴它，不存在的話會無聲失效** ——
>   這是第 6 節最優先要做的一項。

---

## 1. 前置需求

與 Claude Code 相同：**Node.js ≥ 18**（收工檢查 hook 是 Node 寫的）。
Node 通常是機器層安裝、需要管理員權限；受管電腦要請管理員（IT）協助。

```bash
node --version    # 要 v18 以上
```

---

## 2. 安裝與登入

```bash
npm install -g @openai/codex
codex --version
```

登入走 `codex` 互動式流程（ChatGPT 帳號或 API key）。

> 版本號請自己跑 `codex --version` 記下來 —— 本文**不寫死版本**，因為
> hook 與 skill 這兩塊還在快速變動，寫死的版本號過期時不會有任何工具報錯。

---

## 3. 設定檔：三層

| 層 | 位置 | 放什麼 |
|---|---|---|
| 系統 | 由管理員派送 | 組織政策 |
| 使用者 | `~/.codex/config.toml` | 你個人的偏好，跨所有專案 |
| **專案** | `<repo>/.codex/config.toml` | **ChiaoFlow 用的就是這層** —— 進版控，跟著專案走 |

**重點：高層不會覆蓋低層的 hook。** 各層符合條件的 hook 會**一起執行**，
所以專案層加的兩個 hook 不會被你個人的設定蓋掉。

### 與 Claude Code 的對照

| | Claude Code | Codex CLI |
|---|---|---|
| 專案設定 | `.claude/settings.json` | `.codex/config.toml` |
| 格式 | JSON | TOML |
| 守則檔 | `CLAUDE.md` | **`AGENTS.md`** |
| 個人層不進版控的檔 | `.claude/settings.local.json` | `.codex/*.local.toml` |

> ChiaoFlow 的守則正本就是 `AGENTS.md`，Codex 原生讀得到，不需要額外接線。
> Claude 那邊則靠 `CLAUDE.md` 裡一行 `@AGENTS.md` 匯入指過來。

---

## 4. Hooks：⭐ 與 Claude 最大的操作差異

### 4.1 要先 trust 才會執行

Codex **不會執行沒被信任過的 hook**，而且**不會報錯，只是安靜地不跑**。

```
/hooks     # 在 session 裡：檢視來源、審閱內容、trust
```

信任是綁**腳本雜湊**的 —— **腳本改過就要重新 trust**。
這點很容易中招：你照 [core/安裝.md](../core/安裝.md) 改完 `TRIGGERS`，
hook 就變成「未信任」狀態，於是收工檢查安靜地停止工作。

> ⚠️ 這是 Codex 下「看起來裝好了其實沒裝」的頭號原因。
> 每次改過 `.agents/hooks/` 底下的腳本，都回來跑一次 `/hooks`。

### 4.2 ChiaoFlow 用到的兩個事件

| 事件 | 腳本 | 做什麼 |
|---|---|---|
| `Stop` | `.agents/hooks/doc-sync-check.mjs` | 收工前檢查文件已回填。**與 Claude 共用同一支** |
| `PreToolUse` | `.agents/hooks/design-guard.mjs` | 擋住對 `doc/DESIGN.md` 的寫入 |

**為什麼 Stop hook 能共用**：Codex 與 Claude 的契約相同 ——
stdin 都給 `cwd` 與 `stop_hook_active`，stdout 都吃
`{"decision":"block","reason":…}`。所以那支腳本一個字都不用改。

### 4.3 ⚠️ PreToolUse 不支援「跳框問人」

Claude 的 `permissions.ask` 會跳確認框讓人當場裁決。
Codex 的 PreToolUse **只支援 `allow` 與 `deny`** —— 官方把 `"ask"` 標成
*parsed but not supported yet*，也就是**寫了不會報錯，只會安靜地不生效**。

所以 ChiaoFlow 在 Codex 下改用「硬擋 ＋ 解鎖檔」：

```bash
touch doc/.design-unlock     # 人授權這一次的 DESIGN 修改
# ...改完...
rm doc/.design-unlock        # 立刻刪掉
```

`doc/.design-unlock` **必須在 `.gitignore` 裡**（starter 已經寫好）——
它一旦被 commit，這層保護就對所有人永久失效，而且不會有任何症狀。

---

## 5. Skills：放在哪

| 範圍 | 位置 |
|---|---|
| 專案 | `<repo>/.agents/skills/<name>/SKILL.md` ⚠ 待實機確認 |
| 個人 | `~/.codex/skills/` 或 `~/.agents/skills/` |

ChiaoFlow 的 `doc-sync` 正本放在 `.agents/skills/doc-sync/SKILL.md`
（工具中立的位置），Claude 那邊用 `.claude/skills/doc-sync/SKILL.md` 的
四行 stub 指過來。

> ✅ **2026-09-12 實測（0.154.0-alpha.6.2）：`.agents/skills/` 掃得到**，
> `doc-sync` 有出現在 skills 清單裡，所以**不需要 `.codex/skills` stub**。
> 若未來某版掃不到，就在 `.codex/skills/doc-sync/SKILL.md` 放一份**同樣的 stub**
> （指回 `.agents/` 的正本），**不要複製正本內容** ——
> 複製出來就會開始漂移，而漂移不會有任何工具報錯。

SKILL.md 的格式是開放標準（frontmatter 的 `name` ＋ `description`），
兩種工具都吃。**AI 平常只看得到 `description` 那一行**，所以 stub 的
`description` 必須與正本一字不差，否則 skill 會被漏叫。

---

## 6. 裝完要做的探測（取代「驗證版本號」）

`.codex/config.toml` 裡有兩個標了 `⚠ 待實機確認` 的值。用一支拋棄式 hook 確認：

把 `[[hooks.Stop.hooks]]` 的 `command` 暫時換成：

```toml
command = 'sh -c "cat > /tmp/probe.json; env | grep -i codex >> /tmp/probe.json; pwd >> /tmp/probe.json"'
```

跑一輪任意對話，然後看 `/tmp/probe.json`：

| 要確認什麼 | 看哪裡 | 確認後怎麼改 |
|---|---|---|
| ⚠️ **`CODEX_PROJECT_DIR` 存不存在**（唯一還沒驗的） | `env` 那幾行 | 不存在就把 `command` 的路徑改成相對路徑（若 `pwd` 是專案根）或絕對路徑 |
| ✅ `.agents/skills/` 掃不掃得到 | 問 AI「有哪些 skill 可用」 | 0.154 已確認掃得到；掃不到才補 `.codex/skills/` 的 stub |

探測完把 `command` 改回來，**並重新 `/hooks` trust**。

> ### ⚠️ 探測時不要把 `CODEX_HOME` 指向專案裡的 `.codex/`
>
> 那樣 Codex 會把它當成自己的 home，在裡面生出 `state_*.sqlite`、`logs_*.sqlite`、
> `installation_id`、`shell_snapshots/` 等一大包執行期狀態 —— 混在移植包裡，
> 而且會被 `cp -r starter/. <專案>/` 一起複製出去。
> starter 的 `.gitignore` 已經擋掉這些檔名，但**最好一開始就別指過去**。
> 專案層設定是 Codex 自己會讀的，不需要設 `CODEX_HOME`。

---

## 7. 踩坑清單

| 坑 | 症狀 | 解法 |
|---|---|---|
| **hook 沒 trust** | 完全沒反應，不報錯 | `/hooks` 檢視並信任 |
| **改過腳本沒重新 trust** | 本來會擋，改完 `TRIGGERS` 後安靜失效 | 同上。改腳本 → 重新 trust，變成固定動作 |
| **以為 `"ask"` 會跳框** | 寫了 ask，規格正本完全沒被保護，且不報錯 | 用 deny ＋ 解鎖檔（見 4.3） |
| **`doc/.design-unlock` 被 commit** | 保護對所有人永久失效，無症狀 | 確認 `.gitignore` 有那一行；`git status` 看不到它 |
| **解鎖檔用完沒刪** | 同上，只是範圍限本機 | 建 → 改 → 刪，當成一次性手勢 |
| **在 `.codex/` 與 `.agents/` 各放一份 SKILL.md 正本** | 兩份慢慢漂移，AI 讀到哪一份不確定 | 正本只留 `.agents/`，另一邊放 stub（0.154 實測根本不需要 stub） |
| **`matcher` 列舉工具名** | 版本一改名就整個漏擋，**沒有症狀** | 用 `.*` 全收，過濾交給腳本（0.154 的命令工具叫 `exec_command`，不是 `shell`） |
| **把 `CODEX_HOME` 指向專案裡的 `.codex/`** | 執行期狀態檔混進移植包 | 不要設；專案層設定 Codex 自己會讀 |
| **同一事件多個 hook 互相期待** | Codex 併發執行同事件的 hook，彼此擋不到對方 | 一個 hook 只負責一件事 |

---

## 8. 完成檢查清單

- [ ] `node --version` ≥ 18
- [ ] `codex --version` 有輸出（版本號自己記下來）
- [ ] 已登入
- [ ] 專案裡有 `.codex/config.toml`，兩個 `[[hooks.*]]` 區塊都在
- [ ] 已用 `/hooks` trust 兩支 hook
- [ ] 第 6 節的探測做完，`⚠ 待實機確認` 的值都改成實際值，並重新 trust
- [ ] 改 `doc/DESIGN.md` 會被擋；`touch doc/.design-unlock` 後放行
- [ ] `git status --porcelain -uall | grep design-unlock` 沒有輸出
- [ ] 問 AI「有哪些 skill 可用」答得出 `doc-sync`
