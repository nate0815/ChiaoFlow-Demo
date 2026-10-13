# Python 環境

> **選用（0 組｜地基）。**
> ⭐ **A 組（文件體系）完全不需要 Python。** 只有 B 組的三件事會用到：
> Mermaid／draw.io 匯入、PNG 匯出、把現成 `.pptx` 當簡報素材匯入。
> **預計耗時**：已經有 Python 的話 5 分鐘（都在做確認）；要從零裝 20 分鐘。

---

## 1. 先確認你到底需不需要

| 你要做的事 | 需要 Python？ |
|---|---|
| 裝移植包、寫四份文件、收工閘門 | ❌ **不需要**（hook 是 Node 寫的） |
| 用 diagram-design 產圖、輸出 HTML／SVG | ❌ **不需要** |
| `/diagram-design:import-mermaid`、`import-drawio` | ✅ 需要 |
| 匯出 PNG | ✅ 需要（還要 Playwright） |
| frontend-slides 匯入現成 `.pptx` 當素材 | ✅ 需要（`python-pptx`） |

> **不確定就先跳過這份。** 真的撞到「找不到 python」再回來。
> 見 [圖表工具.md](../extras/圖表工具.md) 第 1 節 —— HTML 那條路完全零依賴。

---

## 2. ⭐ 第一件事：你機器上有幾個 Python

**在 Windows 上「有幾個 Python」幾乎永遠不是 1。** 先看清楚：

```bash
python  --version
python3 --version
which -a python python3 py
python  -m pip --version
python3 -m pip --version
```

### 這是本機實測的結果（2026-08-26），三個 Python 並存

| 叫得出來的名字 | 實際版本 | 實際位置 | 從哪來的 |
|---|---|---|---|
| `python` | **3.12.10** | `%LOCALAPPDATA%/Programs/Python/Python312/` | python.org 的**單一使用者安裝** |
| `python3` | **3.14.5** | `%LOCALAPPDATA%/Python/pythoncore-3.14-64/` | 由 `uv` 或 Python Manager 管理 |
| `WindowsApps/python.exe` | 3.14.5 | 指向 `PythonSoftwareFoundation.PythonManager` | Microsoft Store 的 Python Manager |

**這不是壞掉，這是 Windows 的常態。** 但它會產生下一節那個坑。

---

## 3. ⭐⭐ `python` 與 `python3` 可能不是同一個

**這是整份文件最重要的一節。**

### 症狀

```
你：pip install pypdf          → 成功
你：python3 某腳本.py          → ModuleNotFoundError: No module named 'pypdf'
```

裝成功了，但腳本說找不到。**而且錯誤訊息完全不會提到「你裝到另一個 Python 去了」。**

### 本機實測

```bash
$ python  -c "import pypdf; print('OK')"
OK

$ python3 -c "import pypdf"
ModuleNotFoundError: No module named 'pypdf'
```

同一台機器、同一分鐘。因為 `pip` 綁在 `python`（3.12）上，
而 `python3` 是另一個直譯器（3.14），**兩邊的套件目錄互不相通**。

### 為什麼這個坑特別容易踩

因為**工具的說明文件通常寫 `python3`**（那是 Linux／macOS 的慣例）。
diagram-design 的匯入說明就是寫 `python3 <skill-dir>/scripts/mermaid_extract.py`。
你照著貼上去，就跑到另一個直譯器上了。

### 三條規矩

| 規矩 | 為什麼 |
|---|---|
| ⭐ **一律用 `python -m pip install`，不要用 `pip`** | `python -m pip` 保證裝進「執行 `python` 的那一個」。裸 `pip` 是另一支執行檔，可能綁在別的直譯器上 |
| **腳本跑不動時，先問「是哪個 python 在跑」** | `python -c "import sys; print(sys.executable)"` |
| **把版本要求講清楚再選** | 要用哪一個不重要，**前後一致**才重要 |

### 診斷：一行看穿

```bash
for p in python python3; do
  echo "== $p"; $p -c "import sys;print(sys.executable);print(sys.version)"
done
```

兩段輸出的路徑不一樣 = 你有這個坑。

---

## 4. 從零安裝（沒有 Python 的話）

> ⭐ **好消息：Python 可以裝在使用者層，不需要本機管理員權限。**
> 這跟 Node.js 不同（Node 通常裝在 `C:/Program Files`，要管理員協助）。

| 方式 | 要管理員嗎 | 說明 |
|---|---|---|
| **python.org 安裝程式 ＋ 取消勾選「為所有使用者安裝」** | ❌ 不用 | 裝進 `%LOCALAPPDATA%/Programs/Python/`。**建議走這條** |
| **Microsoft Store 的 Python** | ❌ 不用 | 組織若沒鎖 Store 就可以。裝完的執行檔在 `WindowsApps/` |
| `winget` / `choco` / `scoop` | ✅ 要 | ⚠️ **受管電腦不要試**，這幾個在企業環境通常被停用 |

安裝時**務必勾選「Add python.exe to PATH」**，否則後面每個指令都要打完整路徑。

> ⚠️ **下載安裝程式前，先確認來源與雜湊。** python.org 的下載頁每個檔案都附
> SHA256。這是基本的供應鏈安全習慣，不是形式 —— 見下一節。

---

## 5. ⭐ 套件安裝與 Hash 驗證

原則：**安裝任何套件前，要確認該套件在 PyPI 或官方來源上提供 SHA256（或同等級）雜湊。**

### 查一個套件的官方 SHA256

```bash
python -c "import json,urllib.request; d=json.load(urllib.request.urlopen('https://pypi.org/pypi/pypdf/json')); f=d['urls'][0]; print(f['filename']); print('sha256:', f['digests']['sha256'])"
```

輸出長這樣（實測）：

```
pypdf-6.16.2-py3-none-any.whl
sha256: c8b09a59399062fb45a1b8156c18a787a10a3dae03ac9674397a226712c94604
```

### 讓 pip 強制驗證

```bash
python -m pip install --require-hashes -r requirements.txt
```

`requirements.txt` 每一列都要帶雜湊：

```
pypdf==6.16.2 --hash=sha256:c8b09a59399062fb45a1b8156c18a787a10a3dae03ac9674397a226712c94604
```

> ⚠️ **`--require-hashes` 是全有全無**：只要有一列沒帶雜湊就整包拒裝。
> 這是刻意的 —— 半套的驗證等於沒有驗證。

### ⚠️ 真正要小心的是「執行期才下載二進位檔」的套件

有些套件本身在 PyPI 上有雜湊，**但裝完之後會再去下載別的執行檔**。
最典型的就是 **Playwright**：`pip install playwright` 只裝了控制程式，
真正的瀏覽器是後面 `playwright install` 時另外抓的。

| 要確認的 | 怎麼辦 |
|---|---|
| 那次下載有沒有雜湊驗證機制 | **不確定就先查清楚（受管電腦先問管理員），不要先裝再說** |
| 下載會不會被防火牆擋 | 幾乎一定會跳視窗，見 [圖表工具.md](../extras/圖表工具.md) 第 6 節 |

> **卡住的替代方案**：diagram-design 的 SVG 匯出**完全不需要 Playwright**。
> 不要為了 PNG 卡在這一關 —— 用 SVG，或直接瀏覽器截圖。

---

## 6. venv：什麼時候要開

| 情況 | 開不開 |
|---|---|
| 只是要跑 diagram-design 的匯入腳本 | **不用。** 那些腳本只用標準函式庫，什麼都不必裝 |
| 要裝 `python-pptx`、`playwright` 這類套件 | **建議開**，避免污染系統 Python |
| 專案本身是 Python 專案 | **一定開** |

```bash
python -m venv .venv
source .venv/Scripts/activate      # Git Bash
python -m pip install --require-hashes -r requirements.txt
```

> Windows 的啟用腳本在 `.venv/Scripts/`（不是 Linux 的 `.venv/bin/`）。
> PowerShell 用 `.venv\Scripts\Activate.ps1` —— ⚠️ 未簽章腳本可能被企業原則擋，
> 擋住的話改用 Git Bash。

`.venv/` 記得進 `.gitignore`。

---

## 7. 這個工具包實際會用到的套件

**預設一個都不用裝。** 只有走到對應功能才需要：

| 套件 | 為了什麼 | 誰要 |
|---|---|---|
| （無） | Mermaid／draw.io 匯入 | 只用標準函式庫，**不必裝任何東西** |
| `playwright` | diagram-design 的 PNG 匯出 | 只有要 PNG 的人。⚠️ 見第 5 節 |
| `python-pptx` | frontend-slides 匯入現成 `.pptx` 當素材 | 只有要匯入舊簡報的人 |

> 這張表**刻意很短**。B 組的設計原則就是「主線零依賴」——
> 需要裝東西的都是可選路徑，而且每一條都有不裝也能走的替代方案。

---

## 8. 踩坑清單

| 坑 | 現象 | 原因 | 解法 |
|---|---|---|---|
| ⭐ **裝了但 import 不到** | `pip install` 成功，腳本卻 `ModuleNotFoundError` | `pip` 與執行腳本的直譯器不是同一個 | 第 3 節。一律 `python -m pip` |
| **`python` 打開了 Microsoft Store** | 沒安裝 Python 時的舊行為 | Windows 的應用程式執行別名 | 裝真的 Python，或到「設定 → 應用程式 → 應用程式執行別名」關掉 |
| **`python3` 在 Windows 上不存在** | `command not found` | Windows 的官方安裝只給 `python` 與 `py` | 文件寫 `python3` 的地方改打 `python`，但**先確認兩者是不是同一個** |
| **PATH 裡沒有 Python** | 裝完了還是找不到 | 安裝時沒勾「Add python.exe to PATH」 | 重跑安裝程式選 Modify 補勾 |
| **`--require-hashes` 整包失敗** | 一列沒帶雜湊就全部拒裝 | 這是刻意設計 | 補齊所有列的雜湊 |
| **Playwright 卡在下載瀏覽器** | 沒反應或被擋 | 防火牆 ＋ 企業網路 | 改用 SVG 匯出，或找管理員 |
| **PowerShell 啟用 venv 被擋** | `Activate.ps1` 無法載入 | 未簽章腳本被企業原則擋 | 改用 Git Bash 的 `source .venv/Scripts/activate` |
| **升級 Python 之後套件全不見** | 原本能跑的忽然不能跑 | 新版本有自己的套件目錄 | 這是預期行為。重裝，或早點改用 venv |

---

## 9. 完成檢查清單

- [ ] 知道**自己到底需不需要 Python**（第 1 節）
- [ ] 跑過第 2 節的診斷，知道機器上有幾個 Python
- [ ] ⭐ 知道 `python` 與 `python3` **是不是同一個**
- [ ] 已改用 `python -m pip` 的習慣
- [ ] 要裝套件的話，知道怎麼查 SHA256 並用 `--require-hashes`
- [ ] 知道 Playwright 這類「執行期才下載二進位檔」的套件要先問過
- [ ] 知道不裝 Python 也走得通的替代路徑（HTML／SVG）
