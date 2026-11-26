# -*- coding: utf-8 -*-
"""البحث عن مواضع شرح قواعد محددة في كتاب الطالب وكتاب النشاط."""
import io, os, re, sys
import pymupdf as fitz
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

BOOKS = {
    'student': os.path.join(ROOT, 'كتاب_الطالب_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf'),
    'activity': os.path.join(ROOT, 'كتاب_النشاط_للصف_السادس_الإعدادي_8_وحدات_مع_الأدب.pdf'),
}

SEARCH = {
    'reported': ['Reported speech', 'reported speech', 'say ', 'told me', 'backshift'],
    'wish': ['wish', 'if only', 'I wish'],
    'causative': ['have something done', 'get something done', 'make +', 'causative'],
    'linking': ['Linking', 'linking word', 'however', 'therefore', 'moreover'],
    'comparative': ['Comparative', 'comparative', 'superlative', 'Superlative'],
    'quantifier': ['much', 'many', 'few', 'little'],
    'adjectives': ['-ing', '-ed', 'adjective', 'adverb'],
    'passive': ['Passive', 'passive', 'was made', 'by +'],
    'relative': ['relative clause', 'Relative clause', 'defining'],
    'zero_cond': ['zero conditional', 'Zero conditional'],
    'review': ['Review', 'revision'],
}

for name, path in BOOKS.items():
    doc = fitz.open(path)
    print('\n########', name, 'pages:', doc.page_count)
    for key, terms in SEARCH.items():
        hits = []
        for i, page in enumerate(doc):
            t = page.get_text()
            score = sum(t.count(term) for term in terms)
            if score >= 2:
                hits.append((i + 1, score))
        if hits:
            print(' ', key, '->', ', '.join('%d(%d)' % h for h in hits[:14]))
