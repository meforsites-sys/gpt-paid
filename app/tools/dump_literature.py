# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'markdown/ادب مجموع.md'
lines = io.open(p, encoding='utf-8').read().splitlines()
for a,b in [(100,180),(470,540),(640,700),(840,900),(1050,1110),(1350,1420),(1490,1560),(1660,1740),(1840,1900),(1985,2030),(2150,2200),(2345,2400)]:
    print('\n===== %d-%d =====' % (a,b))
    for i in range(a-1, min(len(lines), b)):
        print('%4d| %s' % (i+1, lines[i]))
