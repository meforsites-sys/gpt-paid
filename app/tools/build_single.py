# -*- coding: utf-8 -*-
"""يبني نسخة ملف واحد من التطبيق: كل CSS وJS والبيانات داخل ملف HTML واحد."""
import io, os, sys, base64

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
WEB = os.path.join(ROOT, 'app', 'web')
OUT = os.path.join(ROOT, 'تمارين-النشاط-إنكليزي.html')

html = io.open(os.path.join(WEB, 'index.html'), encoding='utf-8').read()
css = io.open(os.path.join(WEB, 'styles.css'), encoding='utf-8').read()
js_data = io.open(os.path.join(WEB, 'data', 'app.js'), encoding='utf-8').read()
js_exam = io.open(os.path.join(WEB, 'data', 'exam.js'), encoding='utf-8').read()
js_app = io.open(os.path.join(WEB, 'app.js'), encoding='utf-8').read()

# تضمين الخطوط كـ base64
def font_b64(name):
    p = os.path.join(WEB, 'fonts', name)
    return base64.b64encode(io.open(p, 'rb').read()).decode('ascii')

css = css.replace(
    "url('fonts/Tajawal-Regular.ttf')",
    "url(data:font/ttf;base64," + font_b64('Tajawal-Regular.ttf') + ")")
css = css.replace(
    "url('fonts/Tajawal-Bold.ttf')",
    "url(data:font/ttf;base64," + font_b64('Tajawal-Bold.ttf') + ")")
for pf in ('Poppins-Regular.woff2', 'Poppins-SemiBold.woff2', 'Poppins-Bold.woff2'):
    css = css.replace(
        "url('fonts/" + pf + "')",
        "url(data:font/woff2;base64," + font_b64(pf) + ")")

html = html.replace('<link rel="stylesheet" href="styles.css">',
                    '<style>\n' + css + '\n</style>')
html = html.replace('<script src="data/app.js"></script>',
                    '<script>\n' + js_data + '\n</script>')
html = html.replace('<script src="data/exam.js"></script>',
                    '<script>\n' + js_exam + '\n</script>')
html = html.replace('<script src="app.js"></script>',
                    '<script>\n' + js_app + '\n</script>')

io.open(OUT, 'w', encoding='utf-8').write(html)
size = os.path.getsize(OUT) / 1024.0
print('تم إنشاء: %s (%.0f KB)' % (OUT, size))
