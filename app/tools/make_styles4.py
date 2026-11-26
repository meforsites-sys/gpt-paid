# -*- coding: utf-8 -*-
"""أنماط النسخة 4.0: Poppins للإنجليزية + حقول الإدخال في الفراغات."""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'app', 'web3', 'styles.css')
DST = os.path.join(ROOT, 'app', 'web4', 'styles.css')
s = io.open(SRC, encoding='utf-8').read()

# ---------- خط Poppins للإنجليزي ----------
FONTS = """
/* ===== خط Poppins للنصوص الإنجليزية ===== */
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Regular.woff2') format('woff2');font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-SemiBold.woff2') format('woff2');font-weight:600;font-style:normal;font-display:swap}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Bold.woff2') format('woff2');font-weight:700;font-style:normal;font-display:swap}
:root{--en:'Poppins','Segoe UI',system-ui,sans-serif}
"""
if 'Poppins' not in s:
    s = s.replace('/* ---------- الشريط العلوي ---------- */', FONTS + '\n/* ---------- الشريط العلوي ---------- */')

# استبدال خط الإنجليزي في العناصر
s = s.replace(".script{font-style:italic;font-weight:700;margin:10px 0 4px;direction:ltr;text-align:left;\n  font-family:'Segoe UI',system-ui,sans-serif;font-size:14px;color:var(--teal-d)}",
              ".script{font-style:italic;font-weight:700;margin:10px 0 4px;direction:ltr;text-align:left;\n  font-family:var(--en);font-size:14px;color:var(--teal-d)}")
s = s.replace(".items li{padding:7px 0;border-bottom:1px dashed #eef2f7;direction:ltr;text-align:left;\n  font-family:'Segoe UI',system-ui,sans-serif;font-size:14px;line-height:1.6}",
              ".items li{padding:7px 0;border-bottom:1px dashed #eef2f7;direction:ltr;text-align:left;\n  font-family:var(--en);font-size:14px;line-height:1.6}")
s = s.replace(".q-text{font-size:17px;font-weight:700;line-height:1.6;margin-bottom:14px;direction:ltr;text-align:left;\n  font-family:'Segoe UI',system-ui,sans-serif}",
              ".q-text{font-size:17px;font-weight:700;line-height:1.6;margin-bottom:14px;direction:ltr;text-align:left;\n  font-family:var(--en)}")
s = s.replace(".fc-q{font-size:20px;font-weight:700;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;line-height:1.5}",
              ".fc-q{font-size:19px;font-weight:600;direction:ltr;text-align:left;font-family:var(--en);line-height:1.55}")
s = s.replace(".fc-a{font-size:22px;font-weight:700;direction:ltr;text-align:left;font-family:'Segge UI','Segoe UI',system-ui,sans-serif}",
              ".fc-a{font-size:21px;font-weight:700;direction:ltr;text-align:left;font-family:var(--en)}")
s = s.replace(".en-title{direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".en-title{direction:ltr;text-align:left;font-family:var(--en);")
s = s.replace(".rule-en{background:#f8fafc;border:1px dashed var(--line);border-radius:12px;padding:11px 13px;\n  direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;font-size:13px;",
              ".rule-en{background:#f8fafc;border:1px dashed var(--line);border-radius:12px;padding:11px 13px;\n  direction:ltr;text-align:left;font-family:var(--en);font-size:13px;")
s = s.replace(".opt{display:flex;align-items:center;gap:10px;border:1.5px solid var(--line);background:#fff;border-radius:12px;\n  padding:12px 13px;cursor:pointer;font-size:15px;text-align:start;width:100%;font-family:inherit;\n  transition:.15s;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif}",
              ".opt{display:flex;align-items:center;gap:10px;border:1.5px solid var(--line);background:#fff;border-radius:12px;\n  padding:12px 13px;cursor:pointer;font-size:15px;text-align:start;width:100%;font-family:inherit;\n  transition:.15s;direction:ltr;text-align:left;font-family:var(--en)}")
s = s.replace(".topic-card .en{color:var(--muted);font-size:12.5px;direction:ltr;text-align:start;\n  font-family:'Segoe UI',system-ui,sans-serif}",
              ".topic-card .en{color:var(--muted);font-size:12.5px;direction:ltr;text-align:start;\n  font-family:var(--en)}")
s = s.replace(".blk .en{margin:0;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".blk .en{margin:0;direction:ltr;text-align:left;font-family:var(--en);")
s = s.replace(".booklet .en{margin:0 0 9px;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".booklet .en{margin:0 0 9px;direction:ltr;text-align:left;font-family:var(--en);")
s = s.replace(".explain .en{margin:7px 0 0;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".explain .en{margin:7px 0 0;direction:ltr;text-align:left;font-family:var(--en);")
s = s.replace(".fc-en{margin:6px 0 0;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".fc-en{margin:6px 0 0;direction:ltr;text-align:left;font-family:var(--en);")
s = s.replace(".frm .en{margin:6px 0 0;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".frm .en{margin:6px 0 0;direction:ltr;text-align:left;font-family:var(--en);")
s = s.replace(".tip .en{margin:5px 0 0;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".tip .en{margin:5px 0 0;direction:ltr;text-align:left;font-family:var(--en);")
s = s.replace(".missed .en{margin:6px 0 0;direction:ltr;text-align:left;font-family:'Segoe UI',system-ui,sans-serif;",
              ".missed .en{margin:6px 0 0;direction:ltr;text-align:left;font-family:var(--en);")

ADD = """

/* ===== حلّ التمارين: حقول الفراغات ===== */
.item{direction:ltr;text-align:left;font-family:var(--en);font-size:15.5px;line-height:2.1;
  background:#fcfdfe;border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:6px 0}
.item .txt{white-space:pre-wrap}
.gap{display:inline-block;width:118px;min-width:80px;border:0;border-bottom:2px solid #94a3b8;
  background:#fff;border-radius:6px 6px 0 0;padding:2px 8px;font-family:var(--en);font-size:15px;
  color:var(--ink);text-align:center;outline:none;transition:.15s;margin:0 3px}
.gap:focus{border-bottom-color:var(--teal);background:#f0fdfa;box-shadow:0 2px 8px rgba(15,118,110,.12)}
.gap.ok{border-bottom-color:#15803d;background:var(--ok-bg);color:var(--ok);font-weight:600}
.gap.no{border-bottom-color:#b91c1c;background:var(--bad-bg);color:var(--bad)}
.gap:disabled{opacity:.85}
.hint{font-family:var(--en);font-size:12.5px;color:var(--muted);background:#f1f5f9;
  border:1px solid var(--line);border-radius:6px;padding:1px 7px;margin-inline-start:5px;
  white-space:nowrap;vertical-align:middle}
.ex-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:9px}
.btn.tiny{padding:7px 12px;font-size:13px;border-radius:9px;box-shadow:none}
.btn.tiny.ghost{background:#fff;color:var(--teal-d);border:1.5px solid var(--teal)}
.verdict{font-size:13px;font-weight:600}
.verdict.ok{color:var(--ok)}
.verdict.no{color:var(--bad)}
.answer{margin-top:8px;direction:ltr;text-align:left;font-family:var(--en);font-size:14.5px;
  background:var(--warn-bg);border:1px solid #fcd34d;border-radius:10px;padding:9px 12px}
.answer::before{content:'الحل: ';font-family:'Tajawal',sans-serif;font-weight:700;color:var(--warn)}
"""
if 'حلّ التمارين' not in s:
    s += ADD

io.open(DST, 'w', encoding='utf-8').write(s)
print('styles written:', len(s), 'bytes')
