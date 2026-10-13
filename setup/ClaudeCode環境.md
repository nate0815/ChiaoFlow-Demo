# Claude Code CLI 環境

> **必要（0 組｜地基）。** A 組（文件體系）的三層自動化裝置、B 組（圖與簡報）的外掛，
> **全部踩在這上面**。這份沒做完，其他兩組都不用開始。
> **預計耗時**：15 分鐘（含登入與驗證）。

本文對照的版本：**2.1.246**（2026-08-26 量測）。

> **用 Codex CLI 的話看 [CodexCLI環境.md](CodexCLI環境.md)。** [Core](../core/) 兩種工具通用 ——
> 守則、收工檢查腳本、回填流程都是同一份，差別只在規格正本的保護方式與 hook 要不要先信任。
> Extras 的兩個外掛路線（diagram-design、frontend-slides）則是 Claude Code 專屬。

---

## 1. 前置需求：Node.js

Claude Code 用 Node 跑，這是唯一的硬前置。

```bash
node --version    # 要 v18 以上
npm --version
```

| 情況 | 怎麼辦 |
|---|---|
| 有 Node ≥ 18 | 直接跳到第 2 節 |
| 沒有，或版本太舊 | ⚠️ **受管電腦不能自行安裝 Node**，要請管理員（IT）協助 |

> **Node 通常是機器層安裝**（`C:\Program Files\nodejs`），需要管理員權限。
> 但**下一節的 Claude Code 本身不需要** —— 它裝在你的使用者資料夾底下。
> 所以要申請的只有 Node 這一項，講清楚會比較好過。

---

## 2. 安裝：兩條路，先走 npm 這條

### 2.1 npm 全域安裝（建議）

```bash
npm install -g @anthropic-ai/claude-code
```

⭐ **這條不需要本機管理員權限。** npm 的全域目錄預設在你的使用者資料夾：

```bash
npm config get prefix     # 應該指到 %APPDATA%\npm，不是 Program Files
```

指到 `C:\Program Files\...` 的話會裝失敗（權限不足）。改指到使用者資料夾：

```bash
npm config set prefix "$APPDATA/npm"
```

### 2.2 原生版（選用）

```bash
claude install          # 或 claude install latest / claude install <版號>
```

裝的是不依賴 npm 的原生建置。**已經用 2.1 裝起來的話不需要做這步** ——
兩條路二選一就好，不要兩個都裝（`claude` 會指到哪一個變得不確定）。

### 2.3 驗證

```bash
claude --version        # 印出版號 = 裝好了
claude doctor           # 檢查安裝健康度
```

`claude` 找不到的話看第 6 節第一條 —— 幾乎一定是 PATH。

---

## 3. 登入

```bash
claude          # 首次啟動會帶你走登入流程
```

| 指令 | 用途 |
|---|---|
| `claude auth` | 管理登入狀態（登入／登出／查目前身分） |
| `claude setup-token` | 建立長效權杖。**需要 Claude 訂閱**，用在排程或 CI 這類沒有人在旁邊點的場景 |

> 一般互動使用**不需要** `setup-token`，直接 `claude` 登入就好。

---

## 4. 設定檔：三層，弄清楚哪一層放什麼

| 檔案 | 範圍 | 進版控？ |
|---|---|---|
| `~/.claude/settings.json` | **你這個人**，所有專案共用 | 不適用（在使用者資料夾） |
| `<專案>/.claude/settings.json` | **這個專案**，團隊共用 | ✅ **要進** —— 移植包的權限規則與 hook 就靠它 |
| `<專案>/.claude/settings.local.json` | 這個專案，**只有你** | ❌ **不要進** —— 裡面是你按過的權限記錄，帶給別人只會製造雜訊 |

`.gitignore` 要有這一行（移植包複製過去的那份已經含了）：

```gitignore
.claude/settings.local.json
```

### 常用設定鍵

```json
{
  "model": "opus[1m]",
  "effortLevel": "xhigh",
  "permissions": {
    "ask":   ["Edit(doc/DESIGN.md)"],
    "allow": ["Bash(git status:*)"],
    "additionalDirectories": ["C:\\Users\\<你>\\.claude"]
  },
  "statusLine": { "type": "command", "command": "node \"<腳本路徑>\"" },
  "enabledPlugins": { "diagram-design@diagram-design": true }
}
```

| 鍵 | 做什麼 | 誰在用 |
|---|---|---|
| `permissions.ask` | 指定路徑被改寫時**強制跳確認框**，任何權限模式都繞不過 | ⭐ A 組的權威層。見 [README.md](../README.md)「三層裝置怎麼運作」 |
| `permissions.allow` | 免確認的白名單 | 你自己按出來的 |
| `additionalDirectories` | 允許存取專案外的資料夾 | 需要讀 `~/.claude/` 時 |
| `hooks` | 註冊 hook（例如收工前檢查文件） | ⭐ A 組的觸發層。見 [安裝.md](../core/安裝.md) |
| `enabledPlugins` / `extraKnownMarketplaces` | 外掛與來源 | B 組 |
| `model` / `effortLevel` | 模型與推理強度 | 個人偏好 |

> ## ⚠️ 改完 `settings.json` 要重開 session 才生效
>
> 這是安裝移植包時最常見的「照做了但沒作用」。**改完就重開。**

---

## 5. Skill、外掛、MCP：放在哪、怎麼被叫到

### 5.1 放在哪

| 東西 | 使用者層（所有專案） | 專案層（跟著 repo 走） |
|---|---|---|
| **Skill** | `~/.claude/skills/<名字>/SKILL.md` | `<專案>/.claude/skills/<名字>/SKILL.md` |
| **Hook 腳本** | — | `<專案>/.claude/hooks/*.mjs` |
| **外掛** | `/plugin marketplace add …` ＋ `/plugin install …` | — |
| **MCP server** | `claude mcp add …` | 同左，可指定範圍 |

專案層的 skill **跟著 repo 一起交給別人**，這正是移植包裡 `doc-sync` 的做法 ——
複製過去就有，不用每個人自己裝。

> ⚠️ **上表是 Claude Code 本身的規則；ChiaoFlow 的 starter 刻意偏離了它。**
> 為了讓 Codex CLI 共用同一份，hook 腳本與 `doc-sync` 正本放在工具中立的
> `<專案>/.agents/` 底下，`<專案>/.claude/skills/doc-sync/SKILL.md` 只留一個
> 指回去的 stub。Claude Code 照樣掃得到那個 stub，行為不變。
> 理由見 [../core/安裝.md](../core/安裝.md)。

> ⚠️ **第三方外掛市集預設不會自動更新。** 裝完要手動開：
> `/plugin` → **Marketplaces** → 選市集 → **Enable auto-update**。
> 不開的話你會停在安裝當天的版本，而且**不會有任何提示**。
> 詳見 [圖表工具.md](../extras/圖表工具.md) 第 2 節。

### 5.2 ⭐ 怎麼叫用：講話，或打斜線指令

有兩種方式，**差別只有一個：誰做決定。**

| 你打的 | 誰決定用哪個 skill | 會不會漏 |
|---|---|---|
| **自然語言**（「幫我畫張架構圖」） | **AI 判斷** | 有可能沒叫到，**而且不會通知你** |
| **斜線指令**（`/diagram-design:diagram-design`） | **你指定** | 不會漏 |

**斜線指令怎麼打**：把游標移到輸入框**最前面**，按一下 `/`（斜線鍵），
畫面會跳出可用指令的清單；繼續打幾個字會自動過濾，用上下鍵選、按 Enter 送出。

格式是 `/<外掛名>:<skill 名>`。外掛只裝一個 skill 時兩段會同名，
看起來像講了兩次 —— 那是正常的，沒打錯。

> ⚠️ **`/` 一定要在訊息的最前面。** 打在句子中間（「幫我用 /xxx 做簡報」）
> 它只是一個普通的字，不會觸發。打了 `/` 沒跳清單，通常是游標不在最前面或前面有空格。

#### 什麼時候該用哪個

**平常直接講話就好，這是正常用法。** 只有兩種時候改打斜線指令：

| 時機 | 怎麼判斷 |
|---|---|
| **你講了，但感覺它沒用到那個工具** | 回應裡沒有出現該 skill 的特徵 —— 它該產出的格式、它該問你的問題 |
| **有兩個 skill 都可能符合，你要指定其中一個** | 例如同時裝了兩套簡報工具 |

### 5.3 為什麼會漏叫：AI 只看得到 `description` 那一行

決定要不要叫某個 skill 的時候，AI 看到的**不是 skill 的內容**，
只有名字 ＋ frontmatter 的 `description`。SKILL.md 本體是**決定要用了之後才載入**的。

所以能不能被自然語言叫到，**完全由 `description` 寫得好不好決定，
跟 skill 本身做得多好無關。**

> **失敗的樣子**：你說「幫我畫個流程圖」，skill 沒被叫到，
> AI 就用一般能力回你一個看起來合理的答案 ——
> **不會有任何東西告訴你「有個更適合的工具剛剛沒被叫到」。**
>
> 又是一個沒有症狀的失敗形態，跟 [README.md](../README.md)「這套東西解決什麼問題」的第三種病同源。

**判準**：你講的話裡，有沒有出現 `description` 裡的詞？有就會中，沒有就不一定。

這也是為什麼 diagram-design 的 `description` 要把 39 種圖型名稱一個個列出來 ——
上游有一份 ADR 專門講這件事，還寫了 CI 檢查：**新增一種圖型卻沒改 `description` 就讓 build 失敗**。
理由跟 [README.md](../README.md)「文件的物理形態」那條原則一樣：把「壞了不會報錯」換成「會報錯」。

#### 自己寫 skill 時

`description` 是**路由面**，不是簡介。要把**使用者實際會講出來的詞**都塞進去，
不要只寫「這個 skill 做 X」。

```
❌ description: 產生圖表
✅ description: 產生流程圖、架構圖、時序圖、甘特圖、組織圖…；
   當使用者說「畫一張圖」「這段畫成圖」「把 Mermaid 轉成正式的圖」時使用
```

### 5.4 裝越多的代價：常駐 vs 觸發

```bash
claude plugin details <外掛名>       # 看元件清單與預估 token 成本
```

輸出分兩種成本（2026-08-26 量測，數字會隨版本變動）：

| | 什麼時候付 | 實測 |
|---|---|---|
| **常駐（always-on）** | **每個 session 都付** | diagram-design（6 個 skill）約 521 tok；frontend-slides（1 個）約 123 tok |
| **觸發（on-invoke）** | 該 skill 真的被叫到時 | 主 skill 約 9.7k～15k tok |

**常駐的就是那行 `description`，本體要觸發才付。**
所以裝一堆 skill 的成本不是線性爆炸 —— **真正的成本是選錯或沒選到。**

### 5.5 檢查有沒有重複安裝

同一個 skill 可能同時存在於使用者層與外掛層，**兩份都會載入、都在付常駐成本**，
而且斜線指令會出現兩個很像的選項。

```bash
ls ~/.claude/skills/            # 使用者層
claude plugin list              # 外掛層
```

兩邊出現同名的就是重複了。**留外掛那份**（會跟著市集更新），
刪掉 `~/.claude/skills/<同名>/`。

---

## 6. 踩坑清單

| 坑 | 現象 | 原因 | 解法 |
|---|---|---|---|
| **`claude` 找不到** | `command not found` | `%APPDATA%\npm` 不在 PATH | 重開終端機；還是不行就把該路徑加進**使用者層**環境變數（不是系統層，那個要管理員） |
| **npm prefix 指到 Program Files** | `npm install -g` 權限不足 | 預設值被改過 | `npm config set prefix "$APPDATA/npm"` |
| **改了 `settings.json` 沒作用** | 權限規則、hook 都沒動靜 | 沒重載 | **重開 session** |
| **權限白名單裡出現亂碼條目** | `allow` 裡有 `\345\225\237...` 或 `Mermaid��` 這種東西 | 指令含中文檔名，終端機是 cp950 而 Claude Code 存 UTF-8，兩邊對不上 | 那些條目**永遠比不中，形同死條目**。清掉，改用不含中文的路徑或用 glob |
| **明明裝了 skill，卻沒被用到** | 回應裡沒有那個工具的特徵（產出格式、它該問的問題） | 你講的話裡沒有出現該 skill `description` 裡的詞 —— AI 判斷時只看得到那一行 | 當下改打斜線指令（5.2）；長期解是改寫 `description`（5.3） |
| **同一個 skill 裝了兩次** | 斜線清單出現兩個很像的選項；常駐 token 白付一份 | 使用者層 `~/.claude/skills/` 與外掛層各一份 | 5.5。留外掛那份 |
| **`.ps1` hook 跑不起來** | 未簽章被企業原則擋 | 企業原則要求數位簽章 | ⭐ 這就是移植包的 hook 用 **Node（`.mjs`）**而不是 `.ps1` / `.sh` 的原因 |
| **PowerShell 指令報 "core types"** | `Only core types are supported in this language mode` | 撞到約束語言模式（CLM） | 改用不涉及自訂型別的寫法，或改用 Bash。**不要要求使用者自行解除 CLM** |
| **JSON 裡的 Windows 路徑寫成單反斜線** | `settings.json` 整份失效，權限規則與 hook 全部沒作用 | JSON 字串裡 \ 是跳脫字元，`C:\Users` 不是合法 JSON | 寫成 `C:\\Users\\…`，或直接用正斜線 `C:/Users/…` |
| **`settings.local.json` 被 commit** | 協作者拿到一堆你按過的權限 | 忘了加 `.gitignore` | 第 4 節。`git rm --cached` 移掉 |
| **兩種安裝方式都裝了** | 版本對不上、更新了但沒變 | npm 版與原生版並存 | 留一個。`which -a claude` 看有幾個 |
| **`doc/` 沒 commit 前 hook 恆通過** | 裝好了但從來沒擋過 | 未追蹤檔在 `git status` 裡恆為有異動 | 見 [安裝.md](../core/安裝.md) 第 3 節 |

---

## 7. 更新與健檢

```bash
claude update      # 檢查並安裝更新
claude doctor      # 安裝健康度檢查
```

session 裡用 `/doctor` 會做更完整的檢查，而且**能順手修掉問題**。

---

## 8. 完成檢查清單

- [ ] `node --version` ≥ 18
- [ ] `claude --version` 印得出版號
- [ ] `npm config get prefix` 指在使用者資料夾（走 npm 路線的話）
- [ ] 登入完成，`claude` 進得去
- [ ] 知道三層設定檔各放什麼，且 `settings.local.json` 已被 `.gitignore` 排除
- [ ] 知道**改完 settings 要重開 session**
- [ ] 知道第三方外掛市集的自動更新要手動開
- [ ] ⭐ 知道**講話**與**斜線指令**的差別，以及什麼時候該改打斜線（5.2）
- [ ] 跑過 `ls ~/.claude/skills/` ＋ `claude plugin list`，確認沒有重複安裝（5.5）
