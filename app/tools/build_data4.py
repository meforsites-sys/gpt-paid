# -*- coding: utf-8 -*-
"""
يبني بيانات النسخة 4.1:
- الشرح والملاحظات من الملزمة (booklet_content.py).
- التمارين والأمثلة والبطاقات من ملزمة 2027 مع إجاباتها.
- كل فراغ في الجملة يصبح حقل إدخال، مع إبقاء الفعل بين القوسين كتلميح.
"""
import io, os, re, sys, json, collections

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'app', 'content'))
from booklet_content import BOOKLET   # noqa: E402

TOPICS_JSON = os.path.join(ROOT, 'app', 'data', 'booklet_2027_topics.json')
EXJ = os.path.join(ROOT, 'app', 'web', 'data', 'exercises.json')
OUT = os.path.join(ROOT, 'app', 'web4', 'data', 'content.json')

BR = re.compile(r'\(([^()]{1,60})\)')
BLANK = re.compile(r'[…\.]{3,}')
INSTR_WORDS = ['form', 'correct', 'use', 'question', 'suggestion', 'advice', 'regret',
               'the pool', 'a friend', 'somebody', 'someone', 'apply', 'make sure']
LAT = re.compile(r'[A-Za-z]')
# parts من تعليمات نهاية البند مثل: ") Correct)" أو "( Correct the form of the verb )"
TAIL_INSTR = re.compile(r'[\(\)\s]*[Cc]orrect[\s\S]{0,40}$')

UNIT_AR = {1: 'الوحدة الأولى', 2: 'الوحدة الثانية', 3: 'الوحدة الثالثة', 4: 'الوحدة الرابعة',
           5: 'الوحدة الخامسة', 6: 'الوحدة السادسة', 7: 'الوحدة السابعة', 8: 'الوحدة الثامنة'}
UNIT_TITLE = {
    1: 'Past — الحكاية والماضي', 2: 'Plans — الخطط والالتزام', 3: 'Hypotheticals — الفرضيات',
    4: 'Review — مراجعة الوحدة', 5: 'Perfect tenses — الأزمنة التامة',
    6: 'Passive & deduction — المبني للمجهول والاستنتاج', 7: 'Future — المستقبل',
    8: 'Mixed review — مراجعة شاملة',
}


def esc_html(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def md(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def is_instruction(content):
    c = content.strip().lower()
    if len(c.split()) > 4:
        return True
    for w in INSTR_WORDS:
        if w in c:
            return True
    if c[:1].isupper():
        return True
    if '/' in c:            # قائمة خيارات مثل (camp / see) → تعليمات لا فراغ
        return True
    return False


def stem(word):
    """جذر تقريبي للفعل لمطابقة التلميح بالإجابة."""
    w = re.sub(r'[^a-z]', '', word.lower())
    for suf in ('ing', 'ed', 'es', 's'):
        if w.endswith(suf) and len(w) > len(suf) + 1:
            return w[:-len(suf)]
    return w


def clean_item_text(text):
    """ينظّف بندًا: ينقل تعليمة النهاية إلى الحقل، ويوازن الأقواس."""
    instr_tail = ''
    m = TAIL_INSTR.search(text)
    if m and m.start() > 12:
        instr_tail = m.group(0).strip(' ()')
        text = text[:m.start()].rstrip(' ()')
    # إزالة الأقواس الزائدة
    if text.count(')') > text.count('('):
        text = re.sub(r'\)+(?=\s*$)', '', text)
    if text.count('(') > text.count(')'):
        text = re.sub(r'\(\s*(?=$)', '', text)
    return text.strip(), instr_tail


def find_slots(text):
    """يعيد الفراغات: قوس فيه فعل، أو نقاط، مع دمج النقطة مع القوس المجاور."""
    brackets = []
    stop = False
    for m in BR.finditer(text):
        content = m.group(1)
        if is_instruction(content):
            stop = True
            continue
        if stop:
            continue
        brackets.append({'start': m.start(), 'end': m.end(), 'type': 'bracket',
                          'hint': content.strip(), 'raw': m.group(0)})
    # نهاية التعليمات: لا نبحث عن فراغات بعدها
    stop_at = len(text)
    for m in BR.finditer(text):
        if is_instruction(m.group(1)):
            stop_at = min(stop_at, m.start())
            break
    blanks = []
    for m in BLANK.finditer(text):
        if m.start() >= stop_at:
            continue
        if any(b['start'] < m.end() and m.start() < b['end'] for b in brackets):
            continue
        blanks.append({'start': m.start(), 'end': m.end(), 'type': 'blank', 'hint': '', 'raw': m.group(0)})

    slots = brackets + blanks
    slots.sort(key=lambda s: s['start'])
    # دمج: نقطة تسبق قوسًا قريبًا → نفس الفراغ (نحتفظ بالقوس لأنه يحمل التلميح)
    drop_ranges = []
    keep = []
    for i, s in enumerate(slots):
        if s['type'] == 'blank':
            nxt = None
            for j in range(i + 1, len(slots)):
                if slots[j]['start'] >= s['end']:
                    nxt = slots[j]
                    break
            if nxt is not None and nxt['type'] == 'bracket' and (nxt['start'] - s['end']) <= 3:
                drop_ranges.append((s['start'], s['end']))
                continue
        keep.append(s)
    return keep, drop_ranges


def remove_ranges(text, ranges):
    for (a, b) in sorted(ranges, reverse=True):
        text = text[:a] + text[b:]
    return text


def split_answer(ans):
    parts = [p.strip(' .،,') for p in re.split(r'\s*/\s*|\s+or\s+', ans) if p.strip(' .،,')]
    return parts


def split_rule(text):
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
        core = line.replace('`', '')
        latin = len(re.findall(r'[A-Za-z]', core))
        arabic = len(re.findall(r'[\u0600-\u06FF]', core))
        if arabic == 0 and latin > 0:
            out.append({'en': md(esc_html(line)).replace('`', '')})
        elif latin > 25 and latin > arabic:
            out.append({'en': md(esc_html(line)).replace('`', '')})
        else:
            out.append({'ar': md(esc_html(line))})
    return out


AR_TOKEN = re.compile(r'[\u0600-\u06FF]+')
FUNCTION_WORDS = ['في', 'من', 'إلى', 'على', 'مع', 'أن', 'أو', 'هذا', 'هذه', 'الذي',
                  'صيغة', 'ضع', 'اكتب', 'اختر', 'استخدم', 'أكمل', 'اجعل', 'كل', 'بعض',
                  'عندما', 'حيث', 'لأن', 'ثم', 'يعني', 'نستخدم', 'تُستعمل', 'استعمال',
                  'الماضي', 'المضارع', 'المستقبل', 'الفعل', 'الأفعال', 'الجملة', 'الجمل',
                  'الكلمات', 'الوحدة', 'التمرين']


def ar_quality(text):
    if not text:
        return False
    t = text.strip()
    if len(t) < 12 or '#' in t or '\ufffd' in t:
        return False
    tokens = AR_TOKEN.findall(t)
    if len(tokens) < 4:
        return False
    short = [w for w in tokens if len(w) == 1]
    if len(short) / float(len(tokens)) > 0.15:
        return False
    return sum(1 for w in FUNCTION_WORDS if w in t) >= 2


def assign_answers(slots, parts):
    """يربط إجابات الملزمة بالفراغات: بالتلميح أولًا ثم بالترتيب."""
    used = set()
    for s in slots:
        if s['type'] != 'bracket' or not s['hint']:
            continue
        h = stem(s['hint'].split()[0] if s['hint'].split() else '')
        if not h:
            continue
        best, best_score = None, 0
        for pi, p in enumerate(parts):
            if pi in used:
                continue
            words = [stem(w) for w in re.split(r'[\s]+', p) if w]
            score = 0
            if words and words[0] == h:
                score = 3
            elif h in words:
                score = 2
            elif any(w.startswith(h[:3]) and len(h) >= 3 for w in words):
                score = 1
            if score > best_score:
                best, best_score = pi, score
        if best is not None and best_score >= 1:
            s['answer'] = parts[best]
            used.add(best)
    rest = [p for i, p in enumerate(parts) if i not in used]
    hintless = [s for s in slots if 'answer' not in s]
    for i, s in enumerate(hintless):
        if i < len(rest):
            s['answer'] = rest[i]
    return slots


def main():
    items = json.load(io.open(TOPICS_JSON, encoding='utf-8'))
    exdata = json.load(io.open(EXJ, encoding='utf-8'))
    old_by_topic = {t['id']: t for t in exdata['topics']}
    unit_by_topic = {t['id']: t.get('unit', 1) for t in exdata['topics']}

    by_topic = collections.defaultdict(list)
    for it in items:
        by_topic[it['topic']].append(it)

    topics = []
    n_items = n_slots = n_check = 0
    for tid in sorted(BOOKLET.keys()):
        b = BOOKLET[tid]
        unit = 8 if tid == 26 else unit_by_topic.get(tid, 1)

        ex_list = []
        for k, it in enumerate(by_topic.get(tid, [])):
            raw = it['text'].strip()
            answer = it['answer'].strip()
            text, tail = clean_item_text(raw)
            slots, drop_ranges = find_slots(text)
            if drop_ranges:
                text = remove_ranges(text, drop_ranges)
            parts = split_answer(answer)
            assign_answers(slots, parts)

            instr = it.get('instr', '') or ''
            instr = re.sub(r'[=\u2500\u2550]{3,}', ' ', instr)
            instr = re.sub(r'\s{2,}', ' ', instr).strip(' -—')
            if tail:
                instr = (instr + ' — ' + tail).strip(' —')
            if not instr and tail:
                instr = tail
            ex = {
                'id': 'x%d-%03d' % (tid, k),
                'topic': tid,
                'page': it.get('page'),
                'book': it.get('book', ''),
                'n': it.get('n'),
                'instrEn': md(esc_html(instr)),
                'instrAr': md(esc_html(it.get('instrAr', ''))) if ar_quality(it.get('instrAr', '')) else '',
                'text': text,
                'textAr': it.get('textAr', '') if ar_quality(it.get('textAr', '')) else '',
                'answer': answer,
                'slots': slots,
                'interactive': len(slots) > 0,
            }
            ex_list.append(ex)
            n_items += 1
            n_slots += len(slots)
            n_check += sum(1 for s in slots if s.get('answer'))

        old = []
        for e in old_by_topic.get(tid, {}).get('exercises', []):
            pos = e.get('position', {})
            old.append({
                'id': e['id'], 'title': e.get('title', ''),
                'page': pos.get('page'), 'letter': pos.get('letter'),
                'trans': md(esc_html(e.get('translation_ar', ''))),
                'script': md(esc_html(e.get('script_en', ''))),
                'items': [md(esc_html(x)) for x in e.get('items', [])],
                'summary': md(esc_html(e.get('summary_ar', ''))),
            })

        cards = []
        for e in ex_list:
            cards.append({
                'id': 'k' + e['id'], 'topic': tid, 'kind': 'exercise',
                'frontEn': e['text'], 'backEn': e['answer'], 'backAr': e['textAr'],
                'instr': e['instrEn'],
                'src': 'ملزمة 2027 · ص %s' % (e['page'] if e['page'] else '—'),
            })

        topics.append({
            'id': tid, 'unit': unit, 'unitAr': UNIT_AR[unit],
            'ar': b['ar'], 'en': b['en'],
            'rule': split_rule(b.get('rule_ar', '')),
            'ruleEn': b.get('rule_en', ''),
            'tips': [md(esc_html(t)) for t in b.get('tips', [])],
            'exercises': ex_list, 'old': old, 'cards': cards,
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
            'subtitle': 'الصف السادس الإعدادي — ملزمة 2027 (كتاب النشاط) مع الحل',
            'source': 'ملزمة 2027: 2027 1+2+3+4 و 2027 5+6+7+8',
            'units': units,
            'stats': {'topics': len(topics), 'exercises': n_items, 'slots': n_slots,
                      'checkable': n_check, 'cards': sum(len(t['cards']) for t in topics)},
        },
        'topics': topics,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    js = 'window.APP_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    io.open(os.path.join(ROOT, 'app', 'web4', 'data', 'content.js'), 'w', encoding='utf-8').write(js)

    print('topics: %d | exercises: %d | slots: %d (قابلة للتحقق %d) | cards: %d'
          % (len(topics), n_items, n_slots, n_check, data['meta']['stats']['cards']))
    print('content.json KB:', int(os.path.getsize(OUT) / 1024))


if __name__ == '__main__':
    main()
