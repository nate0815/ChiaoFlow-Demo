---
type: decision
date: 2026-08-28
status: 生效
supersedes:
affects: [結構, 命名]
code: [README.md, core/, extras/, setup/, examples/]
---

# 命名為 ChiaoFlow，資料夾重整成 setup／core／extras／examples

**問題是什麼**

拿這一包做了一份導覽簡報之後，兩個辨識度問題浮出來：

1. **核心沒有名字。** 簡報上只能寫「四份文件加一道檢查」—— 描述得出來，但記不住
2. **`template/` 太通用**，而且 `sop/` 把三組東西（地基、文件體系、產出物工具）混在一起 ——
   `README.md` §1 其實已經在用文字解釋這個分組，**資料夾卻沒對上文字**

**選了什麼**

| 名字 | 指什麼 |
|---|---|
| **ChiaoFlow** | 整包 |
| **ChiaoFlow Core** | 四份文件 ＋ 收工前的檢查（`core/`） |
| **ChiaoFlow Extras** | 圖、簡報、編輯器外掛（`extras/`），全部選用 |

資料夾重整成四個，各一個概念 —— **裝什麼／主體／選配／看範例**：

| 舊 | 新 |
|---|---|
| `template/` | `core/starter/` |
| `sop/移植包安裝.md` | `core/安裝.md` |
| `sop/` 的 Obsidian／MCP／Notion 三份 | `core/` |
| `sop/` 的 ClaudeCode／Python 兩份 | `setup/` |
| `sop/` 的圖表／簡報／外掛四份 | `extras/` |
| `簡報範本/` | `extras/簡報範本/` |
| `example-vault/` | `examples/` |

**為什麼資料夾用功能名而不是品牌名**

`core/starter/` 沒有叫 `chiaoflow/`，這是刻意的。

這個資料夾真正的問題**不是「不好記」，是「有人會複製錯」** ——
導覽簡報有一整頁在講「要複製的是這個，不是那兩個範例」。品牌名不解決那個問題，功能名才解決。

而且**這個名字永遠不會進別人的專案**：安裝指令是 `cp -r starter/. <專案路徑>/`，
複製的是**內容**不是資料夾本身。所以品牌只需要活在 `README.md` 與簡報上。

**為什麼改名是安全的**

`template` 這個字**沒有寫死在任何程式或設定裡** —— hook、`settings.json`、
`SKILL.md`、`CLAUDE.md` 全部沒有。寫死的只有 `doc/`，而它在 `core/starter/doc/` 底下，
複製過去之後仍然是專案根的 `doc/`，不受影響。

**舊紀錄怎麼處理**

`decisions/` 與 `devlog/` 是只追加不改寫的：

- ✅ **只更新連結路徑** —— 連結壞掉比路徑過期更糟
- ⛔ **敘述一個字都不改** —— 舊 entry 裡寫的 `sop/`、`template/` 是當時的事實

所以讀舊紀錄看到 `template/`，指的就是現在的 `core/starter/`；看到 `sop/`，
指的是現在拆進 `setup/`、`core/`、`extras/` 的那些檔。

**沒選什麼**

- **沒有改 GitHub repo 名。** 仍然是 `doc-system-kit` —— 改名會讓
  archify 產出的 commit 永久連結全部失效，而那是它唯一的差異化功能
- **沒有把地基收進 `core/`。** Extras 也要 Claude Code CLI，收進 `core/` 會讓人
  以為只裝 Extras 就不用看

**驗證**

搬移前後都跑全 repo 相對連結檢查，基準是**真正壞掉 0 條**（另有 10 條刻意的示範佔位）。
搬完一度壞到 18 條，全部修回 0 條才收工。
