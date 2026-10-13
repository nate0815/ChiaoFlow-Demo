# -*- coding: utf-8 -*-
"""掃全 repo 的相對連結，回報真正壞掉的與刻意的示範佔位。

示範佔位＝文件裡用來教語法的假連結（<標題>、xxx、某決策、image%201.png 等），
不是壞掉。CI 要做這件事的話得先能排除它們，否則全是誤報。
"""
import io, os, re, sys

# 刻意的示範佔位：出現這些片段就不算壞
PLACEHOLDER = ('<', 'xxx', 'yyy', '測試', 'image%201.png', '某決策')

# 整棵剪掉的資料夾：沒有正本、也沒有要維護的連結
SKIP_DIRS = {'.git', '.venv', 'node_modules'}

# 只排除根目錄的那個個人簡報工作資料夾（.gitignore 也是擋那一個）。
# ⚠️ 不能改成「路徑含 簡報/ 就跳過」：那會連 extras/簡報/ 一起排掉，
#    而那裡的檔案是移植包的一部分，正是最需要被掃的。
SKIP_AT_ROOT = {'簡報'}

# 選配模組的目錄結構鏡像 starter（core/選配/doc/ART.md → 專案的 doc/ART.md），
# 裡面的連結是寫給「複製過去之後」的位置。所以照 starter 裡的對應位置解析 ——
# 直接排除的話，選配檔裡真正寫錯的連結也會跟著被放過。
RESOLVE_AS = {'core/選配/': 'core/starter/'}


def collect(root='.'):
    """收集要掃的 .md。

    ⚠️ 用 os.walk 而不是 glob('**/*.md')：glob **不會進入點開頭的資料夾**，
       所以 .agents/skills/ 底下的 SKILL.md（以及 .claude/ 的 stub）會被靜靜跳過 ——
       又是一個「漏掉了但不會有任何工具報錯」的形式。
       starter 改成雙工具適配之後，點開頭的資料夾從一個變成三個
       （.agents/、.claude/、.codex/），這條的重要性只增不減。
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        if os.path.relpath(dirpath, root) == '.':
            dirnames[:] = [d for d in dirnames if d not in SKIP_AT_ROOT]
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith('.md'):
                files.append(os.path.relpath(os.path.join(dirpath, fn), root))
    files.sort()
    return files


def main(root='.'):
    os.chdir(root)
    bad, placeholder = [], []
    files = collect(root='.')
    for f in files:
        d = os.path.dirname(f)
        posix = f.replace(os.sep, '/')
        for src, dst in RESOLVE_AS.items():
            if posix.startswith(src):
                d = os.path.dirname(dst + posix[len(src):])
        t =io.open(f, encoding='utf-8').read()
        for m in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', t):
            link = m.group(2).split('#')[0].strip()
            if not link or link.startswith(('http://', 'https://', 'mailto:')):
                continue
            if os.path.exists(os.path.normpath(os.path.join(d, link))):
                continue
            row = (f.replace(os.sep, '/'), m.group(1)[:30], link)
            (placeholder if any(p in link for p in PLACEHOLDER) else bad).append(row)

    print(f'掃了 {len(files)} 個 .md')
    print(f'刻意的示範佔位 {len(placeholder)} 條（不算壞）')
    print(f'真正壞掉 {len(bad)} 條')
    for f, txt, l in bad:
        print(f'  ⛔ {f}  「{txt}」 → {l}')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
