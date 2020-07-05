import re
import pickle
import os
import pandas as pd
import pdfplumber


def parse_row(row, verbose=False):
    assert isinstance(row, list)
    assert len(row) == 5
    if row[0] == '例例句句':  # 例句
        if verbose:
            print(f"例句{row[1]}")
        return True, row[1].replace('\n', '')
    elif re.search(r'[\u4e00-\u9fa5]+', row[0]):  # 含有中文，扔掉
        return None
    elif row[0] == '' or re.search(r'^Day ', row[0]):
        return None
    else:  # 单词
        meaning = row[2].replace('\u2028', '')
        meaning = [i.replace('\n', '') for i in re.split(r'\n(?=\()', meaning)]
        meaning = '\n'.join(meaning)
        # Remove duplicate words but different encoding (e.g 对⽴立)
        # https://jrgraphix.net/research/unicode_blocks.php
        meaning = re.sub(r'[\u2f00-\u2fdf]', '', meaning)  # Kangxi
        meaning = re.sub(r'[\u3400-\u4dbf]', '', meaning)  # CJK Extras
        meaning = re.sub(r'[\uf900-\ufaff]', '', meaning)  # CJK Extras
        if verbose:
            meaning_verbose = row[2].replace('\n', ' ')
            print(f"单词{row[0]} 音标{row[1]} 释义{meaning_verbose} 同义词{row[3]}")
        return False, (row[0], row[1], meaning, row[3])


def run(in_file):
    # Read PDF
    pdf = pdfplumber.open(in_file).pages

    # Extract Tables
    all_rows = list()
    for i in range(len(pdf)):
        print(f"Reading page {i}...")
        parsed = pdf[i].extract_tables()
        assert len(parsed) == 1
        all_rows.extend(parsed[0])

    # Parse into DataFrame
    last_word = None
    word_row = {'word': [], 'pron': [], 'mean': [], 'syn': [], 'note': []}
    example = {'word': [], 'ex': []}

    for row in all_rows:
        parsed = parse_row(row)
        if parsed is not None:
            is_example, data = parsed
            if not is_example:
                word, pron, mean, syn = data
                last_word = word
                word_row['word'].append(word)
                word_row['pron'].append(pron)
                word_row['mean'].append(mean)
                word_row['syn'].append(syn)
                word_row['note'].append('')
            else:
                assert last_word is not None
                example['word'].append(last_word)
                example['ex'].append(parsed[1])

    data_df = pd.DataFrame(word_row)
    ex_df = pd.DataFrame(example)
    data_df = data_df.merge(ex_df, on='word', how='left')

    # Save output data
    out_filename = os.path.splitext(in_file)[0] + '.fmknowledge'
    if os.path.exists(out_filename):
        choice = input(
            f"\"{out_filename}\" exists and may contain user\'s notes. Provide a different name | [Y]es to overwrite\n")
        if choice == 'Y' or choice == 'y':
            pickle.dump(data_df, open(out_filename, 'wb'))
        else:
            pickle.dump(data_df, open(choice, 'wb'))
    else:
        pickle.dump(data_df, open(out_filename, 'wb'))


if __name__ == '__main__':
    run("data/GRE1450.pdf")
