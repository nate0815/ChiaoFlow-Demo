# -*- coding: utf-8 -*-
"""大綱.md → 帶「圖紙」視覺的可編輯 pptx。

為什麼不是「HTML 轉 pptx」：HTML 的視覺是 CSS，轉不成 PowerPoint 的形狀與文字框。
所以這支不做轉檔 —— 它讀同一份大綱，用 python-pptx **直接畫出**同一套視覺。

三個刻意的設計：
1. 文字全部放在**真正的 placeholder** 裡 —— 改得動，而且大綱檢視看得到。
   自己畫的文字框在版面上看起來一樣，但接手的人會發現大綱檢視是空的（不會有錯誤訊息）。
2. 網格與定位十字走**一張底圖**，不用幾十個形狀 —— 檔案小、也不會擋住編輯。
3. 字型只用**這台機器已經有的**（Noto Sans TC／Cascadia Code）——
   這份是要交給協作者改的，裝 Google Fonts 的話對方打開會變成替代字型。
"""
import io, os, re, sys
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

PX = 6350                      # 1 設計 px（1920 寬）＝ 6350 EMU
PT = 0.5                       # 1 設計 px ＝ 0.5 pt

INK    = RGBColor(0x2D, 0x31, 0x42)
MUTED  = RGBColor(0x4F, 0x5D, 0x75)
SOFT   = RGBColor(0x7A, 0x83, 0x99)
ACCENT = RGBColor(0xEB, 0x6C, 0x36)
PAPER  = RGBColor(0xF5, 0xF5, 0xF5)
RULE   = RGBColor(0xDD, 0xDE, 0xE2)

CJK  = 'Noto Sans TC'
MONO = 'Cascadia Code'

SECTIONS = {'為什麼': 'why', '⭐ Core': 'core', 'Extras': 'extras', 'Skill': 'skill'}


# ── 大綱解析（跟 HTML 生成器同一套規則）──────────────────────────────
def parse(path):
    t = io.open(path, encoding='utf-8').read()
    pages = []
    for m in re.finditer(r'^## (\d+) · (.+?)\n(.*?)(?=\n## |\Z)', t, re.S | re.M):
        no, title, body = int(m.group(1)), m.group(2).strip(), m.group(3)

        def f(k):
            r = re.search(r'\*\*%s\*\* \| (.*?) \|\n' % k, body)
            return r.group(1).strip() if r else ''

        sec, label = '', ''
        for tag, slug in SECTIONS.items():
            if title.startswith(tag + '｜'):
                sec, label, title = slug, tag, title[len(tag) + 1:]
                break
        raw = [re.sub(r'^[①②③④⑤⑥]\s*', '', x).strip() for x in f('內文').split('<br>')]
        # 整段被全形括號包起來的是給自己看的註記，不是條列
        bullets = [x for x in raw if x and not (x.startswith('（') and x.endswith('）'))]
        pages.append(dict(no=no, title=title, sec=sec, label=label, claim=f('主張'),
                          bullets=bullets, sub=f('副標'), visual=f('視覺'), notes=f('講稿')))
    return pages


# ── 小工具 ──────────────────────────────────────────────────────────
def font(run, name, size_px, color, bold=False):
    run.font.size = Pt(size_px * PT)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = name
    rPr = run.font._rPr                       # 東亞字型要另外設，否則中文會掉回預設
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', name)


def rect(slide, x, y, w, h, color):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x * PX, y * PX, w * PX, h * PX)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def textbox(slide, x, y, w, h, text, name, size_px, color, bold=False,
            align=PP_ALIGN.LEFT, space=None):
    tb = slide.shapes.add_textbox(x * PX, y * PX, w * PX, h * PX)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    font(r, name, size_px, color, bold)
    if space:
        r.font._rPr.set('spc', str(int(space * size_px * PT * 100)))
    return tb


def send_to_back(slide, shape):
    el = shape._element
    el.getparent().remove(el)
    slide.shapes._spTree.insert(2, el)


def pick_layout(prs):
    """挑一個同時有標題與內容 placeholder 的版面配置。"""
    for lay in prs.slide_layouts:
        idxs = sorted(ph.placeholder_format.idx for ph in lay.placeholders)
        if 0 in idxs and len(idxs) > 1:
            name = lay.name.lower()
            if any(k in name for k in ('標題及內容', '標題與內容', 'title and content')):
                return lay, [i for i in idxs if i != 0][0]
    for lay in prs.slide_layouts:
        idxs = sorted(ph.placeholder_format.idx for ph in lay.placeholders)
        if 0 in idxs and len(idxs) > 1:
            return lay, [i for i in idxs if i != 0][0]
    raise SystemExit('找不到「有標題也有內容」的版面配置')


# ── 版面座標（設計 px，1920×1080）─────────────────────────────────
PAD_X, PAD_T, PAD_B = 132, 92, 76
BODY_W = 1920 - 2 * PAD_X                      # 1656
MAST_RULE_Y = 147
CLAIM_Y, CLAIM_H = 182, 170                    # 預留兩行
UL_Y = 372                                     # 重音底線
CONTENT_Y = 420
RULER_Y = 899                                  # 刻度尺起點
FOOT_RULE_Y = 971


def chrome(slide, p, total, bg, figure=False):
    """每頁都有的骨架：底圖、左緣識別條、檔頭、刻度尺、頁腳。

    `figure=True`（整頁只有圖）時**不畫刻度尺** —— 那 60px 讓給圖。
    細節多的圖在 16:9 版面上是被高度卡住的，省下來的每一格都有用。
    """
    pic = slide.shapes.add_picture(bg, 0, 0, width=1920 * PX, height=1080 * PX)
    send_to_back(slide, pic)                   # 底圖要在所有東西後面

    # 左緣識別條 —— Core 是唯一主推的，給它重音色
    rect(slide, 0, 0, 12, 1080, ACCENT if p['sec'] == 'core' else RULE)

    # 檔頭
    eyebrow = p['label'] or 'ChiaoFlow ／ 工具包導覽'
    is_core = p['sec'] == 'core'
    textbox(slide, PAD_X, PAD_T - 6, 900, 44, eyebrow, CJK, 25,
            ACCENT if is_core else (MUTED if p['sec'] else SOFT), bold=is_core)
    folio = '%02d / %02d' % (p['no'], total)
    textbox(slide, 1120, PAD_T - 4, 1920 - PAD_X - 1120, 44, folio, MONO, 22,
            MUTED, align=PP_ALIGN.RIGHT, space=0.22)
    rect(slide, PAD_X, MAST_RULE_Y, BODY_W, 2, RULE)

    # 刻度尺（只畫主刻度：240px 一格）
    if not figure:
        for k in range(0, 8):
            x = PAD_X + k * 240
            if x <= PAD_X + BODY_W:
                rect(slide, x, RULER_Y + 30, 2, 28, SOFT)

    # 頁腳
    rect(slide, PAD_X, FOOT_RULE_Y, BODY_W, 1, RULE)
    textbox(slide, PAD_X, FOOT_RULE_Y + 14, 500, 34, folio, MONO, 20, MUTED, space=0.18)
    textbox(slide, 1088, FOOT_RULE_Y + 14, 1920 - PAD_X - 1088, 34, p['title'],
            CJK, 21, SOFT, align=PP_ALIGN.RIGHT)


def build(outline, out, template=None):
    pages = parse(outline)
    total = len(pages)
    # 底圖跟著工具走，不跟著大綱走 —— 這樣任何簡報工作資料夾都能直接用
    bg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'bg-grid.png')
    if not os.path.exists(bg):
        raise SystemExit('找不到底圖：' + bg)

    prs = Presentation(template) if template else Presentation()
    for sld in list(prs.slides._sldIdLst):
        prs.part.drop_rel(sld.get(qn('r:id')))
        prs.slides._sldIdLst.remove(sld)
    prs.slide_width, prs.slide_height = 1920 * PX, 1080 * PX
    layout, body_idx = pick_layout(prs)

    for p in pages:
        slide = prs.slides.add_slide(layout)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = PAPER
        chrome(slide, p, total, bg)

        img = p['visual'] if re.search(r'\.(png|jpg|jpeg)$', p['visual'], re.I) else ''
        img_path = os.path.join(os.path.dirname(os.path.abspath(outline)), img) if img else ''
        if img_path and not os.path.exists(img_path):
            print('⚠️  圖檔找不到，這頁不放圖：' + img)
            img_path = ''
        figure = bool(img_path) and not p['bullets']

        title = slide.shapes.title
        body = slide.placeholders[body_idx]

        # ── 標題 placeholder：放主張（封面放 ChiaoFlow）──
        title.left, title.top = PAD_X * PX, CLAIM_Y * PX
        title.width = 1560 * PX
        title.height = (90 if figure else CLAIM_H) * PX
        tf = title.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.TOP
        para = tf.paragraphs[0]
        if p['no'] == 1:
            r = para.add_run(); r.text = 'Chiao'; font(r, CJK, 224, INK, True)
            r2 = para.add_run(); r2.text = 'Flow'; font(r2, CJK, 224, ACCENT, True)
            title.top, title.height = 250 * PX, 300 * PX
        else:
            r = para.add_run(); r.text = p['claim']
            font(r, CJK, 46 if figure else 58, INK, True)

        # ── 重音底線 ──
        ul_y = 292 if figure else (560 if p['no'] == 1 else UL_Y)
        ul_w = 520 if p['no'] == 1 else 420
        rect(slide, PAD_X, ul_y, ul_w, 5, ACCENT)
        rect(slide, PAD_X + ul_w - 2, ul_y - 8, 20, 20, ACCENT)

        # ── 內容 placeholder ──
        if p['no'] == 1:
            body.left, body.top = PAD_X * PX, 620 * PX
            body.width, body.height = 1400 * PX, 240 * PX
            btf = body.text_frame
            btf.word_wrap = True
            btf.margin_left = btf.margin_top = 0
            q = btf.paragraphs[0]
            r = q.add_run(); r.text = p['sub']; font(r, CJK, 50, MUTED)
            q2 = btf.add_paragraph()
            q2.space_before = Pt(30)
            r2 = q2.add_run(); r2.text = p['claim']; font(r2, CJK, 37, INK, True)
        elif p['bullets']:
            body.left, body.top = PAD_X * PX, CONTENT_Y * PX
            body.width = (740 if img_path else BODY_W) * PX
            body.height = (RULER_Y - CONTENT_Y) * PX
            btf = body.text_frame
            btf.word_wrap = True
            btf.margin_left = btf.margin_top = 0
            for i, b in enumerate(p['bullets']):
                q = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
                if i:
                    q.space_before = Pt(26 * PT)
                rn = q.add_run(); rn.text = '%02d   ' % (i + 1)
                font(rn, MONO, 21, ACCENT, True)
                rt = q.add_run(); rt.text = b
                font(rt, CJK, 30, INK)
        else:
            el = body._element
            el.getparent().remove(el)          # 沒內容的 placeholder 拿掉，避免出現提示字

        # ── 圖 ──
        if img_path:
            if figure:
                top, avail_h, avail_w, left = 320, 950 - 320, BODY_W, PAD_X
            else:
                top, avail_h = CONTENT_Y, RULER_Y - CONTENT_Y
                left, avail_w = 932, 1920 - PAD_X - 932
            pic = slide.shapes.add_picture(img_path, left * PX, top * PX, width=avail_w * PX)
            if pic.height > avail_h * PX:
                sc = (avail_h * PX) / float(pic.height)
                pic.width, pic.height = int(pic.width * sc), int(pic.height * sc)
                pic.left = (left + int((avail_w - pic.width / PX) / 2)) * PX

        if p['notes']:
            slide.notes_slide.notes_text_frame.text = p['notes']

    prs.save(out)
    imgs = sum(1 for p in pages if re.search(r'\.(png|jpg)$', p['visual'], re.I))
    print(f'{out}：{total} 頁，其中 {imgs} 頁有圖')


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
