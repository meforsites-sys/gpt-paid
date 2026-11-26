# -*- coding: utf-8 -*-
"""استخراج نص كتاب الطالب والبحث عن مواضع شرح القواعد."""
import io, os, re, sys
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOK = os.path.join(ROOT, 'كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf')
OUT = os.path.join(ROOT, '.work', 'student_text.txt')


def clean(t):
    t = t.replace('\uf06e', '•').replace('\uf0b7', '•').replace('\uf0a7', '•')
    t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', t)
    return t


doc = fitz.open(BOOK)
print('pages:', doc.page_count)
with io.open(OUT, 'w', encoding='utf-8') as f:
    for i, page in enumerate(doc):
        f.write('\n===== PAGE %d =====\n' % (i + 1))
        f.write(clean(page.get_text()))
print('written:', OUT)

# البحث عن صفحات تحتوي شرحًا قواعديًا
KEYS = ['القاعدة', 'القواعد', 'نستعمل', 'نستخدم', 'تُستعمل', 'Grammar', 'grammar']
hits = []
for i, page in enumerate(doc):
    t = clean(page.get_text())
    score = sum(t.count(k) for k in KEYS)
    if score >= 2:
        hits.append((i + 1, score, t[:90].replace('\n', ' | ')))
for h in hits:
    print(h[0], h[1], h[2])
print('hit pages:', len(hits))
