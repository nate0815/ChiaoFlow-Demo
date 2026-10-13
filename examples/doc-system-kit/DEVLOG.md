# doc-system-kit — 開發日誌（DEVLOG）

> **本檔是入口，不是全部。** 時序 entry、決策、踩坑各自**一則一檔**，
> 放在 [devlog/](devlog)、[decisions/](decisions)、[gotchas/](gotchas)。

---

## 1. 專案基本資料

| 項目 | 內容 |
|---|---|
| 專案名稱 | **ChiaoFlow**（repo 名仍是 `doc-system-kit`） |
| 目的 | 一套帶得走的文件體系，讓文件不落後於程式、規格不被實作侵蝕 |
| 期間 | 2026-08-05 起 |
| 產出形式 | **Core**（`core/`，要複製的在 `core/starter/`）＋ **Extras**（`extras/`）＋ 地基（`setup/`）＋ 手冊（`README.md`）＋ 範例（`examples/`） |
| 規格正本 | [DESIGN.md](DESIGN.md) |

---

## 3. 技術評估

| 方案 | 評估結果 | 為什麼選／為什麼不選 | 對應決策 |
|---|---|---|---|
| Obsidian 當體系地基 | 不採用 | 移植成本從 10 分鐘變半天 | [2026-08-25-Obsidian-降級為可選閱讀器](decisions/2026-08-25-Obsidian-降級為可選閱讀器.md) |
| Obsidian 當可選閱讀器 | **採用** | 反向連結取代手工索引表，而 L0 完全不依賴它 | 同上 |
| Dataview 產生決策表 | 不採用 | AI 讀到零筆而且不報錯 | [gotchas/2026-08-25-Dataview-的結果-AI-讀不到](gotchas/2026-08-25-Dataview-的結果-AI-讀不到.md) |
| 與正式規格流程整合成一套 | 不採用 | 範圍、受眾、節奏三個基數都對不上 | [2026-08-26-不與正式規格流程整合](decisions/2026-08-26-不與正式規格流程整合.md) |
| diagram-design 產圖 ＋ Mermaid 匯入 | **採用** | HTML 路徑零額外安裝，Mermaid 抽取是純本機解析、不連網 | [2026-08-26-周邊工具選型](decisions/2026-08-26-周邊工具選型.md) |
| frontend-slides 做簡報 | **採用（主線）** | MIT、外掛安裝、產出單檔 HTML 零相依 | 同上 |
| Marp 做簡報 | **採用（備線）** | 原始碼是純 Markdown 可進版控；`npx` 免全域安裝；匯出要的瀏覽器 Windows 已內建 | 同上 |
| Anthropic 官方 pptx skill | 不採用 | Proprietary 授權。⚠️ 2026-08-27 更正：**建檔不需要** LibreOffice／Poppler，那兩個只用在縮圖與驗證 —— 擋掉它的是授權那一條 | [2026-08-27-簡報流程改成規劃先於出片](decisions/2026-08-27-簡報流程改成規劃先於出片.md) |
| PowerPoint 自己的大綱匯入 | **採用（零安裝路線）** | 吃 tab 縮排的 `.txt`，套當前範本母片、真正可編輯。不吃圖與講者備忘 | 同上 |
| 自寫 `outline-to-pptx.py` | **採用（主線）** | 只依賴 `python-pptx`；填的是真的 placeholder，所以大綱檢視看得到 | 同上 |
| pptx-from-layouts-skill（MIT） | 不採用，當藍本 | 形狀正確但 23 ★ 太薄，不當相依 | 同上 |
| claude-office-skills | 不採用 | 授權未標明 ＋ 要 LibreOffice／Poppler／Pandoc | 同上 |
| PlantUML 當產圖主線 | 不採用 | 本機算圖要 Java ＋ Graphviz；伺服器模式等於把圖送到外部伺服器 | 同上 |
| archify 產有實據的系統圖 | **採用（窄用途）** | MIT、純 Node 無外部執行檔、程式碼零網路請求。實測**路徑與行號都真的會對 commit 驗證**，假引用擋得下來 —— diagram-design 做不到這件事 | [2026-08-28-archify-收進來但定位寫窄](decisions/2026-08-28-archify-收進來但定位寫窄.md) |
| archify 的 DeepSeek 整合 | 不採用 | 社群版不是官方，而且會把東西送到外部服務。核心功能不需要它 | 同上 |
| diagram-design 同時裝外掛與 skill 兩份 | 收斂成外掛版 | skill 版是 2.6（舊）且**不是 git clone、沒有任何更新路徑**；外掛版 2.6.6 有自動更新，SOP 寫的也是它 | 同上 |

---

## 6. 待決問題（Open Questions）

| # | 問題 | 為什麼重要 | 狀態 |
|---|---|---|---|
| 1 | 連結檢查要不要接進 CI | 「跨檔引用不寫章號」目前只能靠自律，有 CI 就能變成機制 | ⚠️ 2026-08-28：**手動的那支已經有了**（`core/工具/連結檢查.py`，實掃 51 個 `.md`、真正壞掉 0 條、10 條刻意的示範佔位已排除）。剩下的是接進 CI |
| 2 | DESIGN 單檔在正式專案規模下會不會塞不下 | 四份文件體系抽自一週的 prototype，正式專案的 GDD 可能撐不住 | 先維持單檔，塞不下再說 |
| 3 | 簡報規劃的三個閘門要不要做成 skill | 場合卡與大綱表**確實有東西可以擋**，這讓「B 組不做自動化裝置」沒那麼絕對 | 先手動跑幾次，判準驗過再說（[2026-08-27-簡報流程改成規劃先於出片](decisions/2026-08-27-簡報流程改成規劃先於出片.md)） |
| 4 | 簡報 SOP 那兩條規則要不要正式改 | 硬規矩第 2 條與「要對方回答的」對單向分享場合不適用，這一版是刻意偏離 | 跑過第三份再回頭看（[2026-08-28-簡報SOP對單向分享場合的兩處偏離](decisions/2026-08-28-簡報SOP對單向分享場合的兩處偏離.md)） |
| 5 | archify 的實據功能只支援 GitHub，非 GitHub 的私有 repo 怎麼辦 | 那是它唯一的差異化賣點，私有 GitLab／自架 server 完全用不了 | 未解。要嘛只用在公開 repo，要嘛放棄實據只用它的驗證器 |
| 6 | `${CODEX_PROJECT_DIR}` 是否存在還沒實機驗證 | 兩個 hook 都用它定位腳本，不存在的話會**無聲失效** | ⚠️ 2026-09-12 **部分收斂**：Codex 0.154.0-alpha.6.2 已驗過 config 可解析、`.agents/skills/` 掃得到、兩支 hook 行為正確；`matcher` 的問題已修（改 `.*`）。**只剩這一項** —— 當時 session 連不到 OpenAI 端點，走不到 Stop 階段。探測步驟見 [setup/CodexCLI環境.md](../../setup/CodexCLI環境.md) 第 6 節 |
| 7 | hotfix 漏合回 `main` 要不要機制化 | 這是分支規則裡**唯一沒有症狀**的一條 ——只合進 `stable` 的話，下次發佈會把修正蓋回去，bug 原地復活，而你會在使用者回報時才發現 | 未解。目前只有文字護欄（[core/分支與發佈.md](../../core/分支與發佈.md)標成「最常被漏掉的一步」）。真要機制化，該做的是**發佈前檢查 `git log stable ^main` 有沒有東西**，不是再加一個 hook（[2026-09-12-分支模型與發佈流程](decisions/2026-09-12-分支模型與發佈流程.md)） |

---

## 8. 上層依據與既有設計約束

- 歸納自個人 side project（Game Jam 與短期 prototype）；直接的起點是其中一個 prototype（2026-08-05 起，為期一週）
- 與團隊的正式規格文件流程是**接力不是並行**，
  交棒規則見 [decisions/2026-08-26-不與正式規格流程整合.md](decisions/2026-08-26-不與正式規格流程整合.md)
