# core/ — ChiaoFlow Core

> ⭐ **整包唯一「我真心推薦」的部分：四份文件 ＋ 一道收工前的檢查。**
> 治的是「文件落後於程式、決策的為什麼蒸發、規格被實作反向侵蝕」這三種狀況 ——
> 最麻煩的第三種**不會有人抱怨**。為什麼這樣設計見 [../README.md](../README.md)。

> ## ⭐ 要複製到你專案的是 [starter/](starter/)
>
> 複製的是**它的內容**，不是資料夾本身：
>
> ```bash
> cp -r starter/. <你的專案路徑>/
> ```
>
> 所以 `starter` 這個名字不會出現在你的專案裡。

---

## 你該讀哪幾份

**只有第一份是必要的。** 其餘的看你的專案狀況（多一份少一份都不影響前一份）。
前置是 [../setup/](../setup/) 的 AI CLI —— **Claude Code 或 Codex CLI 擇一即可，兩個都裝也行**。

| 你的情況 | 要讀 | 大約耗時 |
|---|---|---|
| 想在專案裡裝起來（所有人都從這裡開始） | **[安裝.md](安裝.md)** ⭐ 必要 | 20 分鐘 |
| 想用圖形介面讀寫文件、看反向連結與關係圖 | ＋ [Obsidian環境.md](Obsidian環境.md) | 15 分鐘 |
| 想讓 AI 同時讀得到 Unity 編輯器狀態或 Notion 內容 | ＋ [MCP連結.md](MCP連結.md) | 15 分鐘 |
| 專案既有文件在 Notion，想搬進來 | ＋ [Notion匯入.md](Notion匯入.md) | 30–90 分鐘 |
| 要開始分線開發，或要推出版本／試玩版 | ＋ [分支與發佈.md](分支與發佈.md) | 10 分鐘 |
| prototype 做完了，要交棒給正式流程或收攤 | ＋ [交棒與封存.md](交棒與封存.md) | 10 分鐘 |
| 有自產的美術素材要量產，想先統一風格與規格 | ＋ [美術指南.md](美術指南.md)（選配的第五份正本 `doc/ART.md`） | 10 分鐘 |

### 附帶的一支工具

[工具/連結檢查.py](工具/連結檢查.py) —— 掃整個 repo 的相對路徑連結，回報真正壞掉的，
並把文件裡刻意的示範佔位（`<標題>`、`xxx`、教 URL 編碼的 `image%201.png`）排除掉。

```bash
python core/工具/連結檢查.py .
```

**為什麼需要它**：壞掉的相對連結**不會報錯**（見 [../README.md](../README.md)「文件的物理形態」）。
沒有人掃就等於沒有人知道。

---

## 裝完之後長什麼樣

**先看它怎麼動**：誰觸發誰、誰擋誰、哪一份文件由誰寫。

![裝起來之後：三層裝置圍著四份文件，外面只有 git 與 Node](圖/三層裝置.svg)

| 圖上的東西 | 對應到下面目錄樹的哪裡 |
|---|---|
| 收工檢查 | `.agents/hooks/doc-sync-check.mjs` |
| doc-sync | `.agents/skills/doc-sync/SKILL.md` |
| 寫入護欄 | Claude：`.claude/settings.json` 的權限規則；Codex：`.agents/hooks/design-guard.mjs` |
| 守則 | `AGENTS.md` |
| 四份文件 | `doc/` |

為什麼是這三層、各自擋什麼，在[手冊](../README.md)的「三層裝置怎麼運作」。

**再看檔案放在哪**。以 Unity 專案為例（其他類型的專案把 `Assets/` 那幾行換掉即可）：

```
MyGame/                          ← 專案根目錄 = git repo 根目錄
├── Assets/  Packages/  ProjectSettings/
├── README.md                    ← 對外進站點：怎麼跑起來 ＋ 文件在哪。只放指標，深度在 doc/
├── AGENTS.md                    ← 給 AI 的工作守則正本（只放指標）
├── .agents/                     ← 兩種工具共用的正本
│   ├── hooks/doc-sync-check.mjs   收工檢查（Claude 與 Codex 跑這同一支）
│   ├── hooks/design-guard.mjs     規格正本的寫入保護（只有 Codex 用到）
│   └── skills/doc-sync/SKILL.md   回填流程與路由表
├── CLAUDE.md                    ← Claude 接線：一行 @AGENTS.md 匯入
├── .claude/                     ← Claude 接線
│   ├── settings.json              規格正本的權限規則 ＋ 註冊 Stop hook
│   └── skills/doc-sync/SKILL.md   四行 stub，指回 .agents/ 的正本
├── .codex/config.toml           ← Codex 接線：註冊兩個 hook
├── doc/                         ← 四份正本 ＋ 三個資料夾
│   ├── DESIGN.md                  做什麼（規格正本，改動需授權）
│   ├── PLAN.md                    為什麼選這條路
│   ├── TECH.md                    實際怎麼實作的
│   ├── DEVLOG.md                  入口：規則、基本資料、待決問題
│   ├── devlog/                    時序 entry，一天一檔
│   ├── decisions/                 一決策一檔
│   ├── gotchas/                   一坑一檔
│   └── .obsidian/               ← 只有裝 Obsidian 才會用到
└── .gitignore
```

> **只裝一種工具的話，另一邊的接線留著不會有任何影響** —— `.codex/` 對 Claude Code
> 只是一般檔案，反之亦然。但**不要因此把 `.agents/` 刪掉**，那裡才是正本。

真的裝起來長什麼樣，直接看 [../examples/](../examples/)。

> ## ⛔ `doc/` 這個目錄名不能改
>
> 它寫死在 hook 的觸發清單、`settings.json` 的權限規則、`.codex/config.toml` 與
> `design-guard.mjs` 的規格正本路徑、`doc-sync` 的路由表，以及四份文件彼此的相對連結裡。
> **改了不會報錯，只會安靜地失效。**

> ⚠️ **Unity 專案特別注意：`doc/` 放專案根目錄，不要放 `Assets/` 底下。**
> Unity 會把 `Assets/` 裡的 `.md` 當 TextAsset 匯入、替每個檔產生 `.meta`，
> 連 `.obsidian/` 設定資料夾都會被掃。vault 會被 meta 檔洗版。

---

## 圖一覽

想先用看的，從這裡開始。全部是手寫的 SVG：純文字、進版控、diff 得出來，
每張的 `<desc>` 都有一段文字說明，所以 AI 也讀得到。

| 圖 | 回答什麼 | 用在哪 |
|---|---|---|
| [三層裝置](圖/三層裝置.svg) | 裝起來之後誰觸發誰、誰擋誰 | 手冊開頭、[安裝.md](安裝.md) |
| [repo 結構](圖/repo結構.svg) | 四個資料夾各是什麼、哪個要複製 | 手冊「這個 repo 的結構」 |
| [四份文件的分工](圖/四份文件的分工.svg) | 哪種內容寫進哪一份 | 手冊「四份文件的分工」 |
| [規格衝突的分流](圖/規格衝突的分流.svg) | 發現與 DESIGN 不一致時，誰要停下來問 | 手冊「DESIGN 是唯一參照」 |
| [收工檢查的判斷](圖/收工檢查的判斷.svg) | hook 什麼時候擋、什麼時候放行 | 手冊「三層裝置怎麼運作」、[安裝.md](安裝.md) 驗證 B |
| [規格護欄的兩種擋法](圖/規格護欄的兩種擋法.svg) | Claude Code 與 Codex CLI 各自怎麼擋 | 手冊「三層裝置怎麼運作」、[安裝.md](安裝.md) 驗證 A |
| [安裝的三層內容](圖/安裝的三層內容.svg) | 複製過去的東西是什麼、各要改哪裡 | [安裝.md](安裝.md)「複製」 |
| [分支模型](圖/分支模型.svg) | 分支怎麼開、怎麼合、tag 打在哪 | [分支與發佈.md](分支與發佈.md)、手冊「為什麼分支也要有規範」 |

> ⚠️ **圖不是正本。** 規則的正本在各自的文件與腳本裡，圖只是它的畫法。
> 機制改了要回頭改圖 —— 而圖沒跟上**不會有任何工具報錯**，所以改動流程時把這張表掃一遍。
