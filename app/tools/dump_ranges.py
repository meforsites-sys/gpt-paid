# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

def dump(path, start, end):
    lines = io.open(path, encoding='utf-8').read().splitlines()
    print('\n===== %s lines %d-%d =====' % (path, start, end))
    for i in range(max(0, start-1), min(len(lines), end)):
        print('%4d| %s' % (i+1, lines[i]))

p = r'markdown/2027 5+6+7+8-compressed.md'
dump(p, 755, 840)
dump(p, 4240, 4305)
p2 = r'markdown/2027  1+2 +3+4-compressed (1).md'
dump(p2, 350, 410)
dump(p2, 1170, 1215)
