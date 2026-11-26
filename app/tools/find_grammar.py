# -*- coding: utf-8 -*-
import io, os, re, sys
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOK = os.path.join(ROOT, 'كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf')
doc = fitz.open(BOOK)

TERMS = ['Grammar', 'grammar', 'GRAMMAR', 'الماضي البسيط', 'Present perfect', 'Past simple',
         'used to', 'المضارع التام', 'الشرط', 'Reported', 'الكلام المنقول', 'المبني للمجهول',
         'Passive', 'Comparative', 'Linking', 'Relative', 'الصفات', 'تتشابه', 'Condition']
pages = []
for i, page in enumerate(doc):
    t = page.get_text()
    found = [k for k in TERMS if k in t]
    if found:
        pages.append((i + 1, found))
for p, f in pages:
    print(p, '|', ', '.join(f[:6]))
print('total pages with grammar terms:', len(pages))
