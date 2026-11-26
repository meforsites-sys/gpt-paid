# -*- coding: utf-8 -*-
"""استخراج مربعات Grammar من كتاب الطالب."""
import io, os, re, sys
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOK = os.path.join(ROOT, 'كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf')


def clean(t):
    t = t.replace('\uf06e', '•').replace('\uf0b7', '•').replace('\uf0a7', '•')
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', t)


doc = fitz.open(BOOK)
for i, page in enumerate(doc):
    t = clean(page.get_text())
    for m in re.finditer(r'Grammar', t):
        start = max(0, m.start() - 120)
        print('\n===== PAGE %d (offset %d) =====' % (i + 1, m.start()))
        print(t[start:m.start() + 1800])
        break
