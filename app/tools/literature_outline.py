# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout.reconfigure(encoding='utf-8')
p = r'markdown/ادب مجموع.md'
lines = io.open(p, encoding='utf-8').read().splitlines()
for i, l in enumerate(lines, 1):
    if re.match(r'^#{2,3} ', l):
        print('%4d| %s' % (i, l))
