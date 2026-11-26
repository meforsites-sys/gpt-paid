# -*- coding: utf-8 -*-
import io, os, re, sys
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOK = os.path.join(ROOT, 'كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf')
doc = fitz.open(BOOK)
print('pages:', doc.page_count)
for i in [0, 1, 2, 3, 4, 5, 8, 10]:
    if i >= doc.page_count:
        break
    t = doc[i].get_text()
    print('===== PAGE', i + 1, 'len=', len(t), 'images=', len(doc[i].get_images()))
    print(t[:700])
    print()
