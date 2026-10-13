# VSCode 外掛

> **推薦清單，不是安裝清單。** 九個外掛，每一個都寫了「為什麼跟這個工具包有關」。
> **不要照單全裝。** 挑跟你手上工作有關的就好。
> 這一份跟你用 Claude Code 還是 Codex CLI 無關 —— 談的是編輯器本身。

---

## 0. ⚠️ 先看這個：你可能不能自己裝

受管電腦（網域控管、標準使用者帳號）**通常不允許自行安裝 VSCode 外掛**，
需要請管理員（IT）協助。

所以這份文件真正的用途是兩個：

1. **知道有什麼可用** —— 遇到問題時知道「這件事有外掛可以解」
2. **要申請的時候，一次講清楚申請哪幾個、為什麼** —— 而不是一個一個試

> 裝不了也不必焦慮。下面九個**沒有一個是必要的** ——
> 它們全部都只是讓事情更順，不是讓事情變成可能。

---

## 1. 怎麼看、怎麼裝、怎麼帶去下一台機器

```bash
# 看目前裝了什麼（帶版號）
code --list-extensions --show-versions

# 裝一個
code --install-extension eamodio.gitlens

# 把整台機器的清單存下來
code --list-extensions > extensions.txt

# 在新機器上一次裝回來
cat extensions.txt | xargs -L 1 code --install-extension
```

> **這幾行本身就值得寫進交接文件。** 換機器時最花時間的不是重裝，
> 是「想不起來當初裝了什麼」。

---

## 2. ⭐ 九個外掛

| ID | 做什麼 | 為什麼跟這裡有關 |
|---|---|---|
| `anthropic.claude-code` | Claude Code 的 VSCode 整合 | 整套自動化的入口。用 CLI 也可以，但 IDE 裡看得到 diff |
| `eamodio.gitlens` | 行內顯示每一行是誰、哪個 commit 改的；查檔案歷史 | ⭐ **直接對應 [README.md](../README.md)「回填為什麼會貴」** —— 回填時「為什麼」要從 commit body 抄，GitLens 讓你不用離開編輯器就查得到 |
| `vstirbu.vscode-mermaid-preview` | 預覽 Markdown 裡的 Mermaid 圖 | 決定「這張 Mermaid 要不要轉成正式圖」之前，先看得到它長怎樣。見 [圖表工具.md](圖表工具.md) 第 5 節 |
| `ms-vscode.live-server` | 本機起一個 server 並自動重整 | 預覽 diagram-design 的 HTML 圖與 HTML 簡報。**VSCode 裝不了 Marp 外掛時的替代方案** |
| `esbenp.prettier-vscode` | 統一格式化（含 Markdown、JSON） | 讓 `doc/` 的 diff 只剩真正的內容變動 |
| `natqe.reload` | 狀態列加一個「重新載入視窗」按鈕 | 改完設定或外掛要讓 VSCode 重讀時點一下就好，不用去命令面板找 `Developer: Reload Window` |
| `oderwat.indent-rainbow` | 縮排層級上色 | 防眼殘。看 frontmatter 與巢狀 JSON 時最有感 |
| `naumovs.color-highlight` | 程式碼裡的色碼直接顯示該顏色 | 調 diagram-design 品牌 token 時看得到實際顏色 |
| `streetsidesoftware.code-spell-checker` | 拼字檢查 | 文件寫多了會需要。**中文無效**，只管英文與變數名 |

### 一次裝完

```bash
code --install-extension anthropic.claude-code
code --install-extension eamodio.gitlens
code --install-extension vstirbu.vscode-mermaid-preview
code --install-extension ms-vscode.live-server
code --install-extension esbenp.prettier-vscode
code --install-extension natqe.reload
code --install-extension oderwat.indent-rainbow
code --install-extension naumovs.color-highlight
code --install-extension streetsidesoftware.code-spell-checker
```

> 只想先裝一個的話，裝 `eamodio.gitlens` —— 它是唯一一個直接對應到
> 本工具包**核心動作**（回填「為什麼」）的外掛，其餘八個都只是讓事情更順。

---

## 3. 這份怎麼維護

| 規則 | 為什麼 |
|---|---|
| **不列版號** | 版號是量測當下的快照。逐行維護一定會漏，而漏掉的地方**不會有任何工具報錯**。要看版號就跑第 1 節那行指令 |
| **加新項目前先問：這是「工具包需要的」還是「我個人習慣的」** | 這份曾經是整台機器的外掛快照（38 個，含遊戲引擎、三家 AI 助手、三個主題）。那樣的清單接手的人只能全部照裝或全部略過，兩種都沒用 |
| **每一列都要填得出「為什麼跟這裡有關」** | 填不出來的，就是屬於你個人環境的，不該進這份 |
