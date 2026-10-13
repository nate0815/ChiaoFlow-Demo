---
type: gotcha
date: 2026-08-25
scope: runtime
---

# 在 Editor 改過的道具數值，重開還在；build 版卻是原值

**現象**

測試時為了試手感，在執行期用程式改了 `ItemDef.dropWeight`。
停止播放、重開 Unity，那個值**還是改過的**。
但同一份程式 build 出來跑，每次啟動都是原本的值。

兩邊行為不同，而且**都不報錯**。

**原因**

ScriptableObject 是**資產檔的共用實例**，不是每次執行都重建的物件。
在 Editor 裡改它等於改資產檔本身，會被寫回磁碟。
Build 之後資產是唯讀的，改動只存在於記憶體，下次啟動就沒了。

這個坑危險的地方在於：你在 Editor 裡調出來的手感，**build 版根本不是那個數值**。

**解法**

**不得在執行期修改 SO 的欄位。** 需要執行期變動的狀態放在 MonoBehaviour 或
執行期的資料容器裡，SO 只當唯讀的定義。

已列入 [../TECH.md](../TECH.md)「不變式」第 2 條 —— 那一節收的就是這種
「違反後還能跑，但已經壞了」的約束。

相關決策：[../decisions/2026-08-24-道具資料改用-ScriptableObject.md](../decisions/2026-08-24-道具資料改用-ScriptableObject.md)
