# -*- coding: utf-8 -*-
"""
يبني بيانات النسخة 3.0:
- الشرح والملاحظات من الملزمة (booklet_content.py) حصرًا.
- الأمثلة والبطاقات وفقرة التدريب من تمارين كتاب النشاط (exercises.json) حصرًا.
"""
import io, os, re, sys, json

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'app', 'content'))
from booklet_content import BOOKLET   # noqa: E402

EXJ = os.path.join(ROOT, 'app', 'web', 'data', 'exercises.json')
OUT = os.path.join(ROOT, 'app', 'web3', 'data', 'content.json')

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
LATIN = re.compile(r'[A-Za-z]')


def md(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def is_example_line(line):
    """هل السطر مثال إنجليزي (يعرض من اليسار)؟"""
    core = line.replace('`', '')
    if not core.strip():
        return False
    latin = len(LATIN.findall(core))
    arabic = len(re.findall(r'[\u0600-\u06FF]', core))
    if '///' in line:
        return True
    if arabic == 0 and latin > 0:
        return True
    # سطر فيه مثال إنجليزي بعد نص عربي مثل: "أمثلة: `...`"
    if arabic > 0 and latin > 25 and latin > arabic:
        return True
    return False


def split_rule(text):
    """يحوّل نص الملزمة إلى أسطر: عربية أو أمثلة إنجليزية."""
    out = []
    for raw in text.split('\n'):
        line = raw.strip()
        if not line:
            continue
        if '///' in line:
            for part in line.split('///'):
                part = part.strip().strip('`').strip()
                if part:
                    out.append({'en': part})
            continue
        if is_example_line(line):
            out.append({'en': md(line.strip('`'))})
        else:
            out.append({'ar': md(line)})
    return out


def main():
    exdata = json.load(io.open(EXJ, encoding='utf-8'))
    book_by_topic = {t['id']: t for t in exdata['topics']}
    unit_by_topic = {t['id']: t.get('unit', 1) for t in exdata['topics']}
    if not unit_by_topic:
        for u in exdata['units']:
            for t in u.get('topics', []):
                unit_by_topic[t['id']] = t.get('unit', u.get('unit', 1))

    topics = []
    n_ex = n_c = n_ex_items = 0

    for tid in sorted(BOOKLET.keys()):
        b = BOOKLET[tid]
        bt = book_by_topic.get(tid, {'exercises': []})
        unit = unit_by_topic.get(tid, 1 if tid != 26 else 8)
        if tid == 26:
            unit = 8

        exercises = []
        cards = []
        for e in bt.get('exercises', []):
            pos = e.get('position', {})
            ex_id = e['id']
            ex = {
                'id': ex_id,
                'topic': tid,
                'unit': unit,
                'title': e.get('title', ''),
                'page': pos.get('page'),
                'letter': pos.get('letter'),
                'posText': e.get('position_raw', ''),
                'script': md(e.get('script_en', '')),
                'trans': md(e.get('translation_ar', '')),
                'items': [md(x) for x in e.get('items', [])],
                'summary': md(e.get('summary_ar', '')),
            }
            exercises.append(ex)
            n_ex_items += len(ex['items'])
            # بطاقة من التمرين: الأمام نص التمرين، والخلف ترجمته وملخصه
            src = 'كتاب النشاط'
            if ex['page']:
                src += ' ص %d' % ex['page']
            if ex['letter']:
                src += ' · التمرين %s' % ex['letter']
            cards.append({
                'id': 'c' + ex_id,
                'topic': tid,
                'unit': unit,
                'kind': 'exercise',
                'frontEn': e.get('script_en', ''),
                'frontAr': '',
                'backEn': e.get('script_en', ''),
                'backAr': e.get('translation_ar', ''),
                'summary': e.get('summary_ar', ''),
                'src': src,
                'title': e.get('title', ''),
            })
        n_ex += len(exercises)
        n_c += len(cards)

        topics.append({
            'id': tid,
            'unit': unit,
            'unitAr': UNIT_AR[unit],
            'ar': b['ar'],
            'en': b['en'],
            'rule': split_rule(b.get('rule_ar', '')),
            'ruleEn': b.get('rule_en', ''),
            'tips': [md(t) for t in b.get('tips', [])],
            'exercises': exercises,
            'cards': cards,
        })

    units = []
    for u in range(1, 9):
        ts = [t for t in topics if t['unit'] == u]
        units.append({
            'id': u, 'ar': UNIT_AR[u], 'title': UNIT_TITLE[u],
            'topics': [t['id'] for t in ts],
            'exCount': sum(len(t['exercises']) for t in ts),
        })

    data = {
        'meta': {
            'title': 'ملزمة القواعد',
            'subtitle': 'الصف السادس الإعدادي — القواعد من الملزمة والتمارين من كتاب النشاط',
            'source': 'الملزمة + كتاب النشاط للصف السادس الإعدادي',
            'units': units,
            'stats': {'topics': len(topics), 'exercises': n_ex, 'cards': n_c, 'items': n_ex_items},
        },
        'topics': topics,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    js = 'window.APP_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    io.open(os.path.join(ROOT, 'app', 'web3', 'data', 'content.js'), 'w', encoding='utf-8').write(js)

    print('topics: %d | book exercises: %d | cards: %d | example lines: %d'
          % (len(topics), n_ex, n_c, n_ex_items))
    for u in units:
        print('  %-14s topics=%d exercises=%d' % (u['ar'], len(u['topics']), u['exCount']))
    print('content.json KB:', int(os.path.getsize(OUT) / 1024))


if __name__ == '__main__':
    main()
