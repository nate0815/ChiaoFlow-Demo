> ℹ️ **這是範例資料夾裡的說明檔，不是 ChiaoFlow 的 README。**
> 這個 repo 真正的進站點是根目錄的 [../../README.md](../../README.md)。
> 要看「一般專案的 README 填完長什麼樣」，去
> [../unity-道具掉落/README.md](../unity-道具掉落/README.md)。

---

# 這個 repo 自己的 README 是個例外

一般專案的 README 是**薄的進站點**：這是什麼、怎麼跑起來、文件在哪，
深度內容一律留在 `doc/`（規範見
[core/starter/.agents/skills/doc-sync/SKILL.md](../../core/starter/.agents/skills/doc-sync/SKILL.md)
的「README 的必備章節」）。

**ChiaoFlow 這個 repo 沒有照這個形狀寫**，根目錄那份是五百多行的手冊。
這裡要老實講為什麼，否則照抄的人會以為「README 就是要這樣寫」。

## 為什麼是例外

| | 一般專案 | 這個 repo |
|---|---|---|
| 產出物是什麼 | 程式 | **文件本身** |
| README 的角色 | 指向產出物與 `doc/` 的進站點 | **它就是產出物的一部分** |
| 「怎麼跑起來」 | 一段可複製的指令 | 沒有東西可以跑 —— 對應的是 [core/安裝.md](../../core/安裝.md) |
| 深度內容放哪 | `doc/` | 手冊只講**為什麼**，步驟外包給各資料夾自己的 `README.md` |

所以它薄不下來：把「為什麼這樣設計」搬進 `doc/`，這個 repo 就只剩一包沒有理由的設定檔。

## 但它仍然遵守同一條紀律

**同一件事不寫在兩處。** 根 README 第 1 節明寫「本手冊不維護第二份清單 ——
維護兩份的下場是它們一定會分岔」，安裝步驟也不在手冊裡複製一份。
薄 README 的「只放指標」跟手冊的「只講為什麼」，擋的是同一件事。

## 判準

> **你的 README 如果過期了，誰會先發現？**
>
> 答案是「改程式的人」→ 那段內容該在 `doc/TECH.md`，README 只放連結。
> 答案是「沒人」→ 那段內容本來就不該存在。

這個 repo 的答案是「讀手冊的人」，因為手冊就是產品。
**你的專案多半不是這種情況。**

---

## 這個資料夾裡的其他檔

`DESIGN.md`／`PLAN.md`／`TECH.md`／`DEVLOG.md` 與 `devlog/` `decisions/` `gotchas/`
是 ChiaoFlow 開發過程的**真實紀錄** —— 看真實的決策鏈長什麼樣，從
[DEVLOG.md](DEVLOG.md) 進去。
