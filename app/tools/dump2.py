# -*- coding: utf-8 -*-
import io, os, re, sys
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOKS = {
    's': os.path.join(ROOT, 'كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf'),
    'a': os.path.join(ROOT, 'كتاب_النشاط_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf'),
}
which = sys.argv[1]
pages = [int(x) for x in sys.argv[2:]]
doc = fitz.open(BOOKS[which])
for p in pages:
    t = doc[p - 1].get_text()
    t = t.replace('\uf06e', '•').replace('\uf0b7', '•').replace('\uf0a7', '•')
    t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', t)
    print('\n########## %s PAGE %d ##########' % (which, p))
    print(t)
