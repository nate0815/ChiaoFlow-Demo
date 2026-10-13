---
type: gotcha
date: 2026-08-26
scope: env
---

# `pip install` 成功了，腳本卻說找不到那個套件

**現象**

```
$ python -m pip install pypdf      → 成功
$ python3 某腳本.py                 → ModuleNotFoundError: No module named 'pypdf'
```

同一台機器、同一分鐘。錯誤訊息完全沒有提到「你裝到另一個直譯器去了」。

**原因**

Windows 上「有幾個 Python」幾乎永遠不是 1。本機 2026-08-26 實測有三個並存：

| 名字 | 版本 | 位置 | 來源 |
|---|---|---|---|
| `python` | 3.12.10 | `%LOCALAPPDATA%/Programs/Python/Python312/` | python.org 單一使用者安裝 |
| `python3` | **3.14.5** | `%LOCALAPPDATA%/Python/pythoncore-3.14-64/` | uv／Python Manager |
| `WindowsApps/python.exe` | 3.14.5 | 指向 `PythonSoftwareFoundation.PythonManager` | Microsoft Store |

驗證：

```
$ python  -c "import pypdf; print('OK')"     → OK
$ python3 -c "import pypdf"                  → ModuleNotFoundError
```

`pip` 綁在 `python`（3.12）上，`python3` 是另一個直譯器（3.14），**套件目錄互不相通**。

**為什麼特別容易踩**

因為工具的說明文件通常寫 `python3` —— 那是 Linux／macOS 的慣例。
diagram-design 的匯入說明就寫 `python3 <skill-dir>/scripts/mermaid_extract.py`，
照著貼上去就跑到另一個直譯器上了。

**解法**

```bash
for p in python python3; do
  echo "== $p"; $p -c "import sys;print(sys.executable);print(sys.version)"
done
```

兩段路徑不同 = 有這個坑。規矩是**一律用 `python -m pip install`，不要用裸 `pip`** ——
`python -m pip` 保證裝進「執行 `python` 的那一個」。

**它屬於哪一類**

跟 [../DESIGN.md](../DESIGN.md)「文件的物理形態」是同一種病：
**壞掉了，但錯誤訊息指向錯的方向。** `ModuleNotFoundError` 看起來像「沒裝成功」，
於是你會再裝一次 —— 再成功一次，再失敗一次。

完整說明在 [../../../setup/Python環境.md](../../../setup/Python環境.md) 第 3 節。
