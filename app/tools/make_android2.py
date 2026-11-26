# -*- coding: utf-8 -*-
"""ينشئ مشروع أندرويد للنسخة الثانية (اسم جديد ومعرّف حزمة جديد)."""
import io, os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'app', 'android')
DST = os.path.join(ROOT, 'app', 'android2')

if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

# معرّف الحزمة الجديد
for root, dirs, files in os.walk(DST):
    for f in files:
        if f.endswith(('.java', '.xml')):
            p = os.path.join(root, f)
            s = io.open(p, encoding='utf-8').read()
            s2 = s.replace('com.sixth.grammar', 'com.sixth.grammar2')
            if s2 != s:
                io.open(p, 'w', encoding='utf-8').write(s2)
                print('patched', os.path.relpath(p, ROOT))

# مجلد الحزمة
old = os.path.join(DST, 'java', 'com', 'sixth', 'grammar')
new = os.path.join(DST, 'java', 'com', 'sixth', 'grammar2')
if os.path.isdir(old):
    os.rename(old, new)
    print('renamed package dir')

# اسم التطبيق الجديد
p = os.path.join(DST, 'res', 'values', 'strings.xml')
s = io.open(p, encoding='utf-8').read()
s = s.replace('<string name="app_name">قواعد الإنجليزي</string>',
              '<string name="app_name">ملزمة القواعد</string>')
io.open(p, 'w', encoding='utf-8').write(s)
print('app_name = ملزمة القواعد')

# النسخة في البيان
p = os.path.join(DST, 'AndroidManifest.xml')
s = io.open(p, encoding='utf-8').read()
s = s.replace('android:versionCode="1"', 'android:versionCode="2"')
s = s.replace('android:versionName="1.0"', 'android:versionName="2.0"')
io.open(p, 'w', encoding='utf-8').write(s)
print('version = 2.0')
