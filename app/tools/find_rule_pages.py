# -*- coding: utf-8 -*-
import io, os, re, sys
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOKS = ['2027  1+2 +3+4-compressed (1).pdf', '2027 5+6+7+8-compressed.pdf']
PAT = re.compile(r'القاعدة\s*رقم|القواعد\s*:?\s*التالية|لغرض')
for bname in BOOKS:
    doc = fitz.open(os.path.join(ROOT, bname))
    pages = []
    for i in range(doc.page_count):
        t = doc[i].get_text()
        if PAT.search(t):
            pages.append(i + 1)
    print('%s -> %d pages: %s' % (bname[:22], len(pages), pages))
    doc.close()
