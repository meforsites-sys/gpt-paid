# -*- coding: utf-8 -*-
"""يدمج تمارين الكتاب + المحتوى التعليمي في ملف بيانات واحد للتطبيق."""
import io, os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'app', 'content'))
from grammar_content import TOPICS  # noqa: E402
from booklet_content import BOOKLET  # noqa: E402 — شرح المواضيع من الملزمة

EXJ = os.path.join(ROOT, 'app', 'web', 'data', 'exercises.json')
OUT = os.path.join(ROOT, 'app', 'web', 'data', 'app.json')

UNIT_AR = {
    1: 'الوحدة الأولى', 2: 'الوحدة الثانية', 3: 'الوحدة الثالثة', 4: 'الوحدة الرابعة',
    5: 'الوحدة الخامسة', 6: 'الوحدة السادسة', 7: 'الوحدة السابعة', 8: 'الوحدة الثامنة',
}
UNIT_TITLE = {
    1: 'Past — الحكاية والماضي', 2: 'Plans — الخطط والالتزام', 3: 'Hypotheticals — الفرضيات',
    4: 'Review — مراجعة الوحدة', 5: 'Perfect tenses — الأزمنة التامة',
    6: 'Passive & deduction — المبني للمجهول والاستنتاج', 7: 'Future — المستقبل',
    8: 'Mixed review — مراجعة شاملة',
}


def md_bold(text):
    """يحوّل **نص** إلى <b>نص</b> لعرضه في الويب."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text


def nl2br(text):
    """يحوّل الأسطر الجديدة إلى <br> لعرضها في الويب (تنسيق السطور المتناوبة)."""
    return text.replace('\r\n', '\n').replace('\n', '<br>')


def main():
    exdata = json.load(io.open(EXJ, encoding='utf-8'))
    book_by_topic = {t['id']: t for t in exdata['topics']}

    topics = []
    total_q = 0
    total_c = 0
    total_e = 0

    for src in TOPICS:
        tid = int(src['id'])
        # شرح الملزمة يغلب على المحتوى التأليفي (الاسم والقاعدة والنصائح) للمواضيع T01–T17
        if tid in BOOKLET:
            ov = dict(BOOKLET[tid])
            ov.pop('id', None)
            src = {**src, **ov}
        bt = book_by_topic.get(tid, {'exercises': [], 'unit': src.get('unit', 1)})
        unit = int(src.get('unit') or bt.get('unit') or 1)
        if tid == 26:
            unit = 8

        exercises = []
        for e in bt.get('exercises', []):
            pos = e.get('position', {})
            exercises.append({
                'id': e['id'],
                'title': e.get('title', ''),
                'unit': pos.get('unit'),
                'page': pos.get('page'),
                'letter': pos.get('letter'),
                'posText': e.get('position_raw', ''),
                'script': md_bold(e.get('script_en', '')),
                'scriptRaw': e.get('script_en', ''),
                'trans': md_bold(e.get('translation_ar', '')),
                'items': [md_bold(x) for x in e.get('items', [])],
                'summary': md_bold(e.get('summary_ar', '')),
                'kind': e.get('kind', 'task'),
            })
        # ترتيب التمارين حسب الصفحة في الكتاب ثم حرف التمرين (12 ← 13 ← 23 ← 26)
        exercises.sort(key=lambda x: (
            x['page'] if x['page'] is not None else 9999,
            (x['letter'] or 'Z').upper(),
        ))
        total_e += len(exercises)

        quiz = []
        for qi, q in enumerate(src.get('quiz', [])):
            text, opts, ans, why = q[0], q[1], q[2], q[3]
            quiz.append({
                'id': 't%dq%d' % (tid, qi),
                'topic': tid,
                'unit': unit,
                'q': text,
                'opts': list(opts),
                'ans': ans,
                'why': why,
            })
        total_q += len(quiz)

        cards = []
        for c in src.get('cards', []):
            cards.append({
                'id': 't%dc%d' % (tid, len(cards)),
                'topic': tid,
                'unit': unit,
                'frontEn': c[0], 'frontAr': c[1], 'backEn': c[2], 'backAr': c[3],
                'kind': 'term',
            })
        for qi, q in enumerate(quiz):
            front = q['q'].replace('______', '………').replace('___', '………')
            cards.append({
                'id': 't%dqc%d' % (tid, qi),
                'topic': tid,
                'unit': unit,
                'frontEn': front,
                'frontAr': '',
                'backEn': q['opts'][q['ans']],
                'backAr': q['why'],
                'kind': 'quiz',
            })
        total_c += len(cards)

        topics.append({
            'id': tid,
            'unit': unit,
            'unitAr': UNIT_AR[unit],
            'ar': src['ar'],
            'en': src['en'],
            'ruleAr': nl2br(md_bold(src['rule_ar'])),
            'ruleEn': src['rule_en'],
            'forms': [{'label': f[0], 'form': f[1], 'exEn': f[2], 'exAr': f[3]}
                      for f in src.get('forms', [])],
            'tips': src.get('tips', []),
            'quiz': quiz,
            'cards': cards,
            'exercises': exercises,
        })

    units = []
    for u in range(1, 9):
        ts = [t for t in topics if t['unit'] == u]
        units.append({
            'id': u,
            'ar': UNIT_AR[u],
            'title': UNIT_TITLE[u],
            'topics': [t['id'] for t in ts],
            'quizCount': sum(len(t['quiz']) for t in ts),
            'exCount': sum(len(t['exercises']) for t in ts),
        })

    data = {
        'meta': {
            'title': 'انكليزي السادس الاعدادي',
            'subtitle': 'الصف السادس الإعدادي — الوحدات 1–8',
            'source': 'كتاب النشاط للصف السادس الإعدادي (الطبعة الجديدة)',
            'units': units,
            'stats': {'topics': len(topics), 'quiz': total_q, 'cards': total_c, 'exercises': total_e},
        },
        'topics': topics,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))

    js = 'window.APP_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    io.open(os.path.join(ROOT, 'app', 'web', 'data', 'app.js'), 'w', encoding='utf-8').write(js)

    print('topics:', len(topics), '| quiz:', total_q, '| cards:', total_c, '| book exercises:', total_e)
    for u in units:
        print('  %-14s topics=%d quiz=%d ex=%d' % (u['ar'], len(u['topics']), u['quizCount'], u['exCount']))
    print('app.json KB:', int(os.path.getsize(OUT) / 1024))


if __name__ == '__main__':
    main()
