# -*- coding: utf-8 -*-
"""يولّد أيقونات التطبيق (mipmap) للنسخة الأولى com.sixth.grammar من الشعار الأصلي.
الطبقة الأمامية PNG لكل الكثافات (بمحاذاة المنطقة الآمنة 66dp) + خلفية بيضاء.
ملاحظة: gen_icons.py (بلا V1) يخص خط مشروع android_malzmah الموازي — لا تخلط بينهما.
"""
import os, sys, statistics
from collections import deque
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP = os.path.join(ROOT, 'app')
SRC = os.path.join(APP, 'android', 'icon_source.png')   # الشعار الأصلي (صورة الأستاذ)
RES = os.path.join(APP, 'android', 'res')
DENS = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}
SAFE = 0.611  # المنطقة الآمنة 66dp من قماش 108dp

im = Image.open(SRC).convert('RGB')
w, h = im.size
px = im.load()

# 1) قصّ الهوامش البيضاء
thr = 242
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(0, h, 2):
    for x in range(0, w, 2):
        r, g, b = px[x, y]
        if r < thr or g < thr or b < thr:
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y
pad = 8
minx = max(0, minx - pad); miny = max(0, miny - pad)
maxx = min(w, maxx + pad); maxy = min(h, maxy + pad)
crop = im.crop((minx, miny, maxx + 1, maxy + 1))
cw, ch = crop.size
print('crop:', crop.size)

# 2) خلفية بيضاء: تندمج مع جيوب الأبيض المحصورة في الشعار
hexc = '#FFFFFF'
print('bg color:', hexc)

# 3) جعل الخلفية البيضاء المتصلة بحواف الصورة شفافة (الأبيض الداخلي المحصور يبقى)
content = crop.convert('RGBA')
W, H = content.size
cp = content.load()

def whiteish(p):
    return p[0] >= 236 and p[1] >= 236 and p[2] >= 236

seen = bytearray(W * H)
q = deque()
for x in range(W):
    for y in (0, H - 1):
        i = y * W + x
        if whiteish(cp[x, y]) and not seen[i]:
            seen[i] = 1; q.append((x, y))
for y in range(H):
    for x in (0, W - 1):
        i = y * W + x
        if whiteish(cp[x, y]) and not seen[i]:
            seen[i] = 1; q.append((x, y))
while q:
    x, y = q.popleft()
    cp[x, y] = (0, 0, 0, 0)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H:
            i = ny * W + nx
            if not seen[i] and whiteish(cp[nx, ny]):
                seen[i] = 1; q.append((nx, ny))
print('transparent bg done')

# 4) الطبقة الأمامية لكل كثافة
for qd, size in DENS.items():
    d = os.path.join(RES, 'mipmap-' + qd)
    os.makedirs(d, exist_ok=True)
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    inner = int(round(size * SAFE))
    sc = inner / float(max(cw, ch))
    nw, nh = max(1, int(round(cw * sc))), max(1, int(round(ch * sc)))
    rs = content.resize((nw, nh), Image.LANCZOS)
    # تآكل الحافة بكسل واحد لإزالة الهالة البيضاء
    a = rs.getchannel('A').filter(ImageFilter.MinFilter(3))
    rs.putalpha(a)
    canvas.paste(rs, ((size - nw) // 2, (size - nh) // 2), rs)
    out = os.path.join(d, 'ic_launcher_foreground.png')
    canvas.save(out, 'PNG')
    print('saved', out, canvas.size)

# 5) تحديث ملفات XML
bg_xml = '''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="%s"
        android:pathData="M0,0h108v108h-108z" />
</vector>
''' % hexc
open(os.path.join(RES, 'drawable', 'ic_launcher_background.xml'), 'w', encoding='utf-8').write(bg_xml)

open(os.path.join(RES, 'mipmap-anydpi-v26', 'ic_launcher.xml'), 'w', encoding='utf-8').write(
    '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
</adaptive-icon>
''')

open(os.path.join(RES, 'mipmap', 'ic_launcher.xml'), 'w', encoding='utf-8').write(
    '''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/ic_launcher_background" />
    <item android:drawable="@mipmap/ic_launcher_foreground" />
</layer-list>
''')

old = os.path.join(RES, 'drawable', 'ic_launcher_foreground.xml')
if os.path.exists(old):
    os.remove(old)
    print('removed:', old)

print('DONE bg=' + hexc)
