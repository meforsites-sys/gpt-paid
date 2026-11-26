# -*- coding: utf-8 -*-
"""استخراج تمارين القواعد من ملف Markdown إلى JSON جاهز للتطبيق."""
import io, os, sys, re, json

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'outputs', 'تمارين_القواعد_مرتبة_حسب_الموضوع',
                   'تمارين_القواعد_مرتبة_حسب_الموضوع_الوحدات_1-8.md')
OUT = os.path.join(ROOT, 'app', 'web', 'data', 'exercises.json')

UNIT_WORDS = {'الأولى': 1, 'الثانية': 2, 'الثالثة': 3, 'الرابعة': 4, 'الخامسة': 5,
              'السادسة': 6, 'السابعة': 7, 'الثامنة': 8}
AR_DIGITS = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5',
             '٦': '6', '٧': '7', '٨': '8', '٩': '9'}


def ar2int(s):
    s = s.translate(str.maketrans(AR_DIGITS))
    m = re.search(r'\d+', s)
    return int(m.group()) if m else None


def clean(line):
    """يزيل ترويسة Markdown من سطر."""
    line = line.rstrip()
    line = re.sub(r'^>\s?', '', line)
    line = re.sub(r'^#+\s*', '', line)
    return line.strip()


def strip_md(s):
    s = re.sub(r'\*\*\*', '', s)
    s = re.sub(r'\*\*', '', s)
    s = s.strip()
    return s


def detect_kind(script, items):
    s = (script or '').lower()
    joined = ' '.join(items).lower()
    if any(k in s for k in ['اختر', 'choose the correct', 'صنّف', 'classify', 'صنّف']):
        if 'صنّف' in s or 'classify' in s:
            return 'classify'
        return 'mcq'
    if any(k in s for k in ['رتّب', 'رتب', 'arrange', 'ترتيب الكلمات', 'رتّب الكلمات']):
        return 'order'
    if any(k in s for k in ['أكمل', 'complete', 'املأ', 'املئي', 'fill']):
        return 'gap'
    if re.search(r'\(\s*[a-d]\s*\)', joined) or re.search(r'\*\*[A-D]\s*/', joined):
        return 'mcq'
    if '………' in joined or '……' in joined or '____' in joined:
        return 'gap'
    return 'task'


def parse_position(pos):
    out = {'raw': pos}
    m = re.search(r'الوحدة\s+([^\s—\-]+)', pos)
    if m:
        word = m.group(1).strip()
        out['unit'] = UNIT_WORDS.get(word, ar2int(word))
    m = re.search(r'ص\s*([0-9٠-٩]+)', pos)
    if m:
        out['page'] = ar2int(m.group(1))
    m = re.search(r'(?:التمرين|تمرين|الحرف)\s*([A-Za-zأ-ي])\b', pos)
    if m:
        out['letter'] = m.group(1)
    m = re.search(r'([\u4e00-\u9fff]+)\s*,?\s*ص', pos)
    if m and 'كتاب' in m.group(1):
        out['book'] = m.group(1)
    return out


def main():
    text = io.open(SRC, encoding='utf-8').read()
    lines = text.split('\n')

    units = []          # [{unit, title, topics:[...]}]
    cur_unit = None
    cur_topic = None
    cur_ex = None
    section = None
    ex_seq = 0

    def flush_ex():
        nonlocal cur_ex, ex_seq
        if cur_ex:
            cur_ex['id'] = 'ex%03d' % ex_seq
            ex_seq += 1
            cur_ex['position'] = parse_position(cur_ex.get('position', ''))
            cur_ex['kind'] = detect_kind(cur_ex.get('script_en', ''), cur_ex.get('items', []))
            cur_topic['exercises'].append(cur_ex)
            cur_ex = None

    def flush_topic():
        nonlocal cur_topic
        flush_ex()
        if cur_topic:
            cur_unit['topics'].append(cur_topic)
            cur_topic = None

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.strip()

        m = re.match(r'^#\s+الوحدة\s+(\S+)\s*—\s*Unit\s*(\d+)', line)
        if m:
            flush_topic()
            cur_unit = {'unit': int(m.group(2)),
                        'title': 'الوحدة %s — Unit %s' % (m.group(1), m.group(2)),
                        'topics': []}
            units.append(cur_unit)
            i += 1
            continue

        m = re.match(r'^#\s+مراجعة مختلطة', line)
        if m:
            flush_topic()
            cur_unit = {'unit': 8, 'title': 'مراجعة مختلطة — Mixed review', 'topics': []}
            units.append(cur_unit)
            i += 1
            continue

        m = re.match(r'^##\s+(\d+)\.\s+(.+)$', line)
        if m:
            flush_topic()
            cur_topic = {'id': int(m.group(1)), 'ar': m.group(2).strip(), 'en': '', 'exercises': []}
            if cur_unit is None:
                cur_unit = {'unit': 0, 'title': 'عام', 'topics': []}
                units.append(cur_unit)
            i += 1
            continue

        m = re.match(r'^###\s+(.+)$', line)
        if m:
            flush_ex()
            cur_ex = {'title': m.group(1).strip(), 'items': []}
            section = None
            i += 1
            continue

        if cur_ex is not None:
            m = re.match(r'^\*\*(.+?):\*\*\s*(.*)$', line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip()
                section = None
                if key == 'الموضوع':
                    cur_ex['topic_ar'] = val
                elif key == 'الموضع':
                    cur_ex['position_raw'] = val
                    cur_ex['position'] = val
                elif key.startswith('النص'):
                    cur_ex['script_en'] = strip_md(val)
                    section = 'script'
                elif key.startswith('الترجمة'):
                    cur_ex['translation_ar'] = strip_md(val)
                    section = 'translation'
                elif key.startswith('نص التمرين'):
                    section = 'items'
                elif key.startswith('الملخص'):
                    cur_ex['summary_ar'] = strip_md(val)
                    section = 'summary'
                i += 1
                continue

            if line.startswith('>'):
                content = clean(line)
                if section == 'script':
                    cur_ex['script_en'] = (cur_ex.get('script_en', '') + ' ' + strip_md(content)).strip()
                elif section == 'translation':
                    cur_ex['translation_ar'] = (cur_ex.get('translation_ar', '') + ' ' + content).strip()
                elif section == 'items':
                    if content:
                        cur_ex['items'].append(content)
                elif section == 'summary':
                    cur_ex['summary_ar'] = (cur_ex.get('summary_ar', '') + ' ' + content).strip()
                i += 1
                continue

        i += 1

    flush_topic()

    # توزيع المواضيع على الوحدات: نأخذ الوحدة من خريطة المواضيع في الملف
    map_tbl = {}
    for m in re.finditer(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*Unit\s*(\d+)\s*\|', text, re.M):
        map_tbl[int(m.group(1))] = int(m.group(3))
    for u in units:
        for t in u['topics']:
            t['unit'] = map_tbl.get(t['id'], u['unit'])
            t['unit_label'] = u['title']

    # إضافة الوحدات الفارغة (4 و 8) حتى يظهر كل شيء في التطبيق
    topics = []
    for u in units:
        for t in u['topics']:
            topics.append(t)

    data = {'units': units, 'topics': topics}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=1))

    print('units:', len(units), 'topics:', len(topics),
          'exercises:', sum(len(t['exercises']) for t in topics))
    for u in units:
        print(' Unit %s -> %d topics, %d ex' % (
            u['unit'], len(u['topics']), sum(len(t['exercises']) for t in u['topics'])))
    kinds = {}
    for t in topics:
        for e in t['exercises']:
            kinds[e['kind']] = kinds.get(e['kind'], 0) + 1
    print('kinds:', kinds)


if __name__ == '__main__':
    main()
