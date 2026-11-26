# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout.reconfigure(encoding='utf-8')
p = r'markdown/كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.md'
s = io.open(p, encoding='utf-8').read()
lines = s.splitlines()
terms = [
    'A police officer', 'Airport security', 'Meet one of the most popular', 'Fitness tech',
    'How to be the best', 'Making money', "Volunteers at the Children", 'Using the library',
    'Against all odds', 'Using your phone behind the wheel', 'The crazy', 'Why are holidays',
]
for term in terms:
    idx = s.lower().find(term.lower())
    if idx < 0:
        print('NOT FOUND', term); continue
    line = s.count('\n', 0, idx) + 1
    print('\n===== %s @ line %d =====' % (term, line))
    for i in range(max(0, line-8), min(len(lines), line+55)):
        print('%4d| %s' % (i+1, lines[i]))
