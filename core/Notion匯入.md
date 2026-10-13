# 從 Notion 匯入既有文件

> **選用，而且是一次性的。**
> **前提**：先完成 [安裝.md](安裝.md) 與 [Obsidian環境.md](Obsidian環境.md)
> —— 匯入要用 Obsidian 的 Importer 外掛。
> **預計耗時**：30–90 分鐘，視資料量。

---

## 0. 先理解限制

- **這是一次性匯入，不是同步。** 匯入後 Notion 那側的修改不會過來。
- **絕對不要用 Notion 的 Markdown 匯出格式** —— 它會漏掉重要資料，而且 Notion 會在
  每個檔名後接一長串 unique ID，這些 ID 也被寫進內部連結，直接拖進 Obsidian
  會得到滿是壞連結的 vault。走 Importer 就不會有這問題。
- **原本的 Notion 內容在整個流程確認完成前，不要刪除任何東西。**

> **可以持續同步嗎？** 沒有可靠方案。社群外掛都不穩定，因為 Notion 的資料模型是 block、
> Obsidian 是純文字檔，來回轉換必然失真。
> 建議做法是**兩邊分工**：技術文件留在 `doc/`（跟程式碼綁在一起），
> 專案管理留 Notion（資料庫視圖強），兩邊都接上 MCP 讓 AI 同時讀得到，不做實際同步。
> 見 [MCP連結.md](MCP連結.md)。

---

## 1. 選擇匯入方式

| | **API 匯入**（本文採用） | 檔案匯入（HTML zip） |
|---|---|---|
| 資料庫 | 保留，轉成 Obsidian Bases，公式盡量轉換 | 不保留，變成散頁 ＋ CSV |
| 需要 token | 要 | 不用 |
| 需要網路 | 要 | 不用 |

**只要 Notion 裡有任何資料庫（表格／看板／清單），就走 API 匯入。**

---

## 2. ⚠️ 先建一個拋棄式測試 vault

**不要直接匯進 `doc/`。**

用「檔案 → 開啟其他保險庫」建一個全新空 vault（例如放在桌面的 `NotionTest`），
在那裡完成匯入與驗收，確認結果沒問題之後，**再手動把需要的檔案搬進 `doc/`**。

匯入結果通常需要整理，你會想先看看長什麼樣子。

> 測試 vault 也要照 [Obsidian環境.md](Obsidian環境.md) 設好那四項，
> 否則你驗收的是一批 wikilink，搬進 `doc/` 之後還要再轉一次。

---

## 3. 在 Notion 建立整合並取得 token

1. 開啟 Notion 整合設定頁：https://www.notion.so/profile/integrations
   （或 Settings → Connections → Developer tools）
2. 選「**New connection**」
3. 名稱隨意（例如 `Obsidian`），驗證方式選「**Access token**」，工作區選你的工作區
4. 建立後進入該連線的 **Configuration** 分頁
5. 確認 **Capabilities** 已勾選：Read content／Update content／Insert content
6. 複製 **Access token**（`ntn_` 開頭的一長串）

> 🔒 **這串 token 等同於你 Notion 帳號的鑰匙。**
> 不要貼進聊天室、issue、截圖或任何公開位置。若不慎外洩，回到同一頁面重新產生一組。

---

## 4. 授權整合存取頁面（最常漏掉的一步）

Notion 的整合**預設看不到任何內容**，必須明確授權。

- 在整合的 **Content access** 分頁中，加入你要匯入的頁面
- 或到 Notion 該頁面右上角「**⋯**」→ **Connections** → 選擇你建立的整合
- 要匯入整個工作區的話，**每個頂層頁面都要做一次**

**症狀檢查**：下一步按 Load 之後清單空空如也 → 就是這步沒做。

---

## 5. 執行匯入

1. 開啟 Importer（左側邊欄圖示，或命令面板 `Ctrl+P` 搜尋 Importer）
2. **File format** 選 `Notion (API)`
3. 貼上 `ntn_` token。若跳出 Add secret 對話框：
   - **ID** 欄位是 Obsidian 自己的標籤名稱，**只能小寫字母、數字、連字號**
     （填 `personal` 可以，`Personal` 會被擋）
   - **Secret** 欄位貼 token
4. 按 **Load**，勾選要匯入的頁面

### 建議設定

| 設定項 | 建議值 | 理由 |
|---|---|---|
| Output folder | `Notion` | 全部收在子資料夾，方便之後挑選搬移 |
| Attachment location | **Same folder as the note** | 預設的 Vault folder 會把所有圖片倒在根目錄 |
| Existing notes | `Update` | 跳過未變動的筆記、保留本地較新編輯，配合分批匯入不會產生重複檔 |
| Convert formulas | `Obsidian syntax` | 轉不過去的會退回靜態值，不會整個失敗 |
| Download external attachments | **開啟** | 外部網址圖片會抓成本地檔，避免連結失效後筆記缺塊 |
| Import linked databases | **關閉**（試跑時） | 開啟會連帶匯入你沒勾選的頁面，試跑會失去意義 |

---

## 6. 分批匯入與驗收

**第一批只勾三個頁面**：一個普通頁面、一個有子頁面的、一個資料庫。

按 Import，跑完後檢查：

- [ ] 頁面之間的連結能正常跳轉
- [ ] 圖片和附件有實際下載到本地
- [ ] 資料庫變成了 `.base` 檔
- [ ] 中文內容沒有亂碼

確認無誤後，回第 5 節匯入其餘內容。此時可考慮開啟 `Import linked databases`，
讓關聯欄位變成真正的連結而非純文字。

---

## 7. 匯入後的整理

這通常是整個遷移最花時間的部分。

### 7.1 連結格式要轉

**Importer 產出的是 wikilink**（`[[頁面名]]`、`![[image 1.png]]`），
即使 vault 設定是 Markdown 連結也一樣。搬進 `doc/` 之前要轉。

⚠️ **圖片檔名帶空格的要 URL 編碼**，否則轉完圖是裂的：

```
![[image 1.png]]   →   ![](image%201.png)
```

Obsidian 沒有內建的批次轉換工具，量少就手動改，量大要寫腳本。

### 7.2 `.base` 檔的內容 AI 讀不到

Notion 資料庫會轉成 `.base` 檔。那是**視圖定義**，列的資料是開啟時掃 frontmatter
即時算出來的 —— AI 讀 `.base` 會得到一張空表，**而且不會報錯**。

資料本身沒有消失，它在每則筆記自己的 frontmatter 裡。所以：
**frontmatter 是正本，`.base` 只是人看的視圖。** 不要把任何只存在於 `.base` 的東西
當成資料來源。

### 7.3 看板、篩選、排序不會跟著過來

需要用 Obsidian 的 Bases 或 Dataview 重建 —— 同樣只當人看的視圖。

### 7.4 搬進 `doc/`

驗收完成後，把需要的檔案從測試 vault 搬進 `doc/` 對應位置，commit。
**搬的時候順便決定它屬於哪一種**：現行規格 → `DESIGN.md`；
決策紀錄 → `decisions/`；踩坑 → `gotchas/`；歷史流水帳 → `devlog/`。

---

## 8. 完成檢查清單

- [ ] Notion integration 已建立，Capabilities 已勾選
- [ ] Content access 已授權目標頁面
- [ ] 在**拋棄式測試 vault** 完成小批次試跑並驗收
- [ ] 全量匯入完成
- [ ] wikilink 已轉成相對路徑 Markdown 連結（圖片檔名的空格已編碼）
- [ ] 需要的檔案已搬進 `doc/` 並 commit
- [ ] 測試 vault 已刪除

---

## 9. 常見問題

**Q：Importer 按 Load 之後清單是空的**
Content access 沒設定。回第 4 節。

**Q：Add secret 對話框的 ID 填不進去**
只接受小寫字母、數字、連字號。用 `personal` 而非 `Personal`。

**Q：匯入過程中 Obsidian 卡住**
先停用其他第三方外掛再試一次。

**Q：匯入大型工作區時出現巢狀 zip 錯誤**
數 GB 的匯出會產生巢狀 `.zip`。手動解開外層，再匯入內層的 `Export-{id}-Part-N.zip`。

**Q：匯入的內容太雜，不知道該搬哪些進 `doc/`**
判準是「這份東西未來會被查嗎」。個人工作日誌、會議流水帳通常不會 ——
那些留在 Notion 就好。要搬的是**規格、決策理由、踩過的坑**。
