# -*- coding: utf-8 -*-
"""Builds the adopted v1.12.9 single-file app with embedded fonts.

The 1.12.9 release still loaded Tajawal/Poppins from Google Fonts, so it needed
the network for its typography. This script replaces that <link> with base64
@font-face rules taken from app/web/fonts, so the page (and the APK that wraps
it) renders identically with no network at all.

Input : app/english2027/index_v1.12.9_original.html   (pristine release)
Output: app/english2027/index.html + index.html      (offline build)

    py app/tools/make_v1129_offline.py
"""
import base64
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
APP = os.path.join(ROOT, 'app')
SRC = os.path.join(APP, 'english2027', 'index_v1.12.9_original.html')
OUTS = [
    os.path.join(APP, 'english2027', 'index.html'),
    os.path.join(ROOT, 'index.html'),
]
FONTS = os.path.join(APP, 'web', 'fonts')

# family, file, mime, css weight range
FACES = [
    ('Tajawal', 'Tajawal-Regular.ttf', 'font/ttf', '400 500'),
    ('Tajawal', 'Tajawal-Bold.ttf', 'font/ttf', '700 900'),
    ('Poppins', 'Poppins-Regular.woff2', 'font/woff2', '400 500'),
    ('Poppins', 'Poppins-SemiBold.woff2', 'font/woff2', '600 600'),
    ('Poppins', 'Poppins-Bold.woff2', 'font/woff2', '700 800'),
]

LINK_RE = re.compile(r'<link[^>]*fonts\.googleapis\.com[^>]*>\s*')


def die(msg):
    print('ERROR:', msg)
    sys.exit(1)


def css_block():
    parts = ['<style>']
    for family, name, mime, weight in FACES:
        path = os.path.join(FONTS, name)
        if not os.path.isfile(path):
            die('missing font ' + path)
        data = base64.b64encode(open(path, 'rb').read()).decode('ascii')
        parts.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
            "font-display:swap;src:url(data:%s;base64,%s) format('%s')}"
            % (family, weight, mime, data, 'truetype' if mime == 'font/ttf' else 'woff2'))
    parts.append('</style>')
    return '\n'.join(parts)


def main():
    if not os.path.isfile(SRC):
        die('missing pristine source ' + SRC)
    html = io.open(SRC, encoding='utf-8', newline='').read()

    if 'offline-fonts-v1129' in html:
        die('source already has embedded fonts — rebuild from the pristine file')

    found = LINK_RE.findall(html)
    if len(found) != 1:
        die('expected exactly one Google Fonts <link>, found %d' % len(found))

    out = LINK_RE.sub(css_block() + '\n', html, count=1)

    for needle in ('fonts.googleapis.com', 'fonts.gstatic.com'):
        if needle in out:
            die('external font reference still present: ' + needle)
    if out.count('@font-face') != len(FACES):
        die('unexpected @font-face count: %d' % out.count('@font-face'))
    if len(out) < len(html):
        die('output unexpectedly smaller than source')

    for path in OUTS:
        io.open(path, 'w', encoding='utf-8', newline='').write(out)
        print('wrote %-52s %8.0f KB' % (os.path.relpath(path, ROOT), os.path.getsize(path) / 1024.0))

    print('\n@font-face : %d' % out.count('@font-face'))
    print('google refs: 0')
    print('size       : %.0f KB (source %.0f KB)' % (len(out.encode('utf-8')) / 1024.0,
                                                     len(html.encode('utf-8')) / 1024.0))


if __name__ == '__main__':
    main()
