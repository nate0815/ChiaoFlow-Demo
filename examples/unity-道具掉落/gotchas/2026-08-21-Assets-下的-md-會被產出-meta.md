---
type: gotcha
date: 2026-08-21
scope: tooling
---

# `Assets/` 下的 .md 每個都冒出一個 .meta

**現象**

把 vault 開在 `Assets/Docs/` 之後，每寫一篇筆記，旁邊就多一個 `.meta`；
`.obsidian/` 資料夾裡的設定檔也全部被產了 meta。git diff 一片紅。

**原因**

Unity 會把 `Assets/` 底下**所有**檔案當成資產匯入，`.md` 變成 TextAsset，
每個匯入的資產都要有 `.meta` 記錄 GUID。它不知道 `.obsidian/` 是設定資料夾。

**解法**

vault 開在**專案根目錄**的 `doc/`，不要放 `Assets/` 底下。
Unity 只掃 `Assets/`、`Packages/`、`ProjectSettings/`，根目錄的其他資料夾它不管。

已產生的 meta 檔：把 vault 搬出去之後，`.meta` 會變成孤兒，
Unity 下次開啟時會自動清掉。
