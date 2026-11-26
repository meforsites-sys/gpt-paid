/* انكليزي السادس الاعدادي | منطق التطبيق */
(function () {
'use strict';

var D = window.APP_DATA;
var TOPICS = D.topics, UNITS = D.meta.units;
var byId = {}; TOPICS.forEach(function (t) { byId[t.id] = t; });

/* ---------------- التخزين ---------------- */
var LS_KEY = 'grammar6_state_v1';
var S = load();
function load() {
  try {
    var raw = localStorage.getItem(LS_KEY);
    if (raw) { var o = JSON.parse(raw); if (o && typeof o === 'object') return o; }
  } catch (e) {}
  return { stats: { answered: 0, correct: 0 }, byTopic: {}, cards: {} };
}
function save() { try { localStorage.setItem(LS_KEY, JSON.stringify(S)); } catch (e) {} }
function topicStat(id) {
  if (!S.byTopic[id]) S.byTopic[id] = { answered: 0, correct: 0 };
  return S.byTopic[id];
}

/* ---------------- أدوات ---------------- */
function el(tag, cls, html) {
  var n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  return n;
}
function esc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function toast(msg) {
  var t = document.getElementById('toast');
  t.textContent = msg; t.hidden = false;
  clearTimeout(t._tm); t._tm = setTimeout(function () { t.hidden = true; }, 1900);
}
function shuffle(a) {
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1)), x = a[i]; a[i] = a[j]; a[j] = x;
  }
  return a;
}
function rand(n) { return Math.floor(Math.random() * n); }

/* ---------------- التبويبات ---------------- */
var currentView = 'ref';
function showView(v) {
  currentView = v;
  document.querySelectorAll('.tab').forEach(function (b) {
    b.classList.toggle('active', b.dataset.view === v);
  });
  document.querySelectorAll('.view').forEach(function (s) {
    s.classList.toggle('active', s.id === 'view-' + v);
  });
  window.scrollTo(0, 0);
  if (v === 'stats') renderStats();
  if (v === 'quiz' && !quizSession && document.getElementById('quizResult').hidden) {
    document.getElementById('quizSetup').hidden = false;
    renderQuizSetup();
  }
  if (v === 'cards' && !cardSession) {
    document.getElementById('cardsSetup').hidden = false;
    renderCardsSetup();
  }
  if (v === 'exam') {
    if (exState.started && !exState.finished) {
      document.getElementById('examSetup').hidden = true;
      document.getElementById('examSession').hidden = false;
      renderExamPart();
    } else if (exState.finished) {
      renderExamResult();
    } else {
      document.getElementById('examSession').hidden = true;
      document.getElementById('examResult').hidden = true;
      document.getElementById('examSetup').hidden = false;
      renderExamSetup();
    }
  }
}
document.querySelectorAll('.tab').forEach(function (b) {
  b.addEventListener('click', function () { showView(b.dataset.view); });
});

/* ================= المرجع ================= */
var curUnit = 1;

function renderUnitChips() {
  var box = document.getElementById('unitChips');
  box.innerHTML = '';
  UNITS.forEach(function (u) {
    var c = el('button', 'chip' + (u.id === curUnit ? ' active' : ''));
    c.innerHTML = esc(u.ar) + ' <small>' + u.topics.length + '</small>';
    c.onclick = function () { curUnit = u.id; renderUnitChips(); renderTopicList(); };
    box.appendChild(c);
  });
}

function renderTopicList(filter) {
  var box = document.getElementById('topicList');
  box.innerHTML = '';
  var searching = !!filter;
  var list = TOPICS.filter(function (t) {
    return searching ? filter(t) : t.unit === curUnit;
  });
  if (!list.length) {
    var unit = UNITS.filter(function (u) { return u.id === curUnit; })[0];
    var msg = searching
      ? '<div class="empty"><div class="big">🔍</div>لا توجد نتائج مطابقة لبحثك'
      : '<div class="empty"><div class="big">📘</div><b>' + esc(unit.ar) + '</b><br>' +
        'لا تحتوي هذه الوحدة مواضيع جديدة؛ فمحتواها مدمج داخل الموضوعات التي ظهرت أول مرة ' +
        'في الوحدات السابقة. اختر وحدة أخرى من الأعلى.';
    box.appendChild(el('div', 'empty', msg));
    return;
  }
  list.forEach(function (t) {
    var c = el('div', 'topic-card');
    var st = topicStat(t.id);
    var acc = st.answered ? Math.round(st.correct * 100 / st.answered) : null;
    c.innerHTML =
      '<h3>' + esc(t.ar) + '</h3>' +
      '<div class="en">' + esc(t.en) + '</div>' +
      '<div class="row">' +
        (searching ? '<span class="tag t-teal">' + esc(t.unitAr) + '</span>' : '') +
        '<span class="tag t-teal">' + t.quiz.length + ' سؤال</span>' +
        '<span class="tag">' + t.cards.length + ' بطاقة</span>' +
        (t.exercises.length ? '<span class="tag t-amber">' + t.exercises.length + ' تمرين كتاب</span>' : '') +
        (acc !== null ? '<span class="tag ' + (acc >= 70 ? 't-green' : '') + '">إتقان ' + acc + '%</span>' : '') +
      '</div>';
    c.onclick = function () { openTopic(t.id); };
    box.appendChild(c);
  });
}

function openTopic(id) {
  var t = byId[id];
  var body = document.getElementById('topicSheetBody');
  var h = '';
  h += '<div class="sheet-grab"><i></i></div>';
  h += '<div class="sheet-title"><h2>' + esc(t.ar) + '</h2>' +
       '<button class="sheet-close" data-close="1"><svg viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"/></svg></button></div>';
  h += '<div class="muted" style="direction:ltr;text-align:left;font-family:Poppins,sans-serif">' + esc(t.en) + '</div>';
  h += '<div class="row" style="display:flex;gap:7px;flex-wrap:wrap;margin:8px 0 2px">' +
       '<span class="tag t-teal">' + esc(t.unitAr) + '</span>' +
       '<span class="tag">' + t.quiz.length + ' سؤال تفاعلي</span>' +
       '<span class="tag">' + t.cards.length + ' بطاقة</span></div>';

  h += '<div class="sec-title">القاعدة</div>';
  h += '<div class="rule-ar">' + t.ruleAr + '</div>';
  h += '<div class="rule-en">' + esc(t.ruleEn).replace(/\n/g, '<br>') + '</div>';

  if (t.forms.length) {
    h += '<div class="sec-title">الصيغ</div><div class="card"><table class="forms"><thead><tr>' +
         '<th>الوظيفة</th><th>الصيغة</th><th>مثال</th><th>المعنى</th></tr></thead><tbody>';
    t.forms.forEach(function (f) {
      h += '<tr><td>' + esc(f.label) + '</td><td class="form">' + esc(f.form) + '</td>' +
           '<td class="ex-en">' + esc(f.exEn) + '</td><td>' + esc(f.exAr) + '</td></tr>';
    });
    h += '</tbody></table></div>';
  }
  if (t.tips.length) {
    h += '<div class="sec-title">انتبه</div><div class="card"><ul class="tips">' +
         t.tips.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul></div>';
  }

  h += '<div class="sec-title">التمارين من كتاب النشاط (' + t.exercises.length + ')</div>';
  if (!t.exercises.length) {
    h += '<div class="card muted">لا توجد تمارين مرفقة بهذا الموضوع.</div>';
  } else {
    t.exercises.forEach(function (e, i) {
      h += '<div class="ex-card" data-ex="' + i + '">' +
        '<div class="ex-head"><span class="t">' + esc(e.title) + '</span>' +
        '<span class="pos">' + (e.page ? 'ص ' + e.page : '') + (e.letter ? ' · ' + esc(e.letter) : '') + '</span>' +
        '<span class="chev">▼</span></div>' +
        '<div class="ex-body">' +
          (e.script ? '<div class="script">' + esc(e.scriptRaw) + '</div>' : '') +
          (e.trans ? '<div class="trans">' + e.trans + '</div>' : '') +
          (e.items.length ? '<ul class="items">' + e.items.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>' : '') +
          (e.summary ? '<div class="summary">' + e.summary + '</div>' : '') +
        '</div></div>';
    });
  }

  h += '<div class="btn-row"><button class="btn" id="tQuiz">تدريب على هذا الموضوع</button>' +
       '<button class="btn ghost" id="tCards">بطاقات الموضوع</button></div>';

  body.innerHTML = h;
  var sheet = document.getElementById('topicSheet');
  sheet.hidden = false;
  document.body.style.overflow = 'hidden';

  body.querySelectorAll('.ex-head').forEach(function (hd) {
    hd.onclick = function () { hd.parentNode.classList.toggle('open'); };
  });
  body.querySelector('#tQuiz').onclick = function () {
    closeSheet();
    startQuiz({ topics: [t.id], count: Math.min(t.quiz.length, 10) });
  };
  body.querySelector('#tCards').onclick = function () {
    closeSheet();
    startCards({ topics: [t.id] });
  };
  sheet.querySelectorAll('[data-close]').forEach(function (n) {
    n.onclick = closeSheet;
  });
}
function closeSheet() {
  document.getElementById('topicSheet').hidden = true;
  document.body.style.overflow = '';
}

/* ---------------- البحث ---------------- */
var searchBar = document.getElementById('searchbar');
document.getElementById('btnSearch').onclick = function () {
  searchBar.hidden = !searchBar.hidden;
  if (!searchBar.hidden) { document.getElementById('searchInput').focus(); }
  else { document.getElementById('searchInput').value = ''; renderTopicList(); }
};
document.getElementById('btnSearchClose').onclick = function () {
  searchBar.hidden = true;
  document.getElementById('searchInput').value = '';
  renderTopicList();
};
document.getElementById('searchInput').oninput = function (e) {
  var q = e.target.value.trim().toLowerCase();
  if (!q) { renderTopicList(); return; }
  renderTopicList(function (t) {
    var hay = (t.ar + ' ' + t.en + ' ' + t.ruleAr + ' ' + t.ruleEn + ' ' +
      t.exercises.map(function (x) { return x.title + ' ' + x.scriptRaw + ' ' + x.trans; }).join(' ')).toLowerCase();
    return hay.indexOf(q) !== -1;
  });
};

/* ================= التمارين ================= */
var quizSession = null;

function renderQuizSetup() {
  var box = document.getElementById('quizSetup');
  var h = '<div class="card"><h2>🎯 ابدأ تمرينًا</h2>' +
    '<p class="muted">اختر الوحدة أو الموضوع، وستظهر أسئلة مع التصحيح الفوري وشرح الإجابة.</p>' +
    '<div class="sec-title">الوحدة</div><div class="chips" id="qUnits"></div>' +
    '<div class="sec-title">الموضوع</div><div class="chips" id="qTopics"></div>' +
    '<div class="sec-title">عدد الأسئلة</div><div class="chips" id="qCount">' +
    '<button class="chip" data-c="5">5</button><button class="chip active" data-c="10">10</button>' +
    '<button class="chip" data-c="20">20</button><button class="chip" data-c="0">الكل</button></div>' +
    '<div class="btn-row"><button class="btn full" id="qStart">ابدأ التمرين</button></div>' +
    '</div>';
  var totals = '<div class="card"><div class="sec-title">إحصاؤك</div><div class="stat-grid">' +
    '<div class="stat"><div class="n">' + S.stats.answered + '</div><div class="l">سؤال مُجاب</div></div>' +
    '<div class="stat"><div class="n">' + S.stats.correct + '</div><div class="l">إجابة صحيحة</div></div>' +
    '<div class="stat"><div class="n">' + (S.stats.answered ? Math.round(S.stats.correct * 100 / S.stats.answered) : 0) + '%</div><div class="l">نسبة الإتقان</div></div>' +
    '</div></div>';
  box.innerHTML = h + totals;

  var sel = { unit: 1, topic: 0, count: 10 };
  function paintTopics() {
    var box2 = document.getElementById('qTopics');
    box2.innerHTML = '';
    var ul = UNITS.filter(function (u) { return u.id === sel.unit; })[0];
    var all = el('button', 'chip' + (sel.topic === 0 ? ' active' : ''));
    all.innerHTML = 'كل موضوعات الوحدة <small>' + ul.quizCount + '</small>';
    all.onclick = function () { sel.topic = 0; paintTopics(); };
    box2.appendChild(all);
    ul.topics.forEach(function (tid) {
      var t = byId[tid];
      var c = el('button', 'chip' + (sel.topic === tid ? ' active' : ''));
      c.innerHTML = esc(t.ar) + ' <small>' + t.quiz.length + '</small>';
      c.onclick = function () { sel.topic = tid; paintTopics(); };
      box2.appendChild(c);
    });
  }
  function paintUnits() {
    var box2 = document.getElementById('qUnits');
    box2.innerHTML = '';
    UNITS.forEach(function (u) {
      if (!u.quizCount) return;
      var c = el('button', 'chip' + (sel.unit === u.id ? ' active' : ''));
      c.innerHTML = esc(u.ar) + ' <small>' + u.quizCount + '</small>';
      c.onclick = function () { sel.unit = u.id; sel.topic = 0; paintUnits(); paintTopics(); };
      box2.appendChild(c);
    });
  }
  paintUnits(); paintTopics();
  box.querySelectorAll('#qCount .chip').forEach(function (c) {
    c.onclick = function () {
      sel.count = parseInt(c.dataset.c, 10);
      box.querySelectorAll('#qCount .chip').forEach(function (x) { x.classList.remove('active'); });
      c.classList.add('active');
    };
  });
  document.getElementById('qStart').onclick = function () {
    var ids = sel.topic ? [sel.topic] : UNITS.filter(function (u) { return u.id === sel.unit; })[0].topics;
    startQuiz({ topics: ids, count: sel.count });
  };
}

function startQuiz(opt) {
  var pool = [];
  opt.topics.forEach(function (id) { pool = pool.concat(byId[id].quiz); });
  if (!pool.length) { toast('لا توجد أسئلة في هذا الاختيار'); return; }
  pool = shuffle(pool.slice());
  var n = opt.count ? Math.min(opt.count, pool.length) : pool.length;
  pool = pool.slice(0, n);

  quizSession = { list: pool, i: 0, answers: [], startedAt: Date.now() };
  document.getElementById('quizSetup').hidden = true;
  document.getElementById('quizResult').hidden = true;
  document.getElementById('quizSession').hidden = false;
  showView('quiz');
  renderQuestion();
}

function renderQuestion() {
  var s = quizSession;
  var q = s.list[s.i];
  var t = byId[q.topic];
  var box = document.getElementById('quizSession');
  var pct = Math.round(s.i * 100 / s.list.length);
  var h = '<div class="quiz-head"><span class="muted">' + esc(t.ar) + '</span>' +
          '<span class="cnt">' + (s.i + 1) + ' / ' + s.list.length + '</span></div>' +
          '<div class="progress"><i style="width:' + pct + '%"></i></div>' +
          '<div class="q-card"><div class="q-num">سؤال ' + (s.i + 1) + '</div>' +
          '<div class="q-text">' + esc(q.q) + '</div>' +
          '<div class="opts" id="opts">';
  q.opts.forEach(function (o, k) {
    h += '<button class="opt" data-k="' + k + '"><span class="mark">' + 'ABCD'[k] + '</span><span>' + esc(o) + '</span></button>';
  });
  h += '</div><div id="fb"></div></div>' +
       '<div class="btn-row"><button class="btn ghost" id="qQuit">إنهاء التمرين</button>' +
       '<button class="btn" id="qNext" hidden>التالي ←</button></div>';
  box.innerHTML = h;

  box.querySelectorAll('.opt').forEach(function (b) {
    b.onclick = function () { answer(k_(b), b); };
  });
  function k_(b) { return parseInt(b.dataset.k, 10); }

  box.querySelector('#qNext').onclick = function () {
    s.i++;
    if (s.i >= s.list.length) renderQuizResult();
    else renderQuestion();
  };
  box.querySelector('#qQuit').onclick = function () { renderQuizResult(true); };
}

function answer(k, btn) {
  var s = quizSession, q = s.list[s.i];
  if (s.answers[s.i] !== undefined) return;
  s.answers[s.i] = k;
  var ok = (k === q.ans);
  var opts = document.querySelectorAll('#opts .opt');
  opts.forEach(function (o) {
    o.classList.add('locked');
    var kk = parseInt(o.dataset.k, 10);
    if (kk === q.ans) o.classList.add('correct');
    else if (kk === k) o.classList.add('wrong');
  });
  S.stats.answered++; if (ok) S.stats.correct++;
  var ts = topicStat(q.topic); ts.answered++; if (ok) ts.correct++;
  save();

  var fb = document.getElementById('fb');
  fb.innerHTML = '<div class="explain ' + (ok ? 'ok' : 'no') + '">' +
    '<div class="h">' + (ok ? '✅ إجابة صحيحة' : '❌ إجابة غير صحيحة') + '</div>' +
    (ok ? '' : '<div style="margin-bottom:4px">الإجابة الصحيحة: <b>' + esc(q.opts[q.ans]) + '</b></div>') +
    esc(q.why) + '</div>';
  document.getElementById('qNext').hidden = false;
  document.getElementById('qNext').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function renderQuizResult(quit) {
  var s = quizSession;
  if (!s) return;
  var done = s.answers.filter(function (a) { return a !== undefined; });
  var right = done.filter(function (a, i) { return a === s.list[i].ans; }).length;
  var pct = done.length ? Math.round(right * 100 / done.length) : 0;
  var missed = [];
  s.list.forEach(function (q, i) {
    if (s.answers[i] !== q.ans) missed.push(q);
  });
  var h = '<div class="card center">' +
    '<div class="score-ring" style="--p:' + pct + '%"><div class="v">' + pct + '%<small>' + right + ' من ' + done.length + '</small></div></div>' +
    '<h2>' + (quit ? 'تم إنهاء التمرين' : (pct >= 80 ? 'ممتاز! 🎉' : pct >= 50 ? 'جيد، واصل! 💪' : 'تحتاج مراجعة 🔁')) + '</h2>' +
    '<p class="muted">أجبت على ' + done.length + ' سؤال من ' + s.list.length + '</p>' +
    '<div class="btn-row"><button class="btn" id="rAgain">إعادة نفس التمرين</button>' +
    '<button class="btn ghost" id="rNew">تمرين جديد</button></div></div>';
  if (missed.length) {
    h += '<div class="sec-title">راجع الأخطاء (' + missed.length + ')</div>';
    missed.forEach(function (q) {
      h += '<div class="missed"><div class="q">' + esc(q.q) + '</div>' +
        '<div class="a">الإجابة: <b>' + esc(q.opts[q.ans]) + '</b></div>' +
        '<div class="a muted">' + esc(q.why) + '</div></div>';
    });
  }
  var box = document.getElementById('quizResult');
  box.innerHTML = h;
  box.hidden = false;
  document.getElementById('quizSession').hidden = true;
  document.getElementById('quizSetup').hidden = true;
  box.querySelector('#rAgain').onclick = function () {
    startQuiz({ topics: Array.from(new Set(s.list.map(function (q) { return q.topic; }))), count: s.list.length });
  };
  box.querySelector('#rNew').onclick = function () {
    quizSession = null;
    box.hidden = true;
    document.getElementById('quizSetup').hidden = false;
    renderQuizSetup();
  };
  quizSession = null;
  renderTopicList();
}

/* ================= البطاقات ================= */
var cardSession = null;

function renderCardsSetup() {
  var box = document.getElementById('cardsSetup');
  var h = '<div class="card"><h2>🃏 بطاقات المراجعة</h2>' +
    '<p class="muted">اقلب البطاقة لترى الإجابة، ثم حدّد: أعرفها / لم أعرفها. ' +
    'البطاقات التي لم تعرفها تعود في نهاية الجولة.</p>' +
    '<div class="sec-title">الوحدة</div><div class="chips" id="cUnits"></div>' +
    '<div class="sec-title">الموضوع</div><div class="chips" id="cTopics"></div>' +
    '<div class="btn-row"><button class="btn full" id="cStart">ابدأ البطاقات</button></div></div>';
  box.innerHTML = h;
  var sel = { unit: 1, topic: 0 };
  function paintTopics() {
    var b = document.getElementById('cTopics'); b.innerHTML = '';
    var ul = UNITS.filter(function (u) { return u.id === sel.unit; })[0];
    var all = el('button', 'chip' + (sel.topic === 0 ? ' active' : ''));
    all.textContent = 'كل موضوعات الوحدة';
    all.onclick = function () { sel.topic = 0; paintTopics(); };
    b.appendChild(all);
    ul.topics.forEach(function (tid) {
      var t = byId[tid];
      var c = el('button', 'chip' + (sel.topic === tid ? ' active' : ''));
      c.innerHTML = esc(t.ar) + ' <small>' + t.cards.length + '</small>';
      c.onclick = function () { sel.topic = tid; paintTopics(); };
      b.appendChild(c);
    });
  }
  function paintUnits() {
    var b = document.getElementById('cUnits'); b.innerHTML = '';
    UNITS.forEach(function (u) {
      if (!u.topics.length) return;
      var c = el('button', 'chip' + (sel.unit === u.id ? ' active' : ''));
      c.innerHTML = esc(u.ar) + ' <small>' + u.topics.length + '</small>';
      c.onclick = function () { sel.unit = u.id; sel.topic = 0; paintUnits(); paintTopics(); };
      b.appendChild(c);
    });
  }
  paintUnits(); paintTopics();
  document.getElementById('cStart').onclick = function () {
    var ids = sel.topic ? [sel.topic] : UNITS.filter(function (u) { return u.id === sel.unit; })[0].topics;
    startCards({ topics: ids });
  };
}

function startCards(opt) {
  var pool = [];
  opt.topics.forEach(function (id) { pool = pool.concat(byId[id].cards); });
  if (!pool.length) { toast('لا توجد بطاقات'); return; }
  pool = shuffle(pool.slice());
  cardSession = { queue: pool.slice(), i: 0, again: [], known: 0, unknown: 0 };
  document.getElementById('cardsSetup').hidden = true;
  document.getElementById('cardsSession').hidden = false;
  showView('cards');
  renderCard();
}

function renderCard() {
  var s = cardSession;
  var box = document.getElementById('cardsSession');
  if (!s.queue.length) {
    box.innerHTML = '<div class="card center"><div style="font-size:44px">🎉</div>' +
      '<h2>انتهت الجولة!</h2><p class="muted">أعرفت ' + s.known + ' بطاقة واحتجت ' + s.unknown + ' بطاقة</p>' +
      '<div class="btn-row"><button class="btn" id="cRestart">جولة جديدة</button>' +
      '<button class="btn ghost" id="cBack">القائمة</button></div></div>';
    box.querySelector('#cRestart').onclick = function () {
      var t = s.queue.slice(); startCards({ topics: Array.from(new Set(t.map(function (c) { return c.topic; }))) });
    };
    box.querySelector('#cBack').onclick = function () {
      cardSession = null; box.hidden = true;
      document.getElementById('cardsSetup').hidden = false; renderCardsSetup();
    };
    return;
  }
  var c = s.queue[s.i];
  var pct = Math.round(s.i * 100 / s.queue.length);
  var h = '<div class="quiz-head"><span class="muted">' + esc(byId[c.topic].ar) + '</span>' +
          '<span class="cnt">' + (s.i + 1) + ' / ' + s.queue.length + '</span></div>' +
          '<div class="progress"><i style="width:' + pct + '%"></i></div>' +
          '<div class="flashcard" id="fc"><div class="fc-inner">' +
            '<div class="fc-face fc-front"><div class="fc-label">السؤال</div>' +
              '<div class="fc-q">' + esc(c.frontEn) + '</div>' +
              (c.frontAr ? '<div class="fc-ar muted">' + esc(c.frontAr) + '</div>' : '') +
              '<div class="fc-hint">اضغط البطاقة لقلبها 👆</div></div>' +
            '<div class="fc-face fc-back"><div class="fc-label">الإجابة</div>' +
              '<div class="fc-a">' + esc(c.backEn) + '</div>' +
              (c.backAr ? '<div class="fc-ar">' + esc(c.backAr) + '</div>' : '') + '</div>' +
          '</div></div>' +
          '<div class="btn-row"><button class="btn gray" id="cNo">لم أعرفها</button>' +
          '<button class="btn" id="cYes">أعرفها ✓</button></div>';
  box.innerHTML = h;
  var fc = document.getElementById('fc');
  fc.onclick = function () { fc.classList.toggle('flip'); };
  box.querySelector('#cYes').onclick = function () { gradeCard(true); };
  box.querySelector('#cNo').onclick = function () { gradeCard(false); };
}

function gradeCard(known) {
  var s = cardSession;
  var c = s.queue[s.i];
  if (!S.cards[c.id]) S.cards[c.id] = { seen: 0, known: false };
  S.cards[c.id].seen++; S.cards[c.id].known = known;
  save();
  if (known) { s.known++; s.queue.splice(s.i, 1); }
  else { s.unknown++; s.queue.push(c); s.i++; }
  renderCard();
}

/* ================= الإحصائي ================= */
function renderStats() {
  var box = document.getElementById('statsPanel');
  var pct = S.stats.answered ? Math.round(S.stats.correct * 100 / S.stats.answered) : 0;
  var h = '<div class="card center">' +
    '<div class="score-ring" style="--p:' + pct + '%"><div class="v">' + pct + '%<small>نسبة الإتقان</small></div></div>' +
    '<div class="stat-grid">' +
    '<div class="stat"><div class="n">' + S.stats.answered + '</div><div class="l">سؤال مُجاب</div></div>' +
    '<div class="stat"><div class="n">' + S.stats.correct + '</div><div class="l">صحيحة</div></div>' +
    '<div class="stat"><div class="n">' + (S.stats.answered - S.stats.correct) + '</div><div class="l">خطأ</div></div>' +
    '</div></div>';

  h += '<div class="card"><div class="sec-title">التقدّم حسب الوحدة</div>';
  UNITS.forEach(function (u) {
    var a = 0, c = 0;
    u.topics.forEach(function (tid) { var s = topicStat(tid); a += s.answered; c += s.correct; });
    var p = a ? Math.round(c * 100 / a) : 0;
    h += '<div class="unit-row"><div class="top"><span>' + esc(u.ar) + '</span><span class="muted">' +
         (a ? c + '/' + a + ' · ' + p + '%' : 'لم تبدأ') + '</span></div>' +
         '<div class="bar"><i style="width:' + p + '%"></i></div></div>';
  });
  h += '</div>';

  h += '<div class="card"><div class="sec-title">المواضيع</div>';
  TOPICS.forEach(function (t) {
    var s = topicStat(t.id);
    var p = s.answered ? Math.round(s.correct * 100 / s.answered) : 0;
    h += '<div class="unit-row"><div class="top"><span>' + esc(t.ar) + '</span>' +
         '<span class="muted">' + (s.answered ? p + '%' : '—') + '</span></div>' +
         '<div class="bar"><i style="width:' + p + '%"></i></div></div>';
  });
  h += '</div>';
  h += '<div class="card"><button class="btn gray full" id="stReset">تصفير الإحصائيات</button></div>';
  h += '<div class="card"><div class="sec-title">حول التطبيق <span class="tag t-teal">الإصدار 1.5</span></div>' +
       '<div class="muted" style="line-height:2">منهج الصف السادس الإعدادي في اللغة الإنجليزية يتكوّن من ثماني وحدات، ومادتها الأساسية <b>كتاب النشاط</b> الذي تُبنى عليه الورقة الوزارية: الحكاية بالماضي البسيط والمستمر، الخطط والتعبير عن المستقبل، الفرضيات والشرط (if / wish / if only)، الأزمنة التامة، المبني للمجهول والاستنتاج، المستقبل، والمراجعات الشاملة — إضافة إلى مادة الأدب (رواية <span class="ltr">Pride and Prejudice</span>). ولأن أسئلة الوزارية تنطلق من تمارين كتاب النشاط، رُتّبت التمارين هنا بترتيب صفحات الكتاب نفسها لكل موضوع.<br>' +
       '<b>فائدة الطالب من التطبيق:</b><br>' +
       '• ' + D.meta.stats.topics + ' موضوعًا قواعديًا مشروحًا بالعربية والإنكليزية (القاعدة + جدول الصيغ + تنبيهات).<br>' +
       '• ' + D.meta.stats.exercises + ' تمرينًا من كتاب النشاط — كأنك تمرّس الكتاب نفسه من هاتفك.<br>' +
       '• ' + D.meta.stats.quiz + ' سؤالًا تفاعليًا بتصحيح فوري وشرح للإجابة الصحيحة.<br>' +
       '• ' + D.meta.stats.cards + ' بطاقة مراجعة سريعة، ومن نسيها تعود إليه في نهاية الجولة.<br>' +
       '• امتحان وزاري محاكي لنموذج 2027 بتصحيح تلقائي ودرجة من 110 مع مراجعة كل خطأ.<br>' +
       '• متابعة تقدّمك لكل وحدة وموضوع، ويعمل دون إنترنت تمامًا. تقدّمك محفوظ على جهازك.<br>' +
       'المصدر: ' + esc(D.meta.source) + '</div></div>';

  h += '<div class="card center">' +
    '<div class="muted" style="font-size:12.5px;letter-spacing:.5px">إعداد وتأليف</div>' +
    '<div style="font-size:17.5px;font-weight:800;margin:4px 0 2px">الأستاذ علي معز الشلاه</div>' +
    '<div class="muted">مدرس اللغة الإنجليزية</div>' +
    '<div class="btn-row"><a class="btn ghost" href="tel:07806611177" style="text-decoration:none">📞 07806611177</a></div></div>';

  box.innerHTML = h;
  box.querySelector('#stReset').onclick = function () {
    if (confirm('هل تريد تصفير كل الإحصائيات؟')) {
      S = { stats: { answered: 0, correct: 0 }, byTopic: {}, cards: {} };
      save(); renderStats(); renderTopicList();
    }
  };
}

/* ================= الامتحان الوزاري ================= */
var EX = window.EXAM_DATA || { parts: [] };
var EX_KEY = 'grammar6_exam_v1';
var exState = loadExam();

function loadExam() {
  try {
    var raw = localStorage.getItem(EX_KEY);
    if (raw) { var o = JSON.parse(raw); if (o && typeof o === 'object' && o.ans) return o; }
  } catch (e) {}
  return { started: false, part: 0, ans: {}, self: {}, graded: {}, finished: false, t0: 0 };
}
function saveExam() { try { localStorage.setItem(EX_KEY, JSON.stringify(exState)); } catch (e) {} }

function normAns(s) {
  return String(s == null ? '' : s).toLowerCase().replace(/[.,!?;:'"()]+/g, '')
    .replace(/\s+/g, ' ').trim();
}
function exAutoOk(it, part) {
  var a = exState.ans[it.id];
  if (a === undefined || a === null || a === '') return null;
  if (it.type === 'mcq') return a === it.ans;
  if (it.type === 'tf') return a === it.ans;
  if (it.type === 'fill') return normAns(a) === normAns(it.ans);
  if (it.type === 'spell' || it.type === 'find') {
    var n = normAns(a);
    return it.ans.some(function (x) { return normAns(x) === n; });
  }
  if (it.type === 'match') return a === part.keys[it.pair];
  return null;
}
function exPartMax(part) {
  var s = 0; part.items.forEach(function (it) { s += it.m; }); return s;
}
function exPartScore(part) {
  var s = 0;
  part.items.forEach(function (it) {
    if (it.type === 'open' || it.type === 'rewrite' || it.type === 'essay') {
      s += exState.self[it.id] || 0;
    } else if (exAutoOk(it, part)) s += it.m;
  });
  return s;
}
function exTotalScore() {
  var s = 0; EX.parts.forEach(function (p) { s += exPartScore(p); }); return s;
}
function exTotalMax() {
  var s = 0; EX.parts.forEach(function (p) { s += exPartMax(p); }); return s;
}

function renderExamSetup() {
  var box = document.getElementById('examSetup');
  var mins = Math.round((Date.now() - exState.t0) / 60000);
  var h = '<div class="card"><h2>📝 ' + esc(EX.title) + '</h2>' +
    '<p class="muted">' + esc(EX.round) + ' · ' + esc(EX.subject) + ' · المدة ' + EX.durationMin + ' دقيقة</p>' +
    '<div class="card"><table class="forms"><thead><tr><th>السؤال</th><th>المحتوى</th><th>الدرجة</th></tr></thead><tbody>' +
    '<tr><td>السؤال الأول</td><td>قراءة: قطعة غير مرئية + فقرات من الكتاب</td><td>20</td></tr>' +
    '<tr><td>السؤال الثاني</td><td>القواعد: إعادة الكتابة + اختيار من متعدد</td><td>30</td></tr>' +
    '<tr><td>السؤال الثالث</td><td>المفردات والإملاء: صندوق + مطابقة + إملاء</td><td>20</td></tr>' +
    '<tr><td>السؤال الرابع</td><td>الأدب: كبرياء وهوى + كما تشاء + البحث عن كلمة</td><td>15</td></tr>' +
    '<tr><td>السؤال الخامس</td><td>الكتابة: موضوع مقالي</td><td>15</td></tr>' +
    '</tbody></table></div>' +
    '<div class="muted" style="font-size:.85rem">📌 ' + esc(EX.note) + '</div>' +
    '<div class="btn-row">';
  if (exState.started && !exState.finished) {
    h += '<button class="btn" id="exResume">متابعة الامتحان (' + mins + ' دقيقة مضت)</button>';
  }
  if (exState.finished) {
    h += '<button class="btn" id="exShowRes">عرض النتيجة الأخيرة</button>';
  }
  h += '<button class="btn' + ((exState.started || exState.finished) ? ' ghost' : ' full') + '" id="exStart">' +
       ((exState.started && !exState.finished) ? 'امتحان جديد (يمحو التقدم)' : 'ابدأ الامتحان') + '</button></div></div>';

  var doneParts = 0;
  EX.parts.forEach(function (p) { if (exState.graded[p.id]) doneParts++; });
  if (exState.started) {
    h += '<div class="card"><div class="sec-title">تقدمك</div>' +
      '<div class="unit-row"><div class="top"><span>أسئلة مُصححة</span><span class="muted">' + doneParts + ' / ' + EX.parts.length + '</span></div>' +
      '<div class="bar"><i style="width:' + Math.round(doneParts * 100 / EX.parts.length) + '%"></i></div></div></div>';
  }
  h += '<div class="card center">' +
    '<div class="muted" style="font-size:12px">إعداد وتأليف — مدرس اللغة الإنجليزية</div>' +
    '<div style="font-weight:800;margin-top:3px">الأستاذ علي معز الشلاه · ' +
    '<a href="tel:07806611177" class="ltr" style="text-decoration:none;color:var(--teal)">07806611177</a></div></div>';
  box.innerHTML = h;
  var start = box.querySelector('#exStart');
  if (start) start.onclick = function () {
    if ((exState.started || exState.finished) && !confirm('هل تريد بدء امتحان جديد؟ سيُمحى تقدمك الحالي.')) return;
    exState = { started: true, part: 0, ans: {}, self: {}, graded: {}, finished: false, t0: Date.now() };
    saveExam();
    openExamSession();
  };
  var res = box.querySelector('#exResume');
  if (res) res.onclick = openExamSession;
  var showRes = box.querySelector('#exShowRes');
  if (showRes) showRes.onclick = renderExamResult;
}

function openExamSession() {
  document.getElementById('examSetup').hidden = true;
  document.getElementById('examResult').hidden = true;
  document.getElementById('examSession').hidden = false;
  renderExamPart();
}

function exItemHead(n, it) {
  return '<div class="ex-item-head"><span class="ex-num">' + n + '</span>' +
    (it.tag ? '<span class="tag t-teal">' + esc(it.tag) + '</span>' : '') +
    '<span class="marks-b">' + it.m + ' د</span></div>';
}

function renderExamPart() {
  if (exState.part >= EX.parts.length) { return renderExamResult(); }
  var part = EX.parts[exState.part];
  var box = document.getElementById('examSession');
  var mins = exState.t0 ? Math.round((Date.now() - exState.t0) / 60000) : 0;
  var h = '<div class="quiz-head"><span class="muted">' + esc(EX.title) + ' · ' + esc(EX.round) + '</span>' +
          '<span class="cnt">⏱ ' + mins + ' د</span></div>' +
          '<div class="progress"><i style="width:' + Math.round(exState.part * 100 / EX.parts.length) + '%"></i></div>' +
          '<div class="part-h"><div><h2>' + esc(part.label) + '</h2>' +
          '<div class="muted">' + esc(part.title) + '</div></div>' +
          '<div class="score-chip">' + (part.realMarks ? 'درجته في الورقة ' + part.realMarks : '') + '</div></div>';
  if (part.choice) h += '<div class="note amber">ℹ️ ' + esc(part.choice) + ' — هنا أجب عن الجميع للتدريب الكامل.</div>';

  if (part.id === 'q1a') {
    h += '<div class="passage-box"><div class="pb-title">' + esc(EX.passage.title) + '</div>' +
         '<div class="pb-text">' + esc(EX.passage.text).replace(/\n\n/g, '<br><br>') + '</div></div>';
  }
  if (part.box) {
    h += '<div class="note">🧺 كلمات الصندوق (استخدم كل كلمة مرة واحدة): <b class="ltr">' +
         part.box.map(esc).join(' · ') + '</b></div>';
  }

  part.items.forEach(function (it, i) {
    h += '<div class="ex-item" id="it-' + it.id + '">' + exItemHead(i + 1, it);
    var a = exState.ans[it.id];
    if (it.type === 'mcq') {
      h += '<div class="q-text">' + esc(it.q) + '</div><div class="opts">';
      it.opts.forEach(function (o, k) {
        h += '<button class="opt' + (a === k ? ' sel' : '') + '" data-k="' + k + '"><span class="mark">' + 'ABCD'[k] + '</span><span>' + esc(o) + '</span></button>';
      });
      h += '</div>';
    } else if (it.type === 'tf') {
      h += '<div class="q-text">' + esc(it.q) + '</div><div class="btn-row" style="justify-content:flex-start">';
      h += '<button class="opt tf-b' + (a === 'T' ? ' sel' : '') + '" data-v="T"><span class="mark">T</span><span>True — صحيح</span></button>';
      h += '<button class="opt tf-b' + (a === 'F' ? ' sel' : '') + '" data-v="F"><span class="mark">F</span><span>False — خطأ</span></button>';
      h += '</div>';
    } else if (it.type === 'fill' || it.type === 'spell' || it.type === 'find') {
      h += '<div class="q-text">' + esc(it.q) + '</div>' +
           '<input class="inp ltr" data-id="' + it.id + '" value="' + esc(a || '') + '" placeholder="اكتب إجابتك هنا…" autocomplete="off">';
    } else if (it.type === 'rewrite') {
      h += '<div class="q-text">' + esc(it.q) + '</div>' +
           '<div class="arrow-line ltr">' + esc(it.arrow) + '</div>' +
           '<textarea class="txta ltr" data-id="' + it.id + '" rows="2" placeholder="أعد الكتابة هنا…">' + esc(a || '') + '</textarea>';
    } else if (it.type === 'open') {
      h += '<div class="q-text">' + esc(it.q) + '</div>' +
           '<textarea class="txta ltr" data-id="' + it.id + '" rows="3" placeholder="اكتب إجابتك هنا…">' + esc(a || '') + '</textarea>';
    } else if (it.type === 'match') {
      /* يُرسم بعد الحلقة */
    } else if (it.type === 'essay') {
      h += '<div class="essay-topics">';
      it.topics.forEach(function (tp, k) {
        h += '<label class="essay-topic' + (a && a.topic === k ? ' sel' : '') + '">' +
          '<input type="radio" name="essayTopic" value="' + k + '"' + (a && a.topic === k ? ' checked' : '') + '>' +
          '<div><b>' + esc(tp.title) + '</b><div class="muted" style="font-size:.85rem">' + esc(tp.prompt) + '</div></div></label>';
      });
      h += '</div><textarea class="txta ltr" id="essayText" rows="7" placeholder="اكتب مقالك هنا (100–120 كلمة)…">' + esc(a && a.text || '') + '</textarea>';
    }
    h += '</div>';
  });

  if (part.words) {
    h += '<div class="ex-item"><div class="ex-item-head"><span class="ex-num">🧩</span><span class="marks-b">5 د</span></div>' +
      '<div class="match-table">';
    part.words.forEach(function (w, i) {
      var it = part.items[i];
      var a = exState.ans[it.id];
      h += '<div class="match-row"><div class="w ltr">' + esc(w) + '</div><select class="match-sel" data-id="' + it.id + '">' +
        '<option value="">— اختر التعريف —</option>';
      part.defs.forEach(function (d) {
        h += '<option value="' + d.k + '"' + (a === d.k ? ' selected' : '') + '>' + esc(d.k) + ') ' + esc(d.t) + '</option>';
      });
      h += '</select></div>';
    });
    h += '</div></div>';
  }

  h += '<div class="btn-row"><button class="btn ghost" id="exQuit">حفظ والخروج</button>';
  if (exState.graded[part.id]) {
    h += '<button class="btn" id="exNext">' + (exState.part + 1 >= EX.parts.length ? 'النتيجة النهائية 🏁' : 'السؤال التالي ←') + '</button>';
  } else {
    h += '<button class="btn" id="exGrade">تصحيح هذا السؤال ✅</button>';
  }
  h += '</div><div id="exGradeBox"></div>';
  box.innerHTML = h;

  /* الأحداث */
  box.querySelectorAll('.opt:not(.tf-b)').forEach(function (b) {
    b.onclick = function () {
      var item = findItem(b);
      exState.ans[item.id] = parseInt(b.dataset.k, 10);
      saveExam();
      var wrap = b.parentNode;
      wrap.querySelectorAll('.opt').forEach(function (x) { x.classList.remove('sel'); });
      b.classList.add('sel');
    };
  });
  box.querySelectorAll('.opt.tf-b').forEach(function (b) {
    b.onclick = function () {
      var item = findItem(b);
      exState.ans[item.id] = b.dataset.v;
      saveExam();
      var wrap = b.closest('.ex-item');
      wrap.querySelectorAll('.tf-b').forEach(function (x) { x.classList.remove('sel'); });
      b.classList.add('sel');
    };
  });
  box.querySelectorAll('.inp').forEach(function (inp) {
    inp.oninput = function () { exState.ans[inp.dataset.id] = inp.value; saveExam(); };
  });
  box.querySelectorAll('.txta').forEach(function (ta) {
    if (ta.id === 'essayText') {
      ta.oninput = function () {
        var cur = exState.ans.e1 || {};
        exState.ans.e1 = { topic: cur.topic, text: ta.value };
        saveExam();
      };
    } else {
      ta.oninput = function () { exState.ans[ta.dataset.id] = ta.value; saveExam(); };
    }
  });
  box.querySelectorAll('input[name=essayTopic]').forEach(function (r) {
    r.onchange = function () {
      var cur = exState.ans.e1 || {};
      exState.ans.e1 = { topic: parseInt(r.value, 10), text: cur.text || '' };
      saveExam();
      box.querySelectorAll('.essay-topic').forEach(function (x) { x.classList.remove('sel'); });
      r.closest('.essay-topic').classList.add('sel');
    };
  });
  box.querySelectorAll('.match-sel').forEach(function (s) {
    s.onchange = function () { exState.ans[s.dataset.id] = s.value; saveExam(); };
  });
  function findItem(b) {
    var card = b.closest('.ex-item');
    var id = card.id.slice(3);
    return part.items.filter(function (x) { return x.id === id; })[0];
  }

  box.querySelector('#exQuit').onclick = function () {
    exState.finished ? renderExamSetup() : null;
    document.getElementById('examSession').hidden = true;
    document.getElementById('examSetup').hidden = false;
    renderExamSetup();
  };
  var g = box.querySelector('#exGrade');
  if (g) g.onclick = function () { gradeExamPart(part); };
  var n = box.querySelector('#exNext');
  if (n) n.onclick = function () {
    exState.part++;
    saveExam();
    if (exState.part >= EX.parts.length) { exState.finished = true; saveExam(); renderExamResult(); }
    else renderExamPart();
  };

  if (exState.graded[part.id]) showPartGrade(part, true);
}

function gradeExamPart(part) {
  exState.graded[part.id] = true;
  saveExam();
  showPartGrade(part, false);
}

function showPartGrade(part, silent) {
  var box = document.getElementById('exGradeBox');
  if (!box) return;
  var score = exPartScore(part), max = exPartMax(part);
  var h = '<div class="card grade-card"><div class="grade-head"><h3>نتيجة ' + esc(part.label) + '</h3>' +
    '<div class="score-chip big">' + score + ' / ' + max + '</div></div>';
  part.items.forEach(function (it) {
    var self = it.type === 'open' || it.type === 'rewrite' || it.type === 'essay';
    var got = self ? (exState.self[it.id] || 0) : (exAutoOk(it, part) ? it.m : 0);
    var answered = self ? true : exState.ans[it.id] !== undefined && exState.ans[it.id] !== '';
    h += '<div class="g-item">';
    if (it.type === 'match') {
      h += '<div class="g-q ltr">' + esc(part.words[it.pair]) + '</div>' +
        '<div class="' + (answered ? (exAutoOk(it, part) ? 'ok' : 'no') : 'muted') + '">' +
        (answered ? (exAutoOk(it, part) ? '✅ ' : '❌ الصحيح: ') : '— لم تُجب · الصحيح: ') +
        '<b>' + esc(part.keys[it.pair]) + ') ' + esc(part.defs.filter(function (d) { return d.k === part.keys[it.pair]; })[0].t) + '</b></div>';
    } else if (self) {
      h += '<div class="g-q">' + esc(it.q || it.arrow) + '</div>';
      if (it.type !== 'essay') {
        h += '<div class="model"><div class="mh">الإجابة النموذجية</div><div class="ltr">' + esc(it.model) + '</div></div>';
        h += '<div class="self-row"><span class="muted">قيّم إجابتك مقارنةً بالنموذج:</span>' +
          '<div class="self-btns" data-id="' + it.id + '">' +
          '<button class="chip' + (exState.self[it.id] === it.m ? ' active' : '') + '" data-v="' + it.m + '">كاملة (' + it.m + ')</button>' +
          '<button class="chip' + (exState.self[it.id] === Math.floor(it.m / 2) ? ' active' : '') + '" data-v="' + Math.floor(it.m / 2) + '">جزئية (' + Math.floor(it.m / 2) + ')</button>' +
          '<button class="chip' + (exState.self[it.id] === 0 ? ' active' : '') + '" data-v="0">صفرية</button></div></div>';
      } else {
        var chosen = exState.ans[it.id] && exState.ans[it.id].topic !== undefined ? it.topics[exState.ans[it.id].topic] : null;
        if (chosen) {
          h += '<div class="model"><div class="mh">نموذج: ' + esc(chosen.title) + '</div><div class="ltr">' + esc(chosen.model).replace(/\n\n/g, '<br><br>') + '</div></div>';
          h += '<div class="muted" style="font-size:.85rem">معايير التصحيح: ' + it.criteria.map(esc).join(' · ') + '</div>';
        }
        h += '<div class="self-row"><span class="muted">قيّم مقالك بناءً على المعايير:</span>' +
          '<div class="self-btns" data-id="' + it.id + '">' +
          [15, 12, 9, 6, 3].map(function (v, i) {
            var lbl = ['ممتاز', 'جيد جدًا', 'جيد', 'مقبول', 'ضعيف'][i];
            return '<button class="chip' + (exState.self[it.id] === v ? ' active' : '') + '" data-v="' + v + '">' + v + ' · ' + lbl + '</button>';
          }).join('') + '</div></div>';
      }
    } else if (it.type === 'mcq') {
      h += '<div class="g-q ltr">' + esc(it.q) + '</div>' +
        '<div class="' + (answered ? (exAutoOk(it, part) ? 'ok' : 'no') : 'muted') + '">' +
        (answered ? (exAutoOk(it, part) ? '✅ إجابة صحيحة' : '❌ الصحيح: <b>' + esc(it.opts[it.ans]) + '</b>') : '— لم تُجب · الصحيح: <b>' + esc(it.opts[it.ans]) + '</b>') +
        '</div><div class="muted">' + esc(it.why) + '</div>';
    } else if (it.type === 'tf') {
      h += '<div class="g-q ltr">' + esc(it.q) + '</div>' +
        '<div class="' + (answered ? (exAutoOk(it, part) ? 'ok' : 'no') : 'muted') + '">' +
        (answered ? (exAutoOk(it, part) ? '✅ ' : '❌ الصحيح: <b>' + (it.ans === 'T' ? 'True' : 'False') + '</b>') : '— لم تُجب · الصحيح: <b>' + (it.ans === 'T' ? 'True' : 'False') + '</b>') +
        '</div><div class="muted">' + esc(it.why) + '</div>';
    } else {
      h += '<div class="g-q ltr">' + esc(it.q) + '</div>' +
        '<div class="' + (answered ? (exAutoOk(it, part) ? 'ok' : 'no') : 'muted') + '">' +
        (answered ? (exAutoOk(it, part) ? '✅ ' : '❌ الصحيح: <b>' + esc(it.ans[0] || it.ans) + '</b>') : '— لم تُجب · الصحيح: <b>' + esc(it.ans[0] || it.ans) + '</b>') + '</div>';
    }
    h += '</div>';
  });
  h += '<div class="btn-row"><button class="btn" id="exNext2">' +
    (exState.part + 1 >= EX.parts.length ? 'النتيجة النهائية 🏁' : 'السؤال التالي ←') + '</button></div></div>';
  box.innerHTML = h;

  box.querySelectorAll('.self-btns .chip').forEach(function (c) {
    c.onclick = function () {
      var id = c.parentNode.dataset.id;
      exState.self[id] = parseInt(c.dataset.v, 10);
      saveExam();
      var wrap = c.parentNode;
      wrap.querySelectorAll('.chip').forEach(function (x) { x.classList.remove('active'); });
      c.classList.add('active');
      var part2 = EX.parts[exState.part];
      var sc = document.querySelector('#exGradeBox .score-chip.big');
      if (sc) sc.textContent = exPartScore(part2) + ' / ' + exPartMax(part2);
    };
  });
  box.querySelector('#exNext2').onclick = function () {
    exState.part++;
    saveExam();
    if (exState.part >= EX.parts.length) { exState.finished = true; saveExam(); renderExamResult(); }
    else renderExamPart();
  };
  if (!silent) box.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderExamResult() {
  var box = document.getElementById('examResult');
  var total = exTotalScore(), maxT = exTotalMax();
  var pct = maxT ? Math.round(total * 100 / maxT) : 0;
  var mins = exState.t0 ? Math.round((Date.now() - exState.t0) / 60000) : 0;
  var h = '<div class="card center">' +
    '<div class="score-ring" style="--p:' + pct + '%"><div class="v">' + total + '<small>/ ' + maxT + ' درجة</small></div></div>' +
    '<h2>' + (pct >= 85 ? 'ممتاز! جاهز للوزارية 🎉' : pct >= 60 ? 'جيد جدًا، استمر 💪' : pct >= 40 ? 'تحتاج مراجعة 🔁' : 'ابدأ من القواعد والتدريب 💪') + '</h2>' +
    '<p class="muted">الامتحان الحقيقي 100 درجة (مع فقرات الاختيار) — هذا التدريب ' + maxT + ' درجة لأنه يشمل كل الفقرات · ⏱ ' + mins + ' دقيقة</p>' +
    '<div class="btn-row"><button class="btn" id="exAgain">امتحان جديد</button>' +
    '<button class="btn ghost" id="exBack">القائمة</button></div></div>';

  h += '<div class="card"><div class="sec-title">الدرجات حسب السؤال</div>';
  EX.parts.forEach(function (p) {
    var got = exPartScore(p), mx = exPartMax(p);
    var pp = mx ? Math.round(got * 100 / mx) : 0;
    h += '<div class="unit-row"><div class="top"><span>' + esc(p.label) + ' — ' + esc(p.title) + '</span>' +
      '<span class="muted">' + got + '/' + mx + '</span></div>' +
      '<div class="bar"><i style="width:' + pp + '%"></i></div></div>';
  });
  h += '</div>';

  /* مراجعة الأخطاء */
  var rows = [];
  EX.parts.forEach(function (p) {
    p.items.forEach(function (it) {
      var self = it.type === 'open' || it.type === 'rewrite' || it.type === 'essay';
      if (self) {
        if ((exState.self[it.id] || 0) < it.m) {
          rows.push({ p: p, it: it, model: it.type === 'essay' ? null : it.model });
        }
      } else if (!exAutoOk(it, p)) {
        rows.push({ p: p, it: it, model: null });
      }
    });
  });
  if (rows.length) {
    h += '<div class="sec-title">راجع ما أخطأت فيه (' + rows.length + ')</div>';
    rows.forEach(function (r) {
      var it = r.it;
      h += '<div class="missed"><div class="q"><span class="tag t-teal">' + esc(r.p.label) + '</span> ';
      if (it.type === 'match') h += esc(r.p.words[it.pair]);
      else h += esc(it.q || it.arrow);
      h += '</div><div class="a">';
      if (it.type === 'match') h += 'الصحيح: <b>' + esc(r.p.keys[it.pair]) + ') ' + esc(r.p.defs.filter(function (d) { return d.k === r.p.keys[it.pair]; })[0].t) + '</b>';
      else if (it.type === 'mcq') h += 'الإجابة: <b>' + esc(it.opts[it.ans]) + '</b>';
      else if (it.type === 'tf') h += 'الإجابة: <b>' + (it.ans === 'T' ? 'True' : 'False') + '</b>';
      else if (it.type === 'fill') h += 'الإجابة: <b>' + esc(it.ans) + '</b>';
      else if (it.type === 'spell' || it.type === 'find') h += 'الإجابة: <b>' + esc(it.ans[0]) + '</b>';
      else if (it.type === 'rewrite') h += 'النموذج: <b class="ltr">' + esc(it.model) + '</b>';
      else if (it.type === 'open') h += 'النموذج: <b class="ltr">' + esc(it.model) + '</b>';
      else h += 'قارن مقالك بالنموذج في صفحة السؤال الخامس';
      h += '</div>';
      if (it.why) h += '<div class="a muted">' + esc(it.why) + '</div>';
      h += '</div>';
    });
  }
  box.innerHTML = h;
  box.hidden = false;
  document.getElementById('examSession').hidden = true;
  document.getElementById('examSetup').hidden = true;
  box.querySelector('#exAgain').onclick = function () {
    exState = { started: true, part: 0, ans: {}, self: {}, graded: {}, finished: false, t0: Date.now() };
    saveExam();
    openExamSession();
  };
  box.querySelector('#exBack').onclick = function () {
    box.hidden = true;
    document.getElementById('examSetup').hidden = false;
    renderExamSetup();
  };
}

/* ================= التشغيل ================= */
/* زر الرجوع في أندرويد: يغلق شاشة الموضوع أولًا */
window.appBack = function () {
  var sheet = document.getElementById('topicSheet');
  if (sheet && !sheet.hidden) { closeSheet(); return true; }
  var sb = document.getElementById('searchbar');
  if (sb && !sb.hidden) { sb.hidden = true; document.getElementById('searchInput').value = ''; renderTopicList(); return true; }
  return false;
};

renderUnitChips();
renderTopicList();
renderQuizSetup();
renderCardsSetup();
showView('ref');
})();
