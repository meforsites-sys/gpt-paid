# -*- coding: utf-8 -*-
"""Upgrades ALI MU'IZ ENGLISH 2027 from v1.12.2 to v1.13.0.

Changes (all inside the single HTML file):
  1. Fonts (Tajawal + Poppins) embedded as base64  -> works fully offline.
  2. 183-question bank injected, quiz engine rebuilt: unit filter, 10/20/all,
     instant feedback with explanation, stars result, mistakes review.
  3. Progress saved in localStorage; real statistics page + home strip + reset.
  4. Android WebView back button support (window.appBack).
  5. Version/about consistency (v1.13.0).

Source of truth for the build is the preserved original copy, so the script is
repeatable: python app/tools/upgrade_2027_v113.py
"""
import io, os, re, json, base64, sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'app', 'english2027', 'index.html')
BAK = os.path.join(ROOT, 'app', 'english2027', 'index_v1.12.2_original.html')
FONTS = os.path.join(ROOT, 'app', 'web', 'fonts')
QUIZ_JSON = os.path.join(ROOT, 'app', 'web', 'data', 'app.json')

if os.path.exists(BAK):
    src = io.open(BAK, encoding='utf-8').read()
else:
    src = io.open(OUT, encoding='utf-8').read()
    io.open(BAK, 'w', encoding='utf-8', newline='\n').write(src)


def b64(path, mime):
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode('ascii'))


taj_r = b64(os.path.join(FONTS, 'Tajawal-Regular.ttf'), 'font/ttf')
taj_b = b64(os.path.join(FONTS, 'Tajawal-Bold.ttf'), 'font/ttf')
pop_r = b64(os.path.join(FONTS, 'Poppins-Regular.woff2'), 'font/woff2')
pop_s = b64(os.path.join(FONTS, 'Poppins-SemiBold.woff2'), 'font/woff2')
pop_b = b64(os.path.join(FONTS, 'Poppins-Bold.woff2'), 'font/woff2')

FONT_CSS = (
    '<style id="embedded-fonts-v113">'
    "@font-face{font-family:'Tajawal';src:url(%s) format('truetype');font-weight:400 600;font-style:normal;font-display:swap}"
    "@font-face{font-family:'Tajawal';src:url(%s) format('truetype');font-weight:700 900;font-style:normal;font-display:swap}"
    "@font-face{font-family:'Poppins';src:url(%s) format('woff2');font-weight:400 500;font-style:normal;font-display:swap}"
    "@font-face{font-family:'Poppins';src:url(%s) format('woff2');font-weight:600;font-style:normal;font-display:swap}"
    "@font-face{font-family:'Poppins';src:url(%s) format('woff2');font-weight:700 900;font-style:normal;font-display:swap}"
    '</style>'
) % (taj_r, taj_b, pop_r, pop_s, pop_b)

UI_CSS = '''<style id="v113-ui">
/* ══ v1.13 — الاختبار والحفظ والإحصاء ══ */
.qz-setup{background:var(--wh);border:1px solid var(--bd);border-radius:16px;padding:16px;margin:10px 0 18px}
.qz-setup .tools{margin-bottom:10px}
.qz-setup .btn-p{width:100%}
.qz-links{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}
.qz-links .back{flex:1;text-align:center}
.qz-best{font-size:13px;color:var(--mu);margin:2px 2px 12px;line-height:1.9}
.qz-best b{color:var(--tl);font-family:'Poppins';font-size:13px}
.qz-bar{height:7px;border-radius:99px;background:#e7eef2;overflow:hidden;margin-bottom:12px}
.qz-bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--tl),var(--tm));transition:width .3s ease}
.qfb.good{background:#eaf8f1;border-color:#b6e3cd}
.qfb.bad{background:#fdeeec;border-color:#f0c3bd}
.qres .stars{display:flex;justify-content:center;gap:6px;font-size:30px;line-height:1;margin-bottom:6px}
.qres .stars .on{color:var(--gd)}
.qres .stars .off{color:#d9e2e8}
.qres .btn-g{background:var(--paper);border:1px solid var(--bd);color:var(--nv);margin-top:8px}
.qz-saved{font-size:12.5px;color:var(--mu)}
.qz-saved b{color:var(--tl);font-family:'Poppins'}
.rw{margin-top:20px;border-top:1px dashed var(--bd);padding-top:16px;text-align:right}
.rw h4{margin:0 0 10px;font-size:14px;color:var(--nv)}
.rw-item{border:1px solid #f0d9d5;background:#fdf4f2;border-radius:12px;padding:11px 13px;margin-bottom:9px}
.rw-item p{margin:0 0 5px;font-size:13px;line-height:1.7;color:#3a4d5c}
.rw-a{font-size:12.5px;color:var(--mu)}
.rw-a b{color:var(--ok);font-family:'Poppins'}
.rw-w{font-size:12px;color:#58707f;margin-top:5px;line-height:1.7}
.qz-block{background:var(--wh);border:1px solid var(--bd);border-radius:16px;padding:16px;margin-top:14px}
.qz-block h4{margin:0 0 12px;font-size:14px;color:var(--nv)}
.bar-row{margin-bottom:11px}
.bar-top{display:flex;justify-content:space-between;font-size:12.5px;color:#3a526b;margin-bottom:5px;gap:8px}
.bar-top span:last-child{font-family:'Poppins';color:var(--tl);font-weight:700}
.bar{height:8px;border-radius:99px;background:#e7eef2;overflow:hidden}
.bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--tl),var(--tm))}
.sg-mini{grid-template-columns:repeat(4,1fr);gap:8px}
.sg-mini .scard b{font-size:20px}
.sg-mini .scard small{font-size:10.5px}
.hp{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--wh);border:1px solid var(--bd);border-radius:14px;padding:12px 14px;margin:6px 0 14px}
.hp-item{text-align:center;min-width:62px}
.hp-item b{display:block;font:800 18px 'Poppins';color:var(--tl);line-height:1.2}
.hp-item span{font-size:10.5px;color:var(--mu)}
.hp-btn{margin-inline-start:auto;border:0;background:var(--tllt);color:var(--tl);font:700 12.5px 'Tajawal';padding:9px 13px;border-radius:10px;cursor:pointer}
.hp-empty{display:block;font-size:12.5px;color:var(--mu);background:var(--wh);border:1px dashed var(--bd);border-radius:14px;padding:12px 14px;margin:6px 0 14px;line-height:1.8}
.hp-empty b{color:var(--tl)}
@media (max-width:520px){.sg-mini{grid-template-columns:repeat(2,1fr)}}
</style>'''

MOD = r'''
/* ═══════════════════════════════════════════════════════════
   v1.13 — حفظ التقدم، بنك الأسئلة الكامل، ودعم زر الرجوع
   ═══════════════════════════════════════════════════════════ */
const STORE_KEY='aliEnglish2027.progress.v1';

function stLoad(){
  try{
    const raw=localStorage.getItem(STORE_KEY);
    const s=raw?JSON.parse(raw):{};
    return Object.assign({attempts:0,correct:0,total:0,best:0,units:{},days:[]},s);
  }catch(e){return {attempts:0,correct:0,total:0,best:0,units:{},days:[]};}
}
function stSave(s){try{localStorage.setItem(STORE_KEY,JSON.stringify(s));}catch(e){}}
function dayKey(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
function stStreak(s){
  if(!s.days||!s.days.length)return 0;
  const set=new Set(s.days);const d=new Date();
  if(!set.has(dayKey(d)))d.setDate(d.getDate()-1);
  let n=0;while(set.has(dayKey(d))){n++;d.setDate(d.getDate()-1);}
  return n;
}
function stLog(correct,total,unit){
  const s=stLoad();const pct=total?Math.round(correct/total*100):0;
  s.attempts++;s.correct+=correct;s.total+=total;
  if(pct>s.best)s.best=pct;
  const k=String(unit);
  if(!(k in s.units)||pct>s.units[k])s.units[k]=pct;
  if(!s.days)s.days=[];
  const t=dayKey(new Date());
  if(s.days.indexOf(t)<0)s.days.push(t);
  s.days=s.days.slice(-400);
  stSave(s);return s;
}
function stReset(){
  if(!window.confirm('سيتم حذف نتائجك المحفوظة كلها. هل تريد المتابعة؟'))return;
  try{localStorage.removeItem(STORE_KEY);}catch(e){}
  renderHomeProgress();_build('stats');
}
function shuffleArr(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const t=a[i];a[i]=a[j];a[j]=t;}return a;}
function unitArName(n){
  try{const u=(typeof UNITS_ALL!=='undefined'?UNITS_ALL:[]).find(x=>String(x.n)===String(n));if(u)return u.ar;}catch(e){}
  return 'الوحدة '+n;
}

/* ── الاختبار ── */
const QZ={items:[],i:0,sc:0,wrong:[],unit:'all'};
function qzUnits(){
  const seen={},out=[];
  QUIZ.forEach(q=>{if(!seen[q.unit]){seen[q.unit]=1;out.push(q.unit);}});
  return out.sort((a,b)=>a-b);
}
function testsHtml(){
  const opts=qzUnits().map(u=>`<option value="${u}">Unit ${u} · ${esc(unitArName(u))}</option>`).join('');
  return `<h2 class="pt fu">الاختبار</h2>
  <p class="ps fu d1">بنك تفاعلي من <b>${QUIZ.length}</b> سؤالاً في قواعد الوحدات. اختر الوحدة وعدد الأسئلة، وتظهر النتيجة والشرح فوراً.</p>
  <div class="qz-setup fu d2">
    <div class="tools">
      <select id="qzU"><option value="all">كل الوحدات</option>${opts}</select>
      <select id="qzN"><option value="10">10 أسئلة</option><option value="20">20 سؤالاً</option><option value="all">كل أسئلة الوحدة</option></select>
    </div>
    <div class="qz-best" id="qzBest"></div>
    <button class="btn-p" onclick="qzStart()">ابدأ الاختبار</button>
  </div>
  <div class="qz-links fu d3">
    <button class="back" onclick="showSection('exercises')">تمارين كتاب النشاط ←</button>
    <button class="back" onclick="showSection('literature')">تمارين الأدب ←</button>
  </div>
  <div id="qB"></div>`;
}
function qzBestInfo(){
  const el=document.getElementById('qzBest');if(!el)return;
  const s=stLoad();
  el.innerHTML=s.attempts
    ? `أفضل نتيجة: <b>${s.best}%</b> · محاولاتك: <b>${s.attempts}</b> · سلسلة: <b>${stStreak(s)}</b> يوم`
    : 'لم تجرِ أي محاولة بعد — النتائج تُحفظ على جهازك.';
}
function qzStart(){
  const uEl=document.getElementById('qzU'),nEl=document.getElementById('qzN');
  const unit=uEl?uEl.value:'all',size=nEl?nEl.value:'10';
  let pool=QUIZ.filter(q=>unit==='all'||String(q.unit)===unit);
  if(!pool.length)return;
  shuffleArr(pool);
  const n=size==='all'?pool.length:Math.min(parseInt(size,10)||10,pool.length);
  QZ.items=pool.slice(0,n).map(q=>{
    const opts=q.opts.map((t,i)=>({t:t,ok:i===q.ans}));
    shuffleArr(opts);
    return {q:q.q,opts:opts,ok:opts.findIndex(o=>o.ok),why:q.why||'',unit:q.unit};
  });
  QZ.i=0;QZ.sc=0;QZ.wrong=[];QZ.unit=unit;
  qzDraw();
}
function qzDraw(){
  const box=document.getElementById('qB');if(!box)return;
  if(QZ.i>=QZ.items.length){qzResult();return;}
  const x=QZ.items[QZ.i];
  const pct=Math.round(QZ.i/QZ.items.length*100);
  box.dataset.done='0';
  box.innerHTML=`<div class="qcard fu">
    <div class="qz-bar"><i style="width:${pct}%"></i></div>
    <div class="qprog">السؤال ${QZ.i+1} من ${QZ.items.length} · إجابات صحيحة: ${QZ.sc}</div>
    <p class="qq" dir="auto">${esc(x.q)}</p>
    <div class="qopts">${x.opts.map((o,j)=>`<button class="qo" onclick="qzAnswer(${j},this)" dir="auto">${esc(o.t)}</button>`).join('')}</div>
    <div id="qfb"></div></div>`;
  try{box.scrollIntoView({behavior:'smooth',block:'start'});}catch(e){}
}
function qzAnswer(j,btn){
  const box=document.getElementById('qB');if(!box||box.dataset.done==='1')return;
  box.dataset.done='1';
  const x=QZ.items[QZ.i];const ok=j===x.ok;
  if(ok)QZ.sc++;else QZ.wrong.push({q:x.q,correct:x.opts[x.ok].t,why:x.why});
  box.querySelectorAll('.qo').forEach((z,k)=>{z.disabled=true;if(k===x.ok)z.classList.add('ok');else if(k===j)z.classList.add('no');});
  const fb=document.getElementById('qfb');
  if(fb)fb.innerHTML=`<div class="qfb ${ok?'good':'bad'}">${ok?'✅ <b>إجابة صحيحة</b>':'❌ <b>الصحيحة:</b> '+esc(x.opts[x.ok].t)}${x.why?'<br>'+esc(x.why):''}</div>
    <button class="btn-p" style="margin-top:11px" onclick="qzNext()">${QZ.i===QZ.items.length-1?'عرض النتيجة':'السؤال التالي ←'}</button>`;
}
function qzNext(){
  const box=document.getElementById('qB');if(box)box.dataset.done='0';
  QZ.i++;qzDraw();
}
function qzResult(){
  const box=document.getElementById('qB');if(!box)return;
  const total=QZ.items.length;const pct=total?Math.round(QZ.sc/total*100):0;
  const s=stLog(QZ.sc,total,QZ.unit);
  const stars=pct>=90?3:pct>=70?2:1;
  const review=QZ.wrong.map(w=>`<div class="rw-item"><p dir="auto">${esc(w.q)}</p><div class="rw-a">الصحيحة: <b dir="auto">${esc(w.correct)}</b></div>${w.why?`<div class="rw-w" dir="auto">${esc(w.why)}</div>`:''}</div>`).join('');
  box.innerHTML=`<div class="qcard fu"><div class="qres">
    <div class="stars">${[1,2,3].map(i=>`<span class="${i<=stars?'on':'off'}">★</span>`).join('')}</div>
    <span class="sc">${QZ.sc}/${total}</span>
    <p>نسبة الإجابة الصحيحة: <b>${pct}%</b></p>
    <p style="font-size:18px">${pct>=90?'ممتاز! 🎉':pct>=70?'جيد جداً 👍':pct>=50?'جيد — راجع الأخطاء 📖':'تحتاج مراجعة 📚'}</p>
    <p class="qz-saved">أفضل نتيجة محفوظة: <b>${s.best}%</b></p>
    <button class="btn-p" onclick="qzStart()">إعادة الاختبار</button>
    <button class="btn-g" onclick="showSection('stats')">عرض تقدمي</button>
  </div>${review?`<div class="rw"><h4>مراجعة الأخطاء (${QZ.wrong.length})</h4>${review}</div>`:''}</div>`;
  qzBestInfo();renderHomeProgress();
  try{box.scrollIntoView({behavior:'smooth',block:'start'});}catch(e){}
}

/* ── الإحصاءات ── */
function statsHtml(){
  const s=stLoad();const acc=s.total?Math.round(s.correct/s.total*100):0;const streak=stStreak(s);
  const bars=qzUnits().map(u=>{
    const p=s.units[String(u)]||0;
    return `<div class="bar-row"><div class="bar-top"><span>Unit ${u} · ${esc(unitArName(u))}</span><span>${p?p+'%':'—'}</span></div><div class="bar"><i style="width:${p}%"></i></div></div>`;
  }).join('');
  const content=[['26','موضوعاً قواعدياً'],['8','وحدات'],['353','تمريناً محلولاً'],['353','بطاقة مراجعة']]
    .map(p=>`<div class="scard"><b>${p[0]}</b><small>${p[1]}</small></div>`).join('');
  return `<h2 class="pt fu">إحصائي</h2>
  <p class="ps fu d1">نتائجك تُحفظ على جهازك وتظهر هنا — بلا إنترنت ولا حساب.</p>
  <div class="sg fu d2">
    <div class="scard"><b>${s.best}%</b><small>أفضل نتيجة</small></div>
    <div class="scard"><b>${acc}%</b><small>دقة الإجابات</small></div>
    <div class="scard"><b>${s.total}</b><small>سؤالاً أجبت عنه</small></div>
    <div class="scard"><b>${s.attempts}</b><small>اختباراً مكتملاً</small></div>
    <div class="scard"><b>${streak}</b><small>يوم متتابع</small></div>
    <div class="scard"><b>${QUIZ.length}</b><small>سؤالاً في البنك</small></div>
  </div>
  <div class="qz-block fu d3"><h4>أفضل نتيجة لكل وحدة</h4>${bars||'<div class="empty">لا توجد نتائج بعد — ابدأ من قسم الاختبار.</div>'}</div>
  <div class="qz-block fu d4"><h4>محتوى التطبيق</h4><div class="sg sg-mini">${content}</div></div>
  <div class="about fu d5"><h4>حول التطبيق</h4><table>
    <tr><td>الاسم</td><td>إنكليزي السادس الإعدادي</td></tr>
    <tr><td>الإصدار</td><td>v1.13.0</td></tr>
    <tr><td>المنهج</td><td>English for Iraq · 8 وحدات + الأدب</td></tr>
    <tr><td>المعلم</td><td>الأستاذ علي معز الشلاه</td></tr>
    <tr><td>المركز</td><td>مكتب الوسام · الحلة، بابل</td></tr>
    <tr><td>العمل دون إنترنت</td><td>✅ الخطوط والمحتوى داخل التطبيق</td></tr>
    <tr><td>حفظ التقدم</td><td>✅ على الجهاز فقط</td></tr>
  </table></div>
  <button class="back" style="margin-top:16px" onclick="stReset()">تصفير النتائج المحفوظة</button>`;
}
function renderHomeProgress(){
  const el=document.getElementById('homeProgress');if(!el)return;
  const s=stLoad();
  if(!s.attempts){
    el.innerHTML=`<div class="hp-empty">لم تبدأ اختباراً بعد — <b>${QUIZ.length} سؤالاً</b> تنتظرك في قسم «الاختبار».</div>`;
    return;
  }
  el.innerHTML=`<div class="hp">
    <div class="hp-item"><b>${s.best}%</b><span>أفضل نتيجة</span></div>
    <div class="hp-item"><b>${s.total?Math.round(s.correct/s.total*100):0}%</b><span>دقة الإجابات</span></div>
    <div class="hp-item"><b>${stStreak(s)}</b><span>يوم متتابع</span></div>
    <button class="hp-btn" onclick="showSection('tests')">تابع التدريب ←</button>
  </div>`;
}

/* ── زر الرجوع في أندرويد ── */
window.appBack=function(){
  try{
    const w=document.getElementById('welcomeScreen');
    if(w&&w.style.display!=='none'&&!w.classList.contains('is-leaving')){startApp();return true;}
    const p=document.getElementById('contentPanel');
    if(p&&!p.hidden){goHome();return true;}
  }catch(e){}
  return false;
};
window.addEventListener('load',renderHomeProgress);
'''

h = src

# 1) Title / version
h = h.replace("ALI MU'IZ ENGLISH 2027 · v1.12.2", "ALI MU'IZ ENGLISH 2027 · v1.13.0")

# 2) Google Fonts -> embedded fonts
link = ('<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900'
        '&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">')
if link not in h:
    raise SystemExit('font link not found')
h = h.replace(link, FONT_CSS, 1)

# 3) UI styles
h = h.replace('</head>', UI_CSS + '\n</head>', 1)

# 4) Quiz bank
data = json.load(io.open(QUIZ_JSON, encoding='utf-8'))
quests = []
for t in data['topics']:
    for q in (t.get('quiz') or []):
        quests.append({'q': q['q'], 'opts': q['opts'], 'ans': q['ans'], 'why': q.get('why', ''),
                       'unit': q['unit'], 'topic': q['topic']})
bank_json = json.dumps(quests, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
bank_tag = '<script id="quiz-bank-v113">window.QUIZ_BANK=%s;</script>\n' % bank_json
anchor = '<script>\nfunction startApp(){'
if anchor not in h:
    raise SystemExit('main script anchor not found')
h = h.replace(anchor, bank_tag + anchor, 1)

# 5) Old 10-question array -> full bank
h, n_q = re.subn(r"const QUIZ=\[.*?\n\];", "const QUIZ=window.QUIZ_BANK||[];", h, count=1, flags=re.S)
if n_q != 1:
    raise SystemExit('QUIZ array not replaced')

# 6) Quiz engine
h, n_r = re.subn(r"function rQuiz\(\)\{.*?\n// ── LITERATURE ──",
                 MOD + "\n// ── LITERATURE ──", h, count=1, flags=re.S)
if n_r != 1:
    raise SystemExit('rQuiz not replaced')

# 7) Tests section
h, n_t = re.subn(r"  if\(key==='tests'\)\{ pb\.innerHTML=.*?; return; \}",
                 "  if(key==='tests'){ pb.innerHTML=testsHtml(); qzBestInfo(); return; }",
                 h, count=1, flags=re.S)
if n_t != 1:
    raise SystemExit('tests section not replaced')

# 8) Stats section
h, n_s = re.subn(r"  if\(key==='stats'\)\{.*?\n  if\(key==='search'\)\{",
                 "  if(key==='stats'){ pb.innerHTML=statsHtml(); return; }\n  if(key==='search'){",
                 h, count=1, flags=re.S)
if n_s != 1:
    raise SystemExit('stats section not replaced')

# 9) Home progress strip
old_ss = '<div class="ss fu d2">الوحدات والدروس والتمارين والشروحات في واجهة واحدة</div>'
if old_ss not in h:
    raise SystemExit('home subtitle not found')
h = h.replace(old_ss, old_ss + '\n    <div id="homeProgress" class="fu d3"></div>', 1)

# 10) Search wording (it searches every unit, not only unit 1)
h = h.replace('ابحث في تمارين الوحدة الأولى.', 'ابحث في جميع التمارين (كل الوحدات).')

io.open(OUT, 'w', encoding='utf-8', newline='\n').write(h)

print('OK  ->', OUT)
print('size: %.0f KB' % (os.path.getsize(OUT) / 1024))
print('questions injected:', len(quests))
print('checks:',
      'embedded-fonts' if 'embedded-fonts-v113' in h else 'NO-FONTS',
      '| quiz-bank' if 'quiz-bank-v113' in h else '| NO-BANK',
      '| stats' if 'statsHtml' in h else '| NO-STATS',
      '| appBack' if 'window.appBack' in h else '| NO-BACK')
