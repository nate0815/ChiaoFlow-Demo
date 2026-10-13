---
type: gotcha
date: 2026-08-28
scope: build
---

# 不裝 Playwright 也能把 HTML 圖轉成 PNG —— 但 Edge 會在寫檔前就返回

**現象**

要把 archify 與 diagram-design 產的 HTML 圖轉成 PNG 放進 pptx。
`圖表工具.md` 說 PNG 匯出要 Playwright（約 150MB ＋ 首次啟動的防火牆視窗），
archify 的 CLI 則**根本沒有匯出指令**，只有檢視器介面上有。

Windows 11 內建的 Edge 支援無頭截圖，零安裝。但第一次跑：

```powershell
& $edge --headless --screenshot="$out" --window-size=1400,1000 $url
if (Test-Path $out) { ... }   # ← 永遠是 False
```

三種模式（`--headless`／`=old`／`=new`）全部「失敗」。連 `--dump-dom` 都沒有輸出。

**原因**

**Edge 是 GUI 子系統程式，它會在子行程還在寫檔時就把控制權交回 shell。**
`Test-Path` 在那個瞬間檔案確實還不存在 —— 但過一會兒檔案就出現了。
（`--dump-dom` 沒輸出是另一件事：GUI 程式的 stdout 不接主控台，跟成敗無關。）

診斷時把暫存目錄列出來才發現：**前面那幾次「失敗」的檔案全都在**。

**解法**

用 `Start-Process -Wait` 等它真的結束：

```powershell
$a = @("--headless","--disable-gpu","--no-sandbox","--user-data-dir=$prof",
       "--screenshot=$out","--window-size=1400,1000","--virtual-time-budget=9000", $url)
Start-Process -FilePath $edge -ArgumentList $a -Wait -WindowStyle Hidden
Start-Sleep -Milliseconds 400      # 保險
```

**另外三件同時學到的事**

| | |
|---|---|
| **archify 的 `visual-check` 認 `ARCHIFY_CHROME`** | 它只找 Chrome／Chromium，但那個環境變數可以指向 Edge（`bin/visual-check.mjs:105`） |
| **投影片用的圖要另出「無 cards 版」** | 檢視器的說明卡與工具列會一起被截進去。拿掉 `cards` 另存一份規格最乾淨 |
| **裁圖補色要從「補丁旁邊」取** | 塗掉右下角的縮放小工具時，用左上角取色會拿到卡片的純白，補在頁面底色（`#f8fafc`）上會留下看得見的方塊 |

**這條路的邊界**

`outline-to-pptx.py` 不吃 SVG，一定要轉 PNG。
diagram-design 的 `--format=svg` 是零相依的，所以完整管線是
**HTML／SVG → Edge 無頭截圖 → Pillow 去邊 → PNG**，全程不需要 Playwright。
