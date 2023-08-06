import argparse
from collections import defaultdict as dd
import re
import sys
import unicodedata

from progress.bar import IncrementalBar


def configure():
    """Interpret command line arguments, open all corpus files given, and
    return a list of tri-tuples as:

    corpora = [(corpus file name, [lines], [tokenized lines]), (n, l, tl)]
    """
    parser = argparse.ArgumentParser(description='A tool that highlights'
                                     'inconsistencies in word segmentation.')
    parser.add_argument('corp', nargs='+',
                        help='one or more files of segmented text')
    parser.add_argument('-d', '--digits',
                        action='store_true',
                        help='exclude digits from the search')
    args = parser.parse_args()
    global digits
    digits = False
    if args.digits:
        digits = True
        print('\n')
        print('Ignoring digits in multi-character inconsistency checking.')
        print('\n')
    else:
        print('\n')
    global longest_fname
    global file_lengths
    filenames = args.corp
    longest_fname = sorted(filenames)[0]
    file_lengths = []
    corpora = []
    for fname in filenames:
        with open(fname) as f:
            lines = f.readlines()
            print(f'Opening {fname}...', flush=True)  # noqa
            file_lengths.append(len(lines))
        print('    cleaning lines...', flush=True)
        clean_lines = [l.rstrip() for l in lines]
        print('    splitting lines...', flush=True)
        token_lines = [l.split(' ') for l in clean_lines]
        corpora.append((fname, lines, token_lines))
        print('\n')
    return corpora


def count_multi(corpus_tokenized):
    """Return dict of multicharacter tokens as keys and as values:
    a two-tuple of a compiled regular expression and an empty list to be filled
    with line numbers and match objects.

    multi_words = {mword: (spaced regex, [])}
    """
    print('Searching corpora for multi-character tokens and compiling regular',
          'expressions for fuzzy matches of each.', flush=True)
    global digits
    bar = IncrementalBar('Processing line by line', max=len(corpus_tokenized),
                         suffix='%(percent).1f%% |')
    multi_words = dd(tuple)
    for line in corpus_tokenized:
        bar.next()
        for token in line:
            if len(token) >= 2 and token not in multi_words:
                if digits:
                    if re.match(r'\d{2,}', token):
                        continue
                exp = re.compile(r'(.{,20})(\b\w*' + r'\s?'.join(re.escape(token)) + r'\w*\b)(.{,20})')  # noqa
                multi_words[token] = (exp, [])
    bar.finish()
    print('\n')
    return multi_words


def find_variation(multi_words, corpora):
    """For every multicharacter word found by count_multi(), use the compiled
    regexes to search for segmentation variation in all corpora given and
    add tri-tuples of (corpus name, line number, match object) to the
    multi_words dictionary.

    multi_words = {mword: (spaced regex, [(c, ln, mo), (c, ln, mo)])}
    """
    print('Searching corpora for matches and inconsistencies.',
          len(multi_words),
          'multi-character tokens to process.', flush=True)
    bar = IncrementalBar('Searching token by token', max=len(multi_words),
                         suffix='%(percent).1f%% | Time remaining %(eta_td)s')
    for token, info in multi_words.items():
        bar.next()
        spaced_regex = info[0]
        all_matches = []
        for corp_name, lines, token_lines in corpora:
            for i, line in enumerate(lines):
                spaced_matches = list(spaced_regex.finditer(line))
                for match in spaced_matches:
                    match_tup = (corp_name, i + 1, match)
                    all_matches.append(match_tup)
        variation = False
        for tup in all_matches:
            if token != tup[2].group(2):  # if there is variation
                multi_words[token] = (spaced_regex, all_matches)
                break
    bar.finish()
    return multi_words


def normalize_width(str):
    length_ls = [unicodedata.east_asian_width(char) for char in str]
    count = 0
    for i in length_ls:
        if i == 'Na' or i == 'A':
            count += 1
        elif i == "W":
            count += 2
    return count


def display(result_dict):
    """Parse and print the results of the search for segmentation variation for
    all multi-character tokens in all corpora. Present the results in a human-
    readable format for review of each instance of inconsistency.
    """
    global longest_fname
    global file_lengths
    print('\n')
    print('If variation found, printing variation matches for each',
          'multi-character token, noting the corpus and line number for each',
          'instance.')
    print('\n')
    for token, info in result_dict.items():
        list_of_match_tups = info[1]
        if list_of_match_tups:
            print('TOKEN: ' + '__' + token + '__')
            for tup in sorted(list_of_match_tups, key=lambda x: x[2].group(2)):
                corp = tup[0]
                line = tup[1]
                name_buff = len(longest_fname) + 2
                line_buff = len(str(sorted(file_lengths)[-1])) + 2
                norm_intro = normalize_width(tup[2].group(1))
                print(f'{corp:<{name_buff}}', f'{line:>{line_buff}}', end='')
                print(' ' * (40 - norm_intro), end='')
                print(tup[2].group(1) + '__' + tup[2].group(2) + '__' + tup[2].group(3))  # noqa
            print('\n\n')


if __name__ == '__main__':
    corpora = configure()
    multi_words = count_multi([line for c in corpora for line in c[2]])
    result_dict = find_variation(multi_words, corpora)
    display(result_dict)
