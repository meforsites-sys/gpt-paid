# -*- coding: utf-8 -*-
"""
يبني بيانات «انكليزي السادس الاعدادي» 1.0 (web_english):
- الشرح + التمارين القابلة للحل + البطاقات من web4 (ملزمة 2027 مع إجاباتها).
- الاختبارات التفاعلية (183 سؤال MCQ مع شرح) من web2 (كانت في النسخة 1 الأصلية).
- يضبط هوية التطبيق: الاسم والإعداد.
"""
import io, os, sys, json, collections, hashlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
WEB4 = os.path.join(ROOT, 'app', 'web4', 'data', 'content.json')
WEB2 = os.path.join(ROOT, 'app', 'web2', 'data', 'content.json')
EXAM = os.path.join(ROOT, 'app', 'web2', 'data', 'exam.js')
OUT_DIR = os.path.join(ROOT, 'app', 'web_english', 'data')
OUT_JSON = os.path.join(OUT_DIR, 'content.json')
OUT_JS = os.path.join(OUT_DIR, 'content.js')
OUT_EXAM = os.path.join(OUT_DIR, 'exam.js')

with io.open(WEB4, encoding='utf-8') as f:
    d = json.load(f)
with io.open(WEB2, encoding='utf-8') as f:
    d2 = json.load(f)

q_by_topic = {t['id']: t.get('quiz', []) for t in d2['topics']}


def pdf_quiz_for_topic(topic):
    """Build four-choice questions from the exercises extracted from the 2027 PDFs."""
    exercises = [e for e in topic.get('exercises', [])
                 if e.get('answer', '').strip() and e.get('text', '').strip()]
    answers = []
    for e in exercises:
        a = e['answer'].strip()
        if a not in answers:
            answers.append(a)
    out = []
    for idx, e in enumerate(exercises):
        correct = e['answer'].strip()
        pool = [a for a in answers if a != correct]
        seed = '%s|%s' % (e.get('id', idx), correct)
        pool.sort(key=lambda x: hashlib.sha1((seed + '|' + x).encode('utf-8')).hexdigest())
        opts = [correct] + pool[:3]
        opts.sort(key=lambda x: hashlib.sha1((seed + '|option|' + x).encode('utf-8')).hexdigest())
        out.append({
            'id': 'pdf-%s-%s' % (topic['id'], idx),
            'topic': topic['id'],
            'q': e['text'],
            'opts': opts,
            'ans': opts.index(correct),
            'whyAr': e.get('textAr', ''),
            'whyEn': e.get('instrEn', ''),
            'source': e.get('book', ''),
            'page': e.get('page', ''),
        })
    return out

assert len(d['topics']) == len(d2['topics']) == 26
assert [t['id'] for t in d['topics']] == [t['id'] for t in d2['topics']] == list(range(1, 27))

for t in d['topics']:
    quiz = pdf_quiz_for_topic(t)
    # Keep the already available unit-8 review questions when the PDF parser
    # finds no answer-bearing exercise for a review topic.
    if not quiz:
        quiz = q_by_topic[t['id']]
    assert quiz, 'topic %d has no quiz' % t['id']
    t['quiz'] = quiz
    t['quizSource'] = '2027 PDF exercises' if pdf_quiz_for_topic(t) else 'unit review'

# عدد الأسئلة لكل وحدة
unit_quiz = collections.Counter()
for t in d['topics']:
    unit_quiz[t['unit']] += len(t['quiz'])
for u in d['meta']['units']:
    u['quizCount'] = unit_quiz.get(u['id'], 0)

total_quiz = sum(len(t['quiz']) for t in d['topics'])
print('quiz questions merged:', total_quiz)

d['meta']['title'] = 'انكليزي السادس الاعدادي'
d['meta']['subtitle'] = 'كتاب النشاط + ملزمة 2027 · الوحدات 1–8 · إعداد أ. علي معز الشلاه'
d['meta']['source'] = 'كتاب النشاط للصف السادس الإعدادي + ملزمة 2027 (كتاب الطالب) — مع الحلول'
d['meta']['stats']['quiz'] = total_quiz
d['meta']['stats']['exam'] = 'الدور الأول 2027'

os.makedirs(OUT_DIR, exist_ok=True)
with io.open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
js = 'window.APP_DATA = ' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';\n'
with io.open(OUT_JS, 'w', encoding='utf-8') as f:
    f.write(js)

with io.open(EXAM, encoding='utf-8') as f:
    exam_src = f.read()
with io.open(OUT_EXAM, 'w', encoding='utf-8') as f:
    f.write(exam_src)

print('written:', OUT_JSON, '(%.0f KB)' % (os.path.getsize(OUT_JSON) / 1024))
print('written:', OUT_JS, '(%.0f KB)' % (os.path.getsize(OUT_JS) / 1024))
print('written:', OUT_EXAM)
