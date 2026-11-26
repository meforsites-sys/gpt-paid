# -*- coding: utf-8 -*-
"""
يبني بيانات النسخة الثانية من التطبيق:
- شرح المواضيع من الملزمة (rules_book.py)
- بنك الأسئلة مع الشرح العربي والإنجليزي المنفصلين (quiz_bank.py)
- تمارين كتاب النشاط (exercises.json)
"""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'app', 'content'))
from rules_book import RULES      # noqa: E402
from quiz_bank import QUIZ        # noqa: E402

EXJ = os.path.join(ROOT, 'app', 'web', 'data', 'exercises.json')
OUT = os.path.join(ROOT, 'app', 'web2', 'data', 'content.json')

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
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text


def main():
    exdata = json.load(io.open(EXJ, encoding='utf-8'))
    book_by_topic = {t['id']: t for t in exdata['topics']}

    topics = []
    n_q = n_c = n_e = 0

    for src in RULES:
        tid = int(src['id'])
        bt = book_by_topic.get(tid, {'exercises': [], 'unit': 1})
        unit = 8 if tid == 26 else int(bt.get('unit') or 1)

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
                'trans': md_bold(e.get('translation_ar', '')),
                'script': md_bold(e.get('script_en', '')),
                'scriptRaw': e.get('script_en', ''),
                'items': [md_bold(x) for x in e.get('items', [])],
                'summary': md_bold(e.get('summary_ar', '')),
                'kind': e.get('kind', 'task'),
            })
        n_e += len(exercises)

        quiz = []
        for qi, item in enumerate(QUIZ.get(tid, [])):
            q, opts, ans, why_ar, why_en = item
            quiz.append({
                'id': 't%dq%d' % (tid, qi),
                'topic': tid,
                'unit': unit,
                'q': q,
                'opts': list(opts),
                'ans': ans,
                'whyAr': why_ar,
                'whyEn': why_en,
            })
        n_q += len(quiz)

        cards = []
        # بطاقات من الصيغ
        for fi, f in enumerate(src.get('forms', [])):
            cards.append({
                'id': 't%df%d' % (tid, fi),
                'topic': tid, 'unit': unit, 'kind': 'form',
                'frontEn': f['en'],
                'frontAr': f['ar'],
                'backEn': f['exEn'],
                'backAr': f['exAr'],
                'whyEn': '',
            })
        # بطاقات من الأسئلة
        for qi, q in enumerate(quiz):
            cards.append({
                'id': 't%dqc%d' % (tid, qi),
                'topic': tid, 'unit': unit, 'kind': 'quiz',
                'frontEn': q['q'].replace('______', '………'),
                'frontAr': '',
                'backEn': q['opts'][q['ans']],
                'backAr': q['whyAr'],
                'whyEn': q['whyEn'],
            })
        n_c += len(cards)

        topics.append({
            'id': tid,
            'unit': unit,
            'unitAr': UNIT_AR[unit],
            'ar': src['ar'],
            'en': src['en'],
            'src': src.get('src', ''),
            'rule': [{'ar': md_bold(b['ar']), 'en': b['en']} for b in src.get('rule', [])],
            'forms': [{'ar': f['ar'], 'en': f['en'], 'exEn': f['exEn'], 'exAr': f['exAr']}
                      for f in src.get('forms', [])],
            'tips': [{'ar': t['ar'], 'en': t['en']} for t in src.get('tips', [])],
            'quiz': quiz,
            'cards': cards,
            'exercises': exercises,
        })

    units = []
    for u in range(1, 9):
        ts = [t for t in topics if t['unit'] == u]
        units.append({
            'id': u, 'ar': UNIT_AR[u], 'title': UNIT_TITLE[u],
            'topics': [t['id'] for t in ts],
            'quizCount': sum(len(t['quiz']) for t in ts),
            'exCount': sum(len(t['exercises']) for t in ts),
        })

    data = {
        'meta': {
            'title': 'ملزمة القواعد',
            'subtitle': 'الصف السادس الإعدادي — شرح من كتاب الطالب والكتاب النشاط',
            'source': 'كتاب الطالب والكتاب النشاط للصف السادس الإعدادي (المنهج الحديث)',
            'units': units,
            'stats': {'topics': len(topics), 'quiz': n_q, 'cards': n_c, 'exercises': n_e},
        },
        'topics': topics,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    js = 'window.APP_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    io.open(os.path.join(ROOT, 'app', 'web2', 'data', 'content.js'), 'w', encoding='utf-8').write(js)

    print('topics: %d | quiz: %d | cards: %d | book exercises: %d' % (len(topics), n_q, n_c, n_e))
    for u in units:
        print('  %-14s topics=%d quiz=%d ex=%d' % (u['ar'], len(u['topics']), u['quizCount'], u['exCount']))
    print('app.json KB:', int(os.path.getsize(OUT) / 1024))


if __name__ == '__main__':
    main()
