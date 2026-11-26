# -*- coding: utf-8 -*-
"""يولّد أيقونات التطبيق (mipmap) من الشعار."""
import io, os, sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'app', 'web3', 'icon512.png')
SRC_A = os.path.join(ROOT, 'app', 'web3', 'icon512_alpha.png')
RES = os.path.join(ROOT, 'app', 'android_malzmah', 'res')

DENSITIES = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}
LEGACY = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
FOREGROUND = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}


def fit(img, size, ratio=1.0):
    """يحجم الصورة داخل مربع مع خلفية اختيارية."""
    w, h = int(size * ratio), int(size * ratio)
    r = img.resize((w, h), Image.LANCZOS)
    return r


def main():
    white = Image.open(SRC).convert('RGBA')
    alpha = Image.open(SRC_A).convert('RGBA')
    print('master:', white.size)

    for dens, scale in DENSITIES.items():
        outdir = os.path.join(RES, 'mipmap-' + dens)
        os.makedirs(outdir, exist_ok=True)

        # أيقونة كلاسيكية (مربعة بخلفية بيضاء)
        size = LEGACY[dens]
        canvas = Image.new('RGBA', (size, size), (255, 255, 255, 255))
        lg = white.resize((size, size), Image.LANCZOS)
        canvas.alpha_composite(lg)
        canvas.convert('RGB').save(os.path.join(outdir, 'ic_launcher.png'), 'PNG', optimize=True)

        # النسخة الدائرية
        mask = Image.new('L', (size * 4, size * 4), 0)
        from PIL import ImageDraw
        d = ImageDraw.Draw(mask)
        d.ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
        mask = mask.resize((size, size), Image.LANCZOS)
        circ = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        circ.paste(canvas, (0, 0), mask)
        circ.convert('RGB').save(os.path.join(outdir, 'ic_launcher_round.png'), 'PNG', optimize=True)

        # طبقة المقدمة للأيقونة التكيّفية (108dp) مع الهامش الآمن
        fsize = FOREGROUND[dens]
        fg = Image.new('RGBA', (fsize, fsize), (0, 0, 0, 0))
        inner = fit(alpha, fsize, 0.62)
        off = (fsize - inner.width) // 2
        fg.alpha_composite(inner, (off, off))
        fg.save(os.path.join(outdir, 'ic_launcher_foreground.png'), 'PNG', optimize=True)

        print('  %-8s legacy=%d foreground=%d' % (dens, size, fsize))

    print('done')


if __name__ == '__main__':
    main()
