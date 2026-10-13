---
type: gotcha
date: 2026-09-12
scope: build
---

# Codex 的 PreToolUse 寫了 `"ask"` 不會報錯，但規格正本完全沒被保護

**現象**

把 Claude Code 的權威層移植到 Codex 時，最直覺的做法是照抄語意 ——
`permissions.ask` 是「跳框問人」，PreToolUse 也有 `permissionDecision`，
那就填 `"ask"`。

設定載入不報錯，`/hooks` 看得到，hook 也確實被執行了。
**但 AI 改 `doc/DESIGN.md` 完全不會被擋，也不會跳任何框。**
整層保護是空的，而一切看起來都正常。

**原因**

Codex 官方文件對 PreToolUse 的輸出欄位寫得很清楚：

> `permissionDecision: "ask"`, legacy `decision: "approve"`, `continue: false`,
> `stopReason`, and `suppressOutput` **are parsed but not supported yet.**

「parsed but not supported」是最糟的組合 —— **它會通過解析**，所以沒有錯誤訊息；
但**行為不存在**，所以等同於沒寫。實際可用的只有 `allow` 與 `deny`。

這正是本包第 0 節講的第三種病：壞掉了，但不會有任何東西告訴你。
而且它壞在**保護規格正本**這一層，也就是整套體系的骨幹。

**解法**

改用「硬擋 ＋ 解鎖檔」。`design-guard.mjs` 一律回 `deny`，
除非 `doc/.design-unlock` 存在：

```js
if (existsSync(resolve(join(root, UNLOCK)))) allow()

deny([
  `${SPEC} 是規格正本，不得自行改寫來遷就實作。`,
  // …叫它去升報，並告訴人怎麼授權
].join('\n'))
```

人要授權就 `touch doc/.design-unlock`，改完 `rm`。

**兩個連帶的坑**

| 坑 | 症狀 | 對策 |
|---|---|---|
| 解鎖檔被 commit | 保護對所有人永久失效，**無症狀** | 進 `.gitignore`，列為[不變式第 8 條](../TECH.md) |
| hook 沒被 trust | Codex **安靜地不執行**未信任的 hook；改過腳本也會失去信任 | 每次改 `.agents/hooks/` 就回 `/hooks` 重新 trust |

第二個在安裝時特別容易中招：照 [../../../core/安裝.md](../../../core/安裝.md)
改完 `TRIGGERS`，hook 就變回未信任狀態 —— 於是收工檢查從那一刻起安靜停擺。

**一條可以帶走的判準**

移植一個保護機制到另一個工具時，**不要驗「設定有沒有被接受」，要驗「它有沒有真的擋下來」**。
前者會過，後者才是你要的。本包的驗證 A 就是為此存在。

相關決策：[../decisions/2026-09-12-雙適配-Claude-與-Codex.md](../decisions/2026-09-12-雙適配-Claude-與-Codex.md)
