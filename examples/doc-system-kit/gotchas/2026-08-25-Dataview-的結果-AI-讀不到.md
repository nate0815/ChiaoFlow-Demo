---
type: gotcha
date: 2026-08-25
scope: tooling
---

# Dataview 的表格在 Obsidian 裡有兩列，AI 讀到零筆

**現象**

用 Dataview 做了一張決策總表，Obsidian 裡顯示得好好的。
叫 AI 「查一下目前最大的決策編號」，它回答「沒有任何決策記錄」。

**沒有錯誤訊息。** 它會拿這個答案繼續做 —— 例如從 D1 開始重新編號。

**原因**

Dataview 是**執行時查詢**，跟 SQL 的 view 一樣：`.md` 檔裡存的是查詢語句，
不是結果。結果是 Obsidian 開啟那一頁的當下、掃描全 vault 的 frontmatter
即時算出來畫在畫面上的，**從來沒有被寫進檔案**。

用 `cat` 打開那個檔，看到的全文只有：

```
# 決策總表

```dataview
TABLE date AS 日期, title AS 決策, status AS 狀態
FROM "decisions"
WHERE type = "decision"
SORT date ASC
```
```

零筆資料。不是少了幾筆，是一筆都沒有。

`.base` 檔（Obsidian Bases）與 `dataviewjs` 完全同理。

**解法**

**frontmatter 是正本，Dataview／Bases 只是人看的視圖。任何資料都不得只存在於查詢結果裡。**

資料本身沒有消失 —— 它在每則筆記自己的 frontmatter 裡，AI grep 得到。
要一覽就用 `ls doc/decisions/` 與 `grep -L "status: 已推翻" doc/decisions/*.md`。

> **判準**：關掉 Obsidian、用記事本打開那個檔，**看不到的東西 AI 也看不到。**
> 這條同時管住 [wikilink 那個坑](2026-08-25-wikilink-不帶路徑.md) 與跨檔章號。
