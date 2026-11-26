# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'markdown/كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.md'
lines = io.open(p, encoding='utf-8').read().splitlines()
for a,b in [(579,650),(1083,1115),(1457,1525),(1792,1830),(2180,2285),(2286,2360),(2681,2740)]:
    print('\n===== %d-%d =====' % (a,b))
    for i in range(a-1, min(len(lines), b)):
        print('%4d| %s' % (i+1, lines[i]))
