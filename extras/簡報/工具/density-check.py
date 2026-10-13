# -*- coding: utf-8 -*-
"""大綱的密度檢查（閘門三能自動查的部分）。

⚠️ 「每點不超過 20 字」要用**單位**算，不是字元數：
   中文一字兩單位、ASCII 一單位，上限 40 單位（＝20 個中文字）。
   用字元數硬算會把 `github.com/cathrynlavery/diagram-design`（38 單位）
   誤判成「38 字超標」，但它其實只有 19 個中文字的寬度。
   來源：archify 的標籤寬度公式（CJK counts as two units）。
"""
import io, re, sys, os

MAX_PTS_READ = 6      # 自己讀的場合放寬到 6 點
MAX_UNITS = 40        # ＝20 個中文字

def units(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)

def main(path, max_pts=MAX_PTS_READ):
    t = io.open(path, encoding='utf-8').read()
    pages = list(re.finditer(r'^## (\d+) · ([^\n]+)\n(.*?)(?=\n## |\Z)', t, re.S | re.M))
    bad = 0
    print(f'密度檢查：{os.path.basename(path)}　上限 {max_pts} 點 / {MAX_UNITS} 單位\n')
    for m in pages:
        no, title, body = m.group(1), m.group(2), m.group(3)
        def f(k):
            r = re.search(r'\*\*%s\*\* \| (.*?) \|\n' % k, body)
            return r.group(1) if r else ''
        claim, serves, visual = f('主張'), f('服務哪一題'), f('視覺')
        pts = [re.sub(r'^[①②③④⑤⑥]\s*', '', x).strip()
               for x in f('內文').split('<br>') if x.strip() and '不放條列' not in x]
        msg = []
        if not claim.endswith(('。', '？', '！')):
            msg.append('主張不是完整句')
        if not serves:
            msg.append('服務哪一題空白')
        has_img = bool(re.search(r'\.(png|jpg|jpeg|svg)$', visual.strip(), re.I))
        cap = 4 if has_img else max_pts     # 有圖的頁只剩一半版面
        if len(pts) > cap:
            msg.append(f'{len(pts)} 點超過 {cap}{"（有圖）" if has_img else ""}')
        over = [f'{x}［{units(x)}單位］' for x in pts if units(x) > MAX_UNITS]
        if over:
            msg.append('超寬：' + '／'.join(over))
        if has_img and not os.path.exists(os.path.join(os.path.dirname(path), visual.strip())):
            msg.append(f'圖檔不存在：{visual.strip()}')
        if msg:
            bad += 1
        img = '🖼' if has_img else '  '
        print(f'  第 {no:>2} 頁 {img} {title[:18]:<20} {len(pts)} 點  {"／".join(msg) if msg else "通過"}')
    print(f'\n  頁數 {len(pages)}　未通過 {bad}')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
