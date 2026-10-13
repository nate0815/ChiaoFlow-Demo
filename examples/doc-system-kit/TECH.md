# doc-system-kit — 技術實作參考（TECH）

> **定位**：**實際怎麼實作的** 的正本。**要改程式就看這份。**
> 與 [DESIGN.md](DESIGN.md) 牴觸時以 DESIGN 為準；如果是程式偏離了規格，
> **停下來回報，不要改 DESIGN 去遷就它。**

---

## 0. 檔案清單

| 檔案 | 職責 | 行數 |
|---|---|---|
| `core/starter/.agents/hooks/doc-sync-check.mjs` | 收工前檢查文件已回填。**Claude Code 與 Codex CLI 共用同一支** | ~120 |
| `core/starter/.agents/hooks/design-guard.mjs` | 規格正本的寫入保護（**只有 Codex 用**，Claude 用原生 `permissions.ask`） | ~110 |
| `core/starter/.agents/skills/doc-sync/SKILL.md` | 回填路由表與升報格式（正本） | ~215 |
| `core/starter/AGENTS.md` | 給 AI 的工作守則（**正本**，工具中立） | ~70 |
| `core/starter/CLAUDE.md` | Claude 接線：`@AGENTS.md` 匯入 ＋ 專屬補充 | ~13 |
| `core/starter/.claude/settings.json` | 權限規則 ＋ 註冊 Stop hook | 24 |
| `core/starter/.claude/skills/doc-sync/SKILL.md` | stub，指回 `.agents/` 的正本 | ~16 |
| `core/starter/.codex/config.toml` | Codex 接線：註冊 Stop 與 PreToolUse 兩個 hook | ~35 |
| `extras/簡報/工具/outline-to-pptx.py` | 大綱 → 樸素 pptx。網址自動變超連結；字寬用單位制（中文一字兩單位） | ~420 |
| `extras/簡報/工具/themed-pptx.py` | 大綱 → **帶視覺的**可編輯 pptx。底圖 ＋ 原生形狀 ＋ 真 placeholder | ~290 |
| `extras/簡報/工具/html-deck.py` ＋ `deck-shell.html` | 大綱 → HTML 簡報（固定 1920×1080 舞台、URL 錨點） | ~110 ＋ ~490 |
| `extras/簡報/工具/density-check.py` | 密度檢查：點數、字寬（單位制）、主張是否完整句 | ~60 |
| `core/工具/連結檢查.py` | 掃全 repo 的相對連結，排除刻意的示範佔位 | ~45 |

---

## 1. 30 秒驗證 ⭐

```bash
echo '{"hook_event_name":"Stop","cwd":"<專案絕對路徑>","stop_hook_active":false}' \
  | node .agents/hooks/doc-sync-check.mjs; echo "[exit=$?]"
```

乾淨工作區應該無輸出、`exit=0`。

---

## 4. 模組契約 ⭐

### 4.1 `doc-sync-check.mjs`

| 對外介面 | 作用 |
|---|---|
| stdin JSON → stdout JSON | 收 `{hook_event_name, cwd, stop_hook_active}`，回 `{decision:"block", reason}` 或無輸出 |

**誰能呼叫**：Claude Code 與 Codex CLI 的 Stop hook（**同一支腳本，兩邊共用**）
**不能做什麼**：**不得修改任何檔案**。它只做判斷與擋 —— 內容由 AI 在對話裡寫，
人看得到也能當場否決。

> 兩種工具的 Stop hook 契約相同，所以這支不需要分歧：stdin 都給 `cwd` 與
> `stop_hook_active`，stdout 都吃 `{decision:"block", reason}`。

### 4.2 `design-guard.mjs`

| 對外介面 | 作用 |
|---|---|
| stdin JSON → stdout JSON | 收 `{cwd, tool_name, tool_input}`，回 `{hookSpecificOutput:{hookEventName:"PreToolUse", permissionDecision:"deny", permissionDecisionReason}}` 或無輸出 |

**誰能呼叫**：Codex CLI 的 PreToolUse hook。**Claude Code 不用這支** —— 它有原生的
`permissions.ask`，會跳確認框讓人當場裁決，比硬擋好。

**判斷順序**：工具名不像寫檔 → 放行；payload 沒提到 `doc/DESIGN.md` → 放行；
shell 類但沒有寫入跡象（`>`、`sed -i`、`tee`…）→ 放行；`doc/.design-unlock` 存在 → 放行；
其餘 → deny。

**註冊方式**：`matcher = ".*"` 全收（見「不變式」第 10 條），由腳本自己快速放行。

**已知限制**（寫在腳本檔頭，不是 bug）：
- 對 patch／edit 類工具可靠；對 shell 只能比對指令字串，**擋不全**。
  設計上偏向「寧可漏擋也不要誤擋」，所以比對不到一律放行。
- ⚠️ **解鎖檔是協作慣例與防呆，不是安全邊界。** 腳本會擋掉「用工具建立解鎖檔」
  這條最直接的路，但有 shell 與寫入權限的 agent 理論上仍有別的辦法繞過去。
  它擋的是「忘記」與「順手」，不是惡意。

---

## 5. 不變式 ⭐⭐ 破壞這些會壞掉，而且不一定馬上看得出來

| # | 不變式 | 保護哪個檔／符號 | 破壞後的症狀 |
|---|---|---|---|
| 1 | `git status` 一定要帶 `-uall` | `doc-sync-check.mjs` 的 `execFileSync` | 未追蹤的整個 `doc/` 只輸出一行 `?? doc/`，底下的檔抓不到 → 閘門誤判為「已回填」而放行 |
| 2 | `git` 一定要帶 `-c core.quotepath=false` | 同上 | 非 ASCII 檔名被跳脫成 `\345\225\237...`，比對不到 → 中文檔名的專案閘門失效 |
| 3 | `stop_hook_active` 為 true 時必須 `exit 0` | `doc-sync-check.mjs` 迴圈守門 | 連續擋 8 次會被 Claude Code 強制覆蓋，中間一直鬼打牆 |
| 4 | 任何例外都要靜默 `exit 0` | `bail()` | 檢查工具自己壞掉（不是 git repo、git 不在 PATH）就卡住工作 |
| 5 | **`GATE` 的比對必須支援目錄前綴** | `doc-sync-check.mjs` 的 `matches()` | 拆檔後回填動的是 `doc/devlog/*.md`，`doc/DEVLOG.md` 不動 → **閘門恆擋**，見 [gotchas/2026-08-26-hook-閘門是嚴格相等比對.md](gotchas/2026-08-26-hook-閘門是嚴格相等比對.md) |
| 6 | **`.agents/hooks/` 底下的腳本必須同時滿足兩種工具的 hook 契約** | `doc-sync-check.mjs` | 只照一邊改（例如改用 Claude 專屬的輸出欄位），另一邊會**安靜地不生效** —— 它不會報「欄位不認得」，只會當成沒有回應而放行 |
| 7 | **stub 的 `description` 必須與正本一字不差** | `core/starter/.claude/skills/doc-sync/SKILL.md` | AI 平常只看得到 `description` 那一行。改短或改寫會讓 skill 被漏叫，而**漏叫沒有任何症狀** |
| 8 | **`doc/.design-unlock` 必須留在 `.gitignore`** | `core/starter/.gitignore` | 一旦被 commit，Codex 那層規格保護就對**所有人、所有時候**永久失效，且不會有任何症狀 |
| 9 | **`design-guard.mjs` 比對不到一律放行** | `design-guard.mjs` | 反過來寫（比對不到就擋）會在 Codex 換工具名時把所有寫入全擋掉，讓人直接把整個 hook 拔掉 —— 拔掉之後連該擋的也不擋了 |
| 10 | **`.codex/config.toml` 的 `matcher` 必須是 `.*`，不可列舉工具名** | `core/starter/.codex/config.toml` | matcher 在 hook 被呼叫**之前**過濾。列舉的話，CLI 一改工具名就整個漏擋，而**單測餵 stdin 會繞過 matcher，照樣全綠**。見 [gotchas/2026-09-12-matcher-列舉工具名會整個漏擋.md](gotchas/2026-09-12-matcher-列舉工具名會整個漏擋.md) |
| 11 | **解鎖檔的檢查必須排在 shell 快速放行之前** | `design-guard.mjs` | 那個快速放行只認「針對 DESIGN.md 的寫入跡象」，`touch doc/.design-unlock` 不會命中 → 被當成讀取放行 → AI 可以自己造一把鑰匙 |
| 12 | **同一個過濾條件不要實作在兩層；真要的話外層寬、內層嚴** | `config.toml` 的 `matcher` ↔ `design-guard.mjs` 的 `WRITE_TOOLS` | 外層嚴的話會安靜吃掉內層判斷，而內層的測試看不到外層。第 10 條是這條的一個實例 |

> 這一節收的都是**違反後還能跑、但已經壞了**的約束。
> 會立刻爆錯的不用寫 —— 錯誤訊息會告訴你。

---

## 9. 刻意沒做的事

| 沒做 | 為什麼 |
|---|---|
| 在這個 repo 的根目錄裝 `.claude/` | hook 會在編輯移植包本身時自己叫起來擋人。所以它放在 `core/starter/` 底下 |
| 為 Claude Code 也裝 `design-guard.mjs` | 它有原生的 `permissions.ask`，**跳框問人比硬擋好** —— 人可以當場點頭。硬擋是 Codex 的妥協，不是更好的設計 |
| 把 `.agents/skills/` 的正本也複製一份到 `.codex/skills/` | 複製出來就會漂移，而漂移不會有任何工具報錯。要就放 stub |
| Extras 的雙工具適配 | Route A 與 diagram-design 是 Claude Code plugin，沒有對等的 Codex 路線。已在文件裡標明，不假裝等價 |
| CI 連結檢查 | 還沒做。一支零相依的 Node 腳本就夠：走訪 `.md`、抽相對連結、確認目標存在 |

---

## 10. 本輪變更收件匣 ⭐ 回填先進這裡

> 暫存區，不是正式章節。永遠放在最後一節 —— 新增它不會讓任何既有章號位移。
> ⚠️ **新的不變式不進收件匣，直接寫 §5。**

### 10.2 目前收件匣

- （→ §4 模組契約）`GATE` 從字串改為陣列，比對邏輯抽成 `matches(f, list)` 與 TRIGGERS 共用
- （→ ?）`template/doc/.obsidian/app.json` 隨移植包一起發，讓 L1 的連結設定零成本正確
- （→ §0 檔案清單）新增 `.agents/`（兩種工具共用的正本）、`.codex/config.toml`（Codex 接線）
- （→ §4 模組契約）`design-guard.mjs` 的 `specPattern` 用 `[/\\]+`（分隔符後面要 `+`）：
  `JSON.stringify` 會把 Windows 路徑的 `\` 轉義成 `\\`，只吃一個會漏掉 Windows 形式的路徑
- （→ ?）`.codex/config.toml` 只剩一個 `⚠ 待實機確認` 的值：`CODEX_PROJECT_DIR`。
  Codex 0.154.0-alpha.6.2 已驗過其餘各項（config 可解析、`.agents/skills/` 掃得到、
  兩支 hook 行為正確）。**`CODEX_PROJECT_DIR` 確認後要回來清掉這一條**
- （→ §4 模組契約）`matcher` 從列舉工具名改成 `.*`；`SHELL_WRITE` 補 `touch`／`install`
- （→ §4 模組契約）`design-guard.mjs` 新增解鎖檔自建防線（`unlockPattern`），
  且該檢查必須排在 shell 快速放行之前
- （→ ?）starter 的 `.gitignore` 新增一整段：擋掉 `CODEX_HOME` 被誤指到專案 `.codex/`
  時生出的執行期狀態檔（sqlite／logs／installation_id／shell_snapshots…）
- （→ ?）`連結檢查.py` 現在要掃三個點開頭資料夾（`.agents/`、`.claude/`、`.codex/`），
  `os.walk` 那條註解已更新
- （→ §0 檔案清單）新增 `core/starter/README.骨架.md` —— 根目錄 README 的骨架。
  **刻意不叫 `README.md`**：安裝第一步是 `cp -r starter/. <專案>/`，同名的話會無聲覆蓋
  專案既有的 README。它會被使用者刪掉，所以章節規範的正本不在它裡面，在
  `doc-sync/SKILL.md` 的「README 的必備章節」
- （→ ?）`README.md` 一直在 `doc-sync-check.mjs` 的 `TRIGGERS` 裡，但**不在 `GATE` 裡**，
  也沒有任何存在性檢查 —— 這是刻意的：`GATE` 是回填閘門，README 是被回填的對象
