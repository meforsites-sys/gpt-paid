# -*- coding: utf-8 -*-
"""أنماط النسخة 3.0: مشتقة من أنماط النسخة 2 مع تعديلات الشعار والأقسام الجديدة."""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'app', 'web2', 'styles.css')
DST = os.path.join(ROOT, 'app', 'web3', 'styles.css')

s = io.open(SRC, encoding='utf-8').read()

# ألوان الشعار
s = s.replace('--teal:#0f766e; --teal-d:#115e59; --teal-l:#14b8a6;',
              '--teal:#1B2A55; --teal-d:#111C3A; --teal-l:#B8860B;')
s = s.replace('.appbar{position:sticky;top:0;z-index:40;background:linear-gradient(135deg,var(--teal-d),var(--teal) 60%,#0d9488);',
              '.appbar{position:sticky;top:0;z-index:40;background:linear-gradient(135deg,#111C3A,#1B2A55 70%,#24356B);')
s = s.replace('.logo{width:40px;height:40px;flex:0 0 40px;border-radius:12px;background:rgba(255,255,255,.16);\n  border:1px solid rgba(255,255,255,.28);display:grid;place-items:center;\n  font-weight:700;font-size:20px;backdrop-filter:blur(4px)}',
              '.logo{width:46px;height:46px;flex:0 0 46px;border-radius:10px;background:#fff;\n  border:1px solid rgba(212,175,55,.6);object-fit:contain;padding:2px}')
s = s.replace('.chip.active{background:var(--teal);border-color:var(--teal);color:#fff;font-weight:700;\n  box-shadow:0 3px 10px rgba(15,118,110,.28)}',
              '.chip.active{background:var(--teal);border-color:var(--teal);color:#fff;font-weight:700;\n  box-shadow:0 3px 10px rgba(27,42,85,.28)}')
s = s.replace('box-shadow:0 4px 16px rgba(15,118,110,.28)}', 'box-shadow:0 4px 16px rgba(27,42,85,.32)}')
s = s.replace('background:linear-gradient(90deg,var(--teal-l),var(--teal))', 'background:linear-gradient(90deg,#D9A520,var(--teal))')
s = s.replace('background:conic-gradient(var(--teal) var(--p,0%),#e2e8f0 0)', 'background:conic-gradient(var(--teal) var(--p,0%),#e2e8f0 0)')

ADD = """

/* ===== النسخة 3: أقسام الملزمة والتدريب ===== */
.booklet{background:#fff}
.booklet .ar{margin:0 0 9px;font-size:15px;line-height:1.95;color:var(--ink)}
.booklet .en{margin:0 0 9px;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;
  font-size:13.5px;line-height:1.75;color:var(--ink-2);background:#f8fafc;
  border:1px dashed var(--line);border-radius:10px;padding:9px 12px}
.booklet .ar:last-child,.booklet .en:last-child{margin-bottom:0}
.sec-title.mini{margin-top:14px;font-size:12px;color:var(--muted)}
.rule-en{background:#f8fafc;border:1px dashed var(--line);border-radius:12px;padding:11px 13px;
  direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;font-size:13px;
  line-height:1.8;color:var(--ink-2);white-space:pre-line}
.tip{margin-bottom:9px;padding-bottom:8px;border-bottom:1px dashed #eef2f7}
.tip:last-child{margin-bottom:0;padding-bottom:0;border-bottom:0}
.tip .ar{margin:0;font-size:14px;line-height:1.85}
#pracFb{max-height:0;overflow:hidden;transition:max-height .35s ease}
#pracFb.show{max-height:900px;overflow:visible}
.fc-src{margin-top:8px;font-size:12px;opacity:.8;direction:rtl}
.fc-back .fc-ar{font-size:14.5px;line-height:1.85;margin:0 0 4px}
.fc-back .fc-en{font-size:13px;opacity:.9;line-height:1.7;margin:0}
.q-card .script{margin-top:4px}
"""
if 'النسخة 3' not in s:
    s += ADD

io.open(DST, 'w', encoding='utf-8').write(s)
print('styles written:', DST, len(s), 'bytes')
