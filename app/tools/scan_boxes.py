# -*- coding: utf-8 -*-
"""استخراج جميع مربعات القواعد (Language boxes) من نص كتاب النشاط."""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, '.work', 'activity_text.txt')
if not os.path.exists(SRC):
    print('missing', SRC)
    sys.exit(1)

t = io.open(SRC, encoding='utf-8').read()
page = 0
blocks = []
cur = []
for line in t.split('\n'):
    m = re.match(r'^===== PAGE (\d+) =====', line.strip())
    if m:
        if cur:
            blocks.append((page, cur))
            cur = []
        page = int(m.group(1))
        continue
    s = line.strip()
    if not s:
        continue
    # سطر قاعدة: يبدأ ب • أو كلمة تعليمية قصيرة
    if s.startswith('•') or re.match(r'^(We |You |Don.t |Remember|Study|Note|Use |If |When |In reported|Look at)', s):
        cur.append(s)

print('pages with rule-like lines:', len(set(p for p, _ in blocks)))
for p, lines in blocks:
    print('\n--- PDF page %d ---' % p)
    for l in lines[:14]:
        print('   ', l[:150])
