# -*- coding: utf-8 -*-
"""يستخرج تمارين ملزمة 2027 مع إجاباتها."""
import io, os, re, sys, json
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BOOKS = ['2027  1+2 +3+4-compressed (1).pdf', '2027 5+6+7+8-compressed.pdf']
OUT = os.path.join(ROOT, 'app', 'data', 'booklet_2027.json')

AR = re.compile(r'[\u0600-\u06FF]')
LAT = re.compile(r'[A-Za-z]')
NUM = re.compile(r'^\s*(\d{1,2})\s*[\.\)]')
DASH = re.compile(r'^[\-\u2013\u2014\s\.]*$')


def page_tokens(page):
    out = []
    d = page.get_text('dict')
    for b in d['blocks']:
        if b.get('type') != 0:
            continue
        for l in b['lines']:
            for s in l['spans']:
                t = s['text'].strip()
                if not t:
                    continue
                bold = bool(s['flags'] & 16) or ('Bold' in s['font'])
                out.append((t, bold))
    return out


def parse_page(tokens, page_no):
    blocks = []
    instr_en, instr_ar, ar_buf = [], [], []
    items = []
    cur = None

    def flush_item():
        nonlocal cur
        if cur and (cur['text'].strip() or cur['answer'].strip()):
            items.append(cur)
        cur = None

    def flush_block():
        nonlocal instr_en, instr_ar, items, ar_buf
        flush_item()
        if items:
            blocks.append({
                'instructionEn': ' '.join(instr_en).strip(),
                'instructionAr': ' '.join(instr_ar).strip(),
                'items': items,
                'page': page_no,
            })
        instr_en, instr_ar, items, ar_buf = [], [], [], []

    i, n = 0, len(tokens)
    while i < n:
        t, bold = tokens[i]

        if bold:
            m = NUM.match(t) if len(t) <= 5 else None
            if m:
                flush_item()
                cur = {'n': int(m.group(1)), 'text': '', 'textAr': '', 'answer': '', 'page': page_no}
                i += 1
                continue
            if cur is not None and not cur['answer'].strip():
                ans = [t]
                j = i + 1
                while j < n and tokens[j][1] and not (len(tokens[j][0]) <= 5 and NUM.match(tokens[j][0])):
                    ans.append(tokens[j][0])
                    j += 1
                cur['answer'] = ' '.join(ans).strip()
                i = j
                continue
            # تعليمات جديدة
            ar_for_instr = [x for x in ar_buf if AR.search(x)]
            flush_block()
            instr_en.append(t)
            if ar_for_instr:
                instr_ar = ar_for_instr
            ar_buf = []
            i += 1
            continue

        # نص عادي
        if cur is not None and not cur['answer'].strip():
            if DASH.match(t) and len(t) <= 4:
                i += 1
                continue
            if AR.search(t) and not LAT.search(t):
                cur['textAr'] = (cur['textAr'] + ' ' + t).strip()
            else:
                cur['text'] = (cur['text'] + ' ' + t).strip()
        else:
            ar_buf.append(t)
        i += 1

    flush_block()
    return blocks


def main():
    all_blocks = []
    for bname in BOOKS:
        path = os.path.join(ROOT, bname)
        if not os.path.exists(path):
            print('missing:', bname)
            continue
        doc = fitz.open(path)
        print('%s: %d pages' % (bname, doc.page_count))
        for i in range(doc.page_count):
            for bl in parse_page(page_tokens(doc[i]), i + 1):
                bl['book'] = bname
                all_blocks.append(bl)
        doc.close()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(all_blocks, ensure_ascii=False, indent=1))

    items = sum(len(b['items']) for b in all_blocks)
    with_ans = sum(1 for b in all_blocks for it in b['items'] if it['answer'].strip())
    print('blocks: %d | items: %d | with answer: %d' % (len(all_blocks), items, with_ans))
    print('written:', OUT)


if __name__ == '__main__':
    main()
