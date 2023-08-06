#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
sys.path.append(os.getcwd())
import string
import random

from collections import defaultdict, Counter
from shove import Shove
from constants import *

def load_abbr(abbr_file=ABBREVIATION_FILE):
    """
    Load the abbr2long from file
    """
    abbr2long = dict()
    with open(abbr_file) as f:
        lines = f.read().split('\n')
        for line in lines:
            m = re.match(r'(\w+)\t(.+)', line)
            if m:
                abbr2long[m.group(1)] = m.group(2)
    return abbr2long


def load_spelling(spell_file=SPELLING_FILE):
    """
    Load the term_freq from spell_file
    """
    with open(spell_file) as f:
        tokens = f.read().split(' ')
        term_freq = Counter(tokens)
    return term_freq

def gen_path(base, code):
    """
    Generate a path for give base path and code used in data generation
    """
    return os.path.join(base, code[:2], code[:3])

def tokenize(s):
    """
    A simple tokneizer
    """
    s = re.sub(r'(?a)(\w+)\'s', r'\1', s) # clean the 's from Crohn's disease
    #s = re.sub(r'(?a)\b', ' ', s) # split the borders of chinese and english chars

    split_pattern = r'[{} ]+'.format(STOPCHARS)
    tokens = [token for token in re.split(split_pattern, s) if not set(token) <= set(string.punctuation)]
    return tokens

def lemmalize(tokens):
    """
    A simple lemalizer
    """
    return [token.lower() for token in tokens]

def filterout(tokens):
    """
    Filter removes stopwords
    """
    return [token for token in tokens if token not in STOPWORDS]

def invert_index(source_dir, index_url=INDEX_URL):
    """
    Build the invert index from give source_dir
    Output a Shove object built on the store_path
    Input:
        source_dir: a directory on the filesystem
        index_url: the store_path for the Shove object
    Output:
        index: a Shove object
    """
    raw_index = defaultdict(list)
    for base, dir_list, fn_list in os.walk(source_dir):
        for fn in fn_list:
            fp = os.path.join(base, fn)
            code = fn
            with open(fp) as f:
                tokens = f.read().strip().split('\n')
                for token in tokens:
                    raw_index[token].append(code)
    index = Shove(store=index_url)
    index.update(raw_index)
    index.sync()
    return index

def get_hints(code_list, k=10, hint_folder=HINT_FOLDER, current_tokens=None):
    """
    Fetch first k hints for given code_list
    """

    def hint_score(v, size):
        """
        The formula for hint score
        """
        return 1.0 - abs(v / (size + 1) - 0.5)
    if len(code_list) <= 1:
        return [], []

    if current_tokens is None:
        current_tokens = []

    size = min(len(code_list), MAX_HINT_SMAPLING_SIZE)
    sample = random.sample(code_list, size)
    hint_list = []
    capital_dict = {}

    for code in sample:
        path = gen_path(hint_folder, code)
        fp = os.path.join(path, code)
        with open(fp) as f:
            hints = set(f.read().strip().split('\n'))
            hint_list.extend([h.lower() for h in hints])
            capital_dict.update({hint.lower(): hint for hint in hints})
    document_freq = Counter(hint_list)
    score = [(capital_dict[k], hint_score(v, size)) \
             for k, v in document_freq.items() if k not in current_tokens]
    if len(score) == 0:
        return [], []
    score.sort(key=lambda x: x[1], reverse=True)
    hints, scores = tuple(list(zip(*score[:k])))
    return hints, scores

def fetch(index, tokens):
    """
    Fetch the codes from given tokens
    """
    if len(tokens) == 0:
        return set()
    return set.intersection(*[set(index.get(token, [])) for token in tokens])

def get_snippets(code_list, base=SNIPPET_FOLDER):
    """
    Get the snippets
    """
    output = []
    for code in code_list:
        path = gen_path(base, code)
        fp = os.path.join(path, code)
        with open(fp) as f:
            output.append(f.read())
    return output

def abbr_expand(tokens):
    log = []
    output = []
    for token in tokens:
        if token in abbr2long:
            long = abbr2long[token]
            log.append((token, long))
            output.extend(tokenize(long))
        else:
            output.append(token)
    return output, log

def _ed1(token):
    insertion = {letter.join([token[:i], token[i:]]) for letter in string.ascii_lowercase for i in range(1, len(token))}
    deletion = {''.join([token[:i], token[i+1:]]) for i in range(1, len(token))}
    substitution = {letter.join([token[:i], token[i+1:]]) for letter in string.ascii_lowercase for i in range(1, len(token))}
    transposition = {''.join([token[:i], token[i+1:i+2],  token[i:i+1], token[i+2:]]) for i in range(1, len(token)-1)}
    return set.union(insertion, deletion, substitution, transposition)

def _ed2(token):
    return {e2 for e1 in _ed1(token) for e2 in _ed1(e1)}

def _correct(token):
    if token.lower() in term_freq:
        return token
    e1 = [t for t in _ed1(token) if t in term_freq]
    if len(e1) > 0:
        e1.sort(key=term_freq.get)
        return e1[0]
    e2 = [t for t in _ed2(token) if t in term_freq]
    if len(e2) > 0:
        e2.sort(key=term_freq.get)
        return e2[0]
    return token

def correct(tokens):
    log = []
    output = []
    for token in tokens:
        corrected = _correct(token)
        if corrected != token:
            log.append((token, corrected))
        output.append(corrected)
    return output, log

def result_sort_key(response_item):
    """
    The sort key function for the search results
    Input:
        response_item: the tuple of (code, snippet)
    output:
        sortable value, the smallest first
    """
    code, snippet = response_item
    return len(snippet.split('\n')[0])

def search(index, query, snippet_folder=SNIPPET_FOLDER):
    fallback_log = []
    code_list = []
    tokens = tokenize(query)
    tokens, abbr_log = abbr_expand(tokens)
    tokens, correct_log = correct(tokens)
    tokens = lemmalize(tokens)
    tokens = filterout(tokens)
    while len(tokens) > 0: # Fallback mechanism
        code_list = fetch(index, tokens)
        if len(code_list) > 0:
            break
        tokens.sort(key=lambda tk:len(index.get(tk, [])))
        remove = tokens.pop()
        fallback_log.append(remove)
    snippets = get_snippets(code_list, snippet_folder)
    hints, hint_scores = get_hints(code_list, current_tokens=tokens)
    response = list(zip(code_list, snippets))
    response.sort(key=result_sort_key)
    return response, tokens, hints, hint_scores, \
           abbr_log, correct_log, fallback_log

# Load abbreviation.txt
abbr2long = load_abbr(abbr_file=ABBREVIATION_FILE)

# Load spelling.txt
term_freq = load_spelling(spell_file=SPELLING_FILE)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="action")
    args = parser.parse_args()
    if args.action == 'buildindex':
        index = invert_index(TOKEN_FOLDER, INDEX_URL)
