# Obsidian 環境

> **選用（L1）。** 沒有 Obsidian，`doc/` 用 git ＋ grep 一樣完整運作 ——
> 這份加的是**閱讀增益**：反向連結、關係圖、改名時自動更新所有引用。
> **前提**：先完成 [安裝.md](安裝.md)。
> **預計耗時**：15 分鐘。

Obsidian 的 vault 就是一個裝 `.md` 的普通資料夾，**沒有專有格式**。
所以它才能當可選的閱讀器 —— 裝了是加分，拿掉不會壞掉任何東西。

---

## 1. 安裝與開啟 vault

1. 下載安裝 Obsidian 桌面版：https://obsidian.md/download
2. 首次開啟選「**開啟資料夾作為保險庫**」（Open folder as vault）
3. 選專案根目錄下的 **`doc/`**
4. 跳過所有帳號登入提示

> **關於 Obsidian Sync**：那是官方的付費同步服務（$4 USD/月起）。
> **本流程不需要，我們用 git 同步。** 安裝後看到的登入視窗直接關掉，
> 不啟用完全不影響其他任何功能。

> ⚠️ **Unity 專案：vault 開在專案根的 `doc/`，不要放 `Assets/` 底下。**
> Unity 會把 `Assets/` 裡的 `.md` 當 TextAsset 匯入、替每個檔產生 `.meta`，
> 連 `.obsidian/` 都會被掃。vault 會被 meta 檔洗版。

---

## 2. ⭐ 四項必要設定

**這一節是整份文件最重要的部分。** 設錯的後果不是報錯，是**產出一批只有在
Obsidian 裡才點得動的連結** —— 在 GitHub、編輯器、以及 AI 眼中它們全都是壞的，
而且沒有任何東西會告訴你。

> **如果你是照 [安裝.md](安裝.md) 複製 `starter/` 過來的，
> `doc/.obsidian/app.json` 已經帶了正確設定，這一節請當作「驗證」用。**
> 從零建的 vault 才需要手動設定。

**設定 → 檔案與連結（Files and links）**：

| # | UI 項目 | 要設成 | `app.json` 對應鍵 | 為什麼 |
|---|---|---|---|---|
| 1 | **Use [[Wikilinks]]** | **關閉** | `"useMarkdownLinks": true` | `[[道具表]]` 不帶路徑。Obsidian 靠內部索引解析，**其他任何工具都只能猜**；vault 裡一出現同名檔就歧義；GitHub 與編輯器都點不開 |
| 2 | **New link format** | **`Path from current file`** | `"newLinkFormat": "relative"` | 產生 `../decisions/xxx.md`，是標準 Markdown 語意，Obsidian／GitHub／編輯器三邊都解得對 |
| 3 | **Automatically update internal links** | **開啟** | `"alwaysUpdateLinks": true` | 改名或搬移檔案時自動改寫所有引用。這把「引用壞了不會有工具報錯」變成工具保證 |
| 4 | **Default location for new attachments** | **`Same folder as the note`** | `"attachmentFolderPath": "./"` | 預設的 Vault folder 會把所有圖倒進 `doc/` 根目錄，跟筆記混在一起 |

### 第 2 項要特別小心：三個選項有兩個是錯的

| 選項 | 產生什麼 | 結果 |
|---|---|---|
| `Shortest path when possible` | `xxx.md` | ❌ **預設值**。跨資料夾時只寫檔名 —— 等於 wikilink 的問題換個皮 |
| `Path from vault folder` | `decisions/xxx.md` | ❌ **最容易選錯的一個**，見下 |
| `Path from current file` | `../decisions/xxx.md` | ✅ **選這個** |

`Path from vault folder` 產生的字串**長得跟相對路徑一模一樣，語意卻不同** ——
它是從 vault 根算的。假設你在 `doc/gotchas/某坑.md` 裡連到 `doc/decisions/某決策.md`：

- 它寫出 `decisions/某決策.md`
- Obsidian 從 vault 根解析 → ✅ 正常
- GitHub 與編輯器從**當前檔案所在資料夾**解析 → 找 `doc/gotchas/decisions/某決策.md` → ❌ 404

在 Obsidian 裡完全看不出問題。又是一個安靜壞掉的形式。

> 標籤在不同版本略有出入（有些文件寫成 "Relative path to file"）。
> **以「從目前檔案起算」的那一個為準**，不要只認字面。

### 驗證：對 `app.json`

改完**把設定視窗關掉**，然後打開 `doc/.obsidian/app.json`，應該有這四個鍵：

```json
{
  "useMarkdownLinks": true,
  "newLinkFormat": "relative",
  "alwaysUpdateLinks": true,
  "attachmentFolderPath": "./"
}
```

⚠️ **兩個容易誤判的地方**：

1. **`useMarkdownLinks` 的鍵名方向與 UI 開關相反** —— UI 上「Use [[Wikilinks]]」**關閉**，
   對應的鍵值是 `true`（意思是「使用 Markdown 連結」）。看到 `true` 不要以為設反了。
2. **Obsidian 不會即時寫檔** —— 要切換到別的設定頁或關閉設定視窗才落盤。
   「改了但 `app.json` 沒變」通常只是還沒寫下去，不是沒設定成功。

**鍵不存在 = 還是預設值。** 四個鍵少任何一個，就是那一項沒設到。

### 再驗證一次：實際建兩個連結

在 `doc/gotchas/` 和 `doc/decisions/` 各建一篇測試筆記，互相連結，然後用**記事本**打開：

- ✅ `[某決策](../decisions/測試.md)` —— 正確
- ❌ `[[測試]]` —— 第 1 項沒關
- ❌ `[某決策](decisions/測試.md)` —— 第 2 項選成了 `Path from vault folder`

測完把測試筆記刪掉。

---

## 3. `.gitignore`

照 [安裝.md](安裝.md) 複製過來的 `.gitignore` 已經含這幾行：

```gitignore
doc/.obsidian/workspace.json
doc/.obsidian/workspace-mobile.json
doc/.obsidian/cache
```

⚠️ **只排除這三個，`.obsidian/` 的其他部分要進版控。**

`app.json`（連結設定）、外掛設定、模板設定進版控，團隊成員的環境才會一致 ——
否則協作者的 vault 可能還在用 wikilink，兩邊產出的連結格式就分岔了。
排除的只有 `workspace.json` 這類「每開關一次分頁就變動」的個人工作區狀態。

---

## 4. 外掛：先只裝需要的

Obsidian 的**核心功能**（反向連結、關係圖、未連結提及、屬性面板）**全部內建、零外掛**，
這一層就是 L1 的全部價值。

| 外掛 | 什麼時候才需要 |
|---|---|
| **Importer** | 只有要做 [Notion匯入.md](Notion匯入.md) 才需要 |
| **Dataview** | 想要人看的自動彙整視圖時。**先讀下一節的警告** |
| **Templater** | 想讓新筆記自動套骨架時 |

裝完記得按「**啟用**」—— **安裝不等於啟用**，這是最常見的「裝了怎麼沒作用」。

> **最常見的坑不是任何一個設定，是花三週調外掛而不是寫文件。**
> 先用內建功能跑一週，真的覺得缺什麼再回來加。

---

## 5. 踩坑清單

| 坑 | 現象 | 原因 | 解法 |
|---|---|---|---|
| **Dataview／Bases 的結果 AI 讀不到** | AI 說「沒有任何決策記錄」，但 Obsidian 裡明明有一整張表 | Dataview 是**執行時查詢**，`.md` 裡存的只有查詢語句，資料是開啟頁面時掃 frontmatter 算出來的，**從來沒被寫進檔案** | frontmatter 是正本，Dataview 只做人看的視圖。資料不得只存在於查詢結果裡 |
| **wikilink 沒有路徑** | 連結在 Obsidian 點得動，在 GitHub 上是純文字 | `[[xxx]]` 只有名字沒有位置 | 見第 2 節第 1 項 |
| **偽相對路徑** | 連結在 Obsidian 正常，在 GitHub 404 | `Path from vault folder` 產生的字串與相對路徑同形不同義 | 見第 2 節第 2 項 |
| **vault 放進 `Assets/`** | 每個 `.md` 旁邊冒出 `.meta`，`.obsidian/` 也被 Unity 掃 | Unity 把 `Assets/` 裡的 `.md` 當 TextAsset 匯入 | vault 開在專案根的 `doc/` |
| **安裝 ≠ 啟用** | 外掛裝好了但沒作用 | 安裝與啟用是兩個動作 | 裝完到第三方外掛清單按「啟用」 |
| **`.obsidian/` 整個排除或整個進版控** | 前者協作者的連結格式跟你不一樣，後者每次開關分頁都有 diff | 排除範圍抓錯 | 只排除 `workspace.json` / `workspace-mobile.json` / `cache` |
| **圖片檔名帶空格** | 轉成 Markdown 連結後圖裂掉 | 空格在 URL 裡不合法 | URL 編碼：`![](image%201.png)` |
| **設定改了但 `app.json` 沒變** | 對照設定檔以為沒生效 | Obsidian 不即時寫檔 | 切換設定頁或關閉設定視窗後再看 |
| **Obsidian Sync 的登入視窗** | 以為要付費才能用 | 那是另外的付費同步服務 | 直接關掉，本流程用 git |

---

## 6. 完成檢查清單

- [ ] vault 開在 `doc/`（**不是** `Assets/`，也不是 `Docs/`）
- [ ] `app.json` 四個鍵齊全且值正確
- [ ] 實際建兩篇跨資料夾筆記互連，記事本打開看到的是 `[標題](../xxx/yyy.md)`
- [ ] `.gitignore` 只排除三個 workspace 檔，`app.json` 有進版控
- [ ] 需要的外掛已**啟用**（不只是安裝）
- [ ] 知道 Dataview 的產出不是正本

---

## 7. 常見問題

**Q：不裝 Obsidian 會少什麼？**
少反向連結面板、關係圖、改名自動更新引用。文件本身完全一樣 ——
它們就是普通的 `.md`，用任何編輯器讀寫都行。

**Q：`doc/.obsidian/` 可以刪掉嗎？**
可以。刪掉之後 Obsidian 會用預設值重建，但**你會失去那四項設定** ——
下次寫的連結又會變成 wikilink。要刪的話請確認整個團隊都不用 Obsidian。

**Q：反向連結面板是空的**
反向連結只在有人真的寫連結時才存在。它不會腐爛，但也不會自己長出來 ——
entry 要連到決策、決策要連到被它推翻的那一則。

**Q：可以用 Obsidian 的每日筆記（Daily notes）當 devlog entry 嗎？**
可以，把每日筆記的資料夾設成 `devlog/`、日期格式設成 `YYYY-MM-DD` 即可。
但 frontmatter 還是要自己補（或用 Templater 套模板）。
