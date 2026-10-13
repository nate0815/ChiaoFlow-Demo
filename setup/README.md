# setup/ — 地基

> **給誰**：要把 ChiaoFlow 裝起來的人。
> 這兩份是 **[Core](../core/) 與 [Extras](../extras/) 的共同前置** ——
> 但**不是整組都必要**，看你要用到哪些功能。

---

## 你該讀哪一份

**AI CLI 擇一即可**（兩個都裝也行，ChiaoFlow Core 兩邊通用）：

| 你的情況 | 要讀 | 大約耗時 |
|---|---|---|
| 用 Claude Code —— 想弄清楚設定檔哪一層放什麼，或**想知道 skill 怎麼被叫到** | **[ClaudeCode環境.md](ClaudeCode環境.md)** ⭐ | 15 分鐘 |
| 用 Codex CLI —— `config.toml` 三層、hook 的信任機制 | **[CodexCLI環境.md](CodexCLI環境.md)** ⭐ | 15 分鐘 |
| 要用 Mermaid／draw.io 匯入、PNG 匯出、匯入現成 `.pptx` | ＋ [Python環境.md](Python環境.md) | 5–20 分鐘 |

> **兩個都裝的話兩份都讀**，但重點在差異：Codex 的 hook **要先 trust 才會執行**，
> 而且規格正本的保護方式與 Claude 不同。兩份各自有一張對照表。

> ⚠️ **Python 不是必要的。** Core 完全不需要它，Extras 的主線（產 HTML 圖與 HTML 簡報）
> 也不需要。撞到「找不到 python」再回頭讀那一份就好。

---

## 前置需求

**要申請管理員權限的只有一項**（Node.js）。其餘全部裝得進使用者資料夾。

| 項目 | 誰需要 | 要管理員權限嗎 | 細節 |
|---|---|---|---|
| Git | Core 全部 | 通常已裝 | 文件跟著專案一起版控 |
| **Node.js ≥ 18** | Core 全部；Extras 只有 Marp | ⚠️ **要** —— 請管理員（IT）協助 | 收工檢查 hook 是 Node 寫的 |
| **Claude Code 或 Codex CLI**（擇一） | 全部 | ❌ 不用（裝在 `%APPDATA%/npm`） | [ClaudeCode環境.md](ClaudeCode環境.md)／[CodexCLI環境.md](CodexCLI環境.md) |
| Python 3 | 只有匯入／PNG 匯出 | ❌ 不用（單一使用者安裝） | [Python環境.md](Python環境.md) |
| 瀏覽器（Chrome／Edge／Firefox） | 只有 Marp 要匯出 PDF／PPTX | ❌ 不用 | **Windows 11 內建 Edge，實務上不用另外做事** |
| Obsidian 桌面版 | 只有 L1 閱讀增益 | 受管電腦依組織政策 | 免費，https://obsidian.md/download |
| Notion 帳號 | 只有要匯入 | — | 免費方案即可 |

> **為什麼 hook 用 Node 而不是 `.ps1` 或 `.sh`**：受管的企業環境常因未簽章而不能跑 `.ps1`，
> `.sh` 在 Windows 又依賴 Git Bash。Node 兩邊都通 —— 這也讓同一支腳本能同時服務
> Claude Code 與 Codex CLI。
