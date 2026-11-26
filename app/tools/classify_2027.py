# -*- coding: utf-8 -*-
"""يصنّف بنود تمارين ملزمة 2027 إلى المواضيع النحوية مع إجاباتها."""
import io, json, os, re, sys, collections

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'app', 'data', 'booklet_2027.json')
OUT = os.path.join(ROOT, 'app', 'data', 'booklet_2027_topics.json')

# كلمات مفتاحية لكل موضوع (من أسماء الملزمة)
TOPIC_KEYS = {
    1: ['past simple', 'past continuous', 'past form', 'yesterday', 'last night', 'ago',
        'was/were', 'while', 'when', 'used to', 'simple', 'continuous', 'correct the form of the verb'],
    2: ['adjective', 'adverb', '-ing', '-ed', 'boring', 'bored', 'interested', 'interesting',
        'excited', 'frightened', 'fully', 'carefully'],
    3: ['much', 'many', 'few', 'little', 'quantity', 'a lot of', 'plenty of', 'enough',
        'countable', 'uncountable'],
    4: ['prefix', 'suffix', 'opposite of the words', 'un-', 'dis-', 'im-', 'in-', 'de-',
        'word formation', 'add the prefix'],
    5: ['used to', "didn't use to", 'used to/didn'],
    6: ['comparative', 'superlative', 'than', 'as ... as', 'more ... than', 'bigger', 'taller',
        'used to be', 'not as', 'as good as', 'than they used', 'than it used'],
    7: ['linking', 'linking word', 'however', 'therefore', 'moreover', 'in addition',
         'firstly', 'whereas', 'on the other hand', 'as a result', 'for example'],
    8: ['must', 'have to', 'need to', "mustn't", "needn't", "don't have to", 'not necessary',
        'obligation', 'necessary'],
    9: ['could you', 'shall we', 'shall i', 'would you like', "let's", 'imperative', 'request',
        'suggestion', 'offer', 'advice', 'buy some magazines'],
    10: ['expectation', 'expect'],
    11: ['something done', 'causative', 'have it done', 'get it done', 'make + object', 'repair'],
    12: ['first conditional', 'if clause', 'if it is sunny', 'if you come'],
    13: ['second conditional', 'if i were', 'unreal', 'if i had enough'],
    14: ['reported speech', 'said she', 'said he', 'told me', 'ask if', 'ask whether'],
    15: ['wish', 'if only', 'regret'],
    16: ['third conditional', 'had passed', 'would have', 'had + ', 'could have'],
    17: ['conditional'],
    18: ['present perfect simple', 'ever', 'never', 'already', 'yet', 'for ', 'since ',
         'have/has +', 'has lived', 'have finished'],
    19: ['present perfect continuous', 'been +', 'have been'],
    20: ['past perfect', 'had done', 'by the time', 'had + past participle', 'had already',
         'had lost', 'had changed', 'before you had', 'the earlier action'],
    21: ['relative clause', 'relative pronoun', 'who/which/that', 'whose', 'where',
         'defining', 'non-defining', 'combine with a relative'],
    22: ['passive', 'for the passive', 'by +', 'was made', 'were made'],
    23: ['deduction', "can't have", 'must have', 'might have'],
    24: ['future', 'going to', 'will be', 'future continuous', 'future simple', 'present simple for future'],
    25: ['future in the past', 'would +', 'was going to'],
    26: ['review', 'mixed'],
}
# مواضيع الشرط تتداخل: أولوية للخاص
PRIORITY = [17, 16, 13, 12, 14, 15, 22, 23, 21, 19, 20, 18, 24, 25, 5, 6, 11, 9, 8, 3, 4, 2, 7, 10, 1, 26]

VERB_BRACKET = re.compile(r'\(([^()]{1,40})\)')
BLANK = re.compile(r'[…\.]{4,}|\.{5,}')


def looks_grammar(item):
    t = item['text']
    if not t.strip():
        return False
    has_v = bool(VERB_BRACKET.search(t))
    has_b = bool(BLANK.search(t))
    if not (has_v or has_b):
        return False
    if len(t.strip()) < 8:
        return False
    return bool(item['answer'].strip())


def score(item, topic):
    hay = (item['text'] + ' ' + item.get('instr', '') + ' ' + item['answer']).lower()
    s = 0
    for k in TOPIC_KEYS.get(topic, []):
        if k in hay:
            s += 2 if ' ' in k else 1
    return s


def main():
    blocks = json.load(io.open(SRC, encoding='utf-8'))
    #.attach instruction to items
    for b in blocks:
        for it in b['items']:
            it['instr'] = b['instructionEn']

    kept = []
    for b in blocks:
        for it in b['items']:
            if not looks_grammar(it):
                continue
            best, best_s = None, 0
            for t in PRIORITY:
                s = score(it, t)
                if s > best_s:
                    best, best_s = t, s
            if best and best_s >= 1:
                it['topic'] = best
                it['page'] = b.get('page', it.get('page'))
                it['book'] = b['book']
                it['instr'] = b['instructionEn']
                it['instrAr'] = b['instructionAr']
                kept.append(it)

    print('grammar items:', len(kept))
    cnt = collections.Counter(i['topic'] for i in kept)
    for t in sorted(cnt):
        print('  topic %-2d : %d' % (t, cnt[t]))

    json.dump(kept, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('written:', OUT)


if __name__ == '__main__':
    main()
