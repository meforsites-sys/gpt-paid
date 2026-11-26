# -*- coding: utf-8 -*-
"""استخراج سياق عبارات قواعد من كتاب النشاط."""
import io, os, re, sys
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOKS = {
    's': os.path.join(ROOT, 'كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf'),
    'a': os.path.join(ROOT, 'كتاب_النشاط_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf'),
}
which = sys.argv[1]
phrase = sys.argv[2]
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 700
doc = fitz.open(BOOKS[which])
for i, page in enumerate(doc):
    t = page.get_text().replace('\uf06e', '•').replace('\uf0b7', '•').replace('\uf0a7', '•')
    t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', t)
    for m in re.finditer(re.escape(phrase), t, re.I):
        print('\n===== %s PAGE %d =====' % (which, i + 1))
        print(t[max(0, m.start() - 100):m.start() + ctx])
