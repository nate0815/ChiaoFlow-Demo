# 道具掉落與背包 — 開發日誌（DEVLOG）

> **本檔是入口，不是全部。** 時序 entry、決策、踩坑各自**一則一檔**，
> 放在 [devlog/](devlog)、[decisions/](decisions)、[gotchas/](gotchas)。
> 落點規則、frontmatter 欄位、查詢指令的完整版見移植包的 [core/starter/doc/DEVLOG.md](../../core/starter/doc/DEVLOG.md) §0。

---

## 1. 專案基本資料

| 項目 | 內容 |
|---|---|
| 專案名稱 | 道具掉落與背包 |
| 目的 | 驗證自動拾取的手感，以及 20 格背包夠不夠用 |
| 期間 | 2026-08-19 起 |
| 負責人 | <負責人> |
| 驗收標準 | 見 [PLAN.md](PLAN.md)「驗收方式」 |
| 規格正本 | [DESIGN.md](DESIGN.md) |

---

## 3. 技術評估

| 方案 | 評估結果 | 為什麼選／為什麼不選 | 對應決策 |
|---|---|---|---|
| JSON 檔 | 先採用，後推翻 | designer 改一個值要重開 Unity | [2026-08-20-道具資料用-JSON](decisions/2026-08-20-道具資料用-JSON.md) |
| ScriptableObject | **採用** | Inspector 直接編輯，型別安全 | [2026-08-24-道具資料改用-ScriptableObject](decisions/2026-08-24-道具資料改用-ScriptableObject.md) |
| Addressables ＋ 遠端資料 | 不採用 | 本專案不做熱更新，複雜度換不到東西 | —— |

---

## 6. 待決問題（Open Questions）

> 留在本檔，因為它跨檔、不屬於任何單一則 entry，而且要能一眼看完。
> 解決後標日期與結論，**不刪掉**。

| # | 問題 | 為什麼重要 | 狀態 |
|---|---|---|---|
| 1 | 背包滿了要不要給玩家提示 | 不提示的話玩家會以為拾取壞了 | 待 <負責人> 決定 |
| 2 | 掉落物的 30 秒是否夠長 | 太短會讓玩家清怪後撿不到 | 2026-08-24 → 試玩再定，先維持 30 秒 |

---

## 8. 上層依據與既有設計約束

- 專案的 SO 命名慣例：`<類別>Def`（如 `ItemDef`、`EnemyDef`）
