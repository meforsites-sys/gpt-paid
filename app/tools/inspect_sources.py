# -*- coding: utf-8 -*-
import io, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

FILES = [
    r'markdown/2027  1+2 +3+4-compressed (1).md',
    r'markdown/2027 5+6+7+8-compressed.md',
    r'markdown/كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.md',
    r'markdown/كتاب_النشاط_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.md',
    r'markdown/ادب مجموع.md',
]
TERMS = ['When I was 16', 'Kerkennah', 'Euphrates', 'Ammar', 'قطعة', 'Reading', 'read the', 'اقرأ', 'Pride and Prejudice', 'As You Like It', 'Section 1']

for p in FILES:
    if not os.path.exists(p):
        continue
    s = io.open(p, encoding='utf-8').read()
    print('\n===== %s | %d chars =====' % (p, len(s)))
    for term in TERMS:
        idxs = [m.start() for m in re.finditer(re.escape(term), s, re.I)]
        if idxs:
            print('  %-25s %d hits' % (term, len(idxs)))
            for ix in idxs[:3]:
                line = s.count('\n', 0, ix) + 1
                print('    line %d: %s' % (line, s[max(0, ix-100):ix+180].replace('\n', ' | ')))
