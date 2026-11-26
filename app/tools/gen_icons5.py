# -*- coding: utf-8 -*-
"""يولّد أيقونات «انكليزي السادس الاعدادي» (mipmap) من شعار الأستاذ علي معز الشلاه."""
import io, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'logo-ali-moez-alshallah-v2.png')   # شعار دائري ذهبي/كحلي
WEB = os.path.join(ROOT, 'app', 'web_english')
RES = os.path.join(ROOT, 'app', 'android_english6', 'res')

NAVY = (18, 47, 79, 255)      # كحلي الشعار
NAVY_HEX = '#122F4F'

DENSITIES = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}
LEGACY = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
FOREGROUND = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}


def circle_mask(size):
    m = Image.new('L', (size * 4, size * 4), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    return m.resize((size, size), Image.LANCZOS)


def main():
    logo = Image.open(SRC).convert('RGBA')
    # قصّ محيط الشعار (إزالة أي فراغ خارجي إن وجد)
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    print('logo master:', logo.size)

    os.makedirs(WEB, exist_ok=True)

    # أيقونة الويب (رأس الصفحة): الدائرة الشفافة
    icon512 = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    lg = logo.resize((512, 512), Image.LANCZOS)
    icon512.alpha_composite(lg)
    icon512.save(os.path.join(WEB, 'icon512.png'), 'PNG', optimize=True)
    icon512.save(os.path.join(WEB, 'icon512_alpha.png'), 'PNG', optimize=True)
    print('web icons written')

    for dens, scale in DENSITIES.items():
        outdir = os.path.join(RES, 'mipmap-' + dens)
        os.makedirs(outdir, exist_ok=True)

        # الأيقونة الكلاسيكية: كحلي ممتلئ + الشعار
        size = LEGACY[dens]
        canvas = Image.new('RGBA', (size, size), NAVY)
        inner = logo.resize((int(size * 0.92), int(size * 0.92)), Image.LANCZOS)
        off = (size - inner.width) // 2
        canvas.alpha_composite(inner, (off, off))
        canvas.convert('RGB').save(os.path.join(outdir, 'ic_launcher.png'), 'PNG', optimize=True)

        # الأيقونة الدائرية
        mask = circle_mask(size)
        circ = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        circ.paste(canvas, (0, 0), mask)
        circ.convert('RGB').save(os.path.join(outdir, 'ic_launcher_round.png'), 'PNG', optimize=True)

        # طبقة المقدمة التكيّفية (الهامش الآمن ~66%)
        fsize = FOREGROUND[dens]
        fg = Image.new('RGBA', (fsize, fsize), (0, 0, 0, 0))
        inner2 = logo.resize((int(fsize * 0.66), int(fsize * 0.66)), Image.LANCZOS)
        off2 = (fsize - inner2.width) // 2
        fg.alpha_composite(inner2, (off2, off2))
        fg.save(os.path.join(outdir, 'ic_launcher_foreground.png'), 'PNG', optimize=True)
        print('  %-8s legacy=%d foreground=%d' % (dens, size, fsize))

    print('done — NAVY background:', NAVY_HEX)


if __name__ == '__main__':
    main()
