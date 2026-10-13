---
type: decision
date: 2026-08-24
status: 生效
supersedes: 2026-08-20-道具資料用-JSON
affects: [Loot, Inventory]
code: [Assets/Scripts/Loot/LootTable.cs]
---

# 道具資料改用 ScriptableObject

**選了什麼**

`ItemDef` 改成 `ScriptableObject`，一個道具一個資產檔，掉落表用 SO 陣列引用。

**推翻了什麼**

[2026-08-20-道具資料用-JSON.md](2026-08-20-道具資料用-JSON.md)。

**為什麼推翻**

原本的判斷（「上百個資產檔會很難找」）在實際跑了四天之後被兩件事蓋過去：

1. **designer 改一個掉落權重要重開 Unity。** JSON 在 `StreamingAssets` 裡，
   編輯器不會熱重載，一天下來重開十幾次。
2. **打錯欄位名不會報錯。** `"stackLimit"` 打成 `"stacklimit"` 時反序列化拿到預設值 0，
   遊戲照跑，症狀是「這個道具堆不起來」—— 查了半天才發現是 typo。

SO 兩個問題都沒有：Inspector 直接改、欄位名由編譯器保證。

至於「難找」，用資料夾分類 ＋ Project 視窗搜尋就夠了，不是真問題。

**如果錯了會怎樣**

要做線上熱更新時得整個換掉。目前判斷本專案不做熱更新（見 [../PLAN.md](../PLAN.md)「核心判斷」）。

**代價**

SO 是共用實例，執行期改它的欄位會有 Editor 與 build 行為不一致的問題 ——
已列為不變式，見 [../TECH.md](../TECH.md)「不變式」與
[../gotchas/2026-08-25-ScriptableObject-在-Editor-會保留執行期修改.md](../gotchas/2026-08-25-ScriptableObject-在-Editor-會保留執行期修改.md)。
