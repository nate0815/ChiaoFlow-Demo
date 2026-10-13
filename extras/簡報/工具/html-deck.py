# -*- coding: utf-8 -*-
"""從 大綱.md 生出「圖紙」風格的 HTML 簡報。

為什麼用生成器而不是手寫 23 頁：大綱是文案正本，手寫容易漏字或改錯邊。
生成器保證 HTML 跟大綱一字不差 —— 要改內容就改大綱再重跑。

⚠️ 但這仍然是**單向輸出**：在 HTML 裡手改的東西不會回到大綱。
"""
import io, os, re, sys, html

SECTIONS = {'為什麼': 'why', '⭐ Core': 'core', 'Extras': 'extras', 'Skill': 'skill'}


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
        # 整段被全形括號包起來的是「給自己看的註記」，不是條列 —— 不該上投影片
        bullets = [x for x in raw if x and not (x.startswith('（') and x.endswith('）'))]
        pages.append(dict(no=no, title=title, sec=sec, label=label, claim=f('主張'),
                          bullets=bullets, sub=f('副標'), visual=f('視覺'), notes=f('講稿')))
    return pages


def esc(s):
    return html.escape(s, quote=False)


def slide_html(p, total):
    img = p['visual'] if re.search(r'\.(png|jpg|jpeg)$', p['visual'], re.I) else ''
    cls = ['slide']
    if p['no'] == 1:
        cls.append('cover')
    if p['sec']:
        cls.append('sec-' + p['sec'])
    if img:
        cls.append('has-img')
    if img and not p['bullets']:
        cls.append('figure')          # 整頁只有圖 —— 細節多的圖需要整個寬度
    elif not p['bullets'] and p['no'] != 1:
        cls.append('statement')

    eyebrow = esc(p['label']) if p['label'] else 'ChiaoFlow ／ 工具包導覽'
    folio = '%02d / %02d' % (p['no'], total)
    out = ['<section class="%s" data-notes="%s">' % (' '.join(cls), esc(p['notes']))]
    out.append('  <i class="reg tl"></i><i class="reg tr"></i><i class="reg bl"></i><i class="reg br"></i>')
    out.append('  <header class="masthead reveal r1">')
    out.append('    <span class="eyebrow">%s</span><span class="folio">%s</span>' % (eyebrow, folio))
    out.append('  </header>')

    if p['no'] == 1:
        out.append('  <div class="body"><div class="hero">')
        out.append('    <h1 class="reveal r2">Chiao<span class="k">Flow</span></h1>')
        out.append('    <div class="underline"></div>')
        out.append('    <p class="tagline reveal r3">%s</p>' % esc(p['sub']))
        out.append('    <p class="statement reveal r4">%s</p>' % esc(p['claim']))
        out.append('  </div></div>')
    else:
        out.append('  <div class="body">')
        out.append('    <h2 class="claim reveal r2">%s</h2>' % esc(p['claim']))
        out.append('    <div class="underline"></div>')
        out.append('    <div class="cols">')
        out.append('      <div class="col-text">')
        if p['bullets']:
            out.append('        <ol class="points">')
            for i, b in enumerate(p['bullets'], 1):
                out.append('          <li class="reveal r%d"><span class="n">%02d</span><span class="t">%s</span></li>'
                           % (min(i + 2, 6), i, esc(b)))
            out.append('        </ol>')
        out.append('      </div>')
        if img:
            out.append('      <figure class="col-img reveal r4"><img src="%s" alt="%s"></figure>'
                       % (esc(img), esc(p['title'])))
        out.append('    </div>')
        out.append('  </div>')

    out.append('  <div class="ruler reveal r6"><div class="ticks"></div><div class="ticks major"></div>')
    out.append('    <div class="footline"><span>%s</span><span class="tag">%s</span></div></div>'
               % (folio, esc(p['title'])))
    out.append('</section>')
    return '\n'.join(out)


def main(outline, shell, out):
    pages = parse(outline)
    total = len(pages)
    slides = '\n\n'.join(slide_html(p, total) for p in pages)
    t = io.open(shell, encoding='utf-8').read()
    t = t.replace('<!--__SLIDES__-->', slides)
    io.open(out, 'w', encoding='utf-8', newline='\n').write(t)
    imgs = sum(1 for p in pages if re.search(r'\.(png|jpg)$', p['visual'], re.I))
    print(f'{out}：{total} 頁，其中 {imgs} 頁有圖')


if __name__ == '__main__':
    main(*sys.argv[1:4])
