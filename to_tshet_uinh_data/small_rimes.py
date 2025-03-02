from collections import Counter
from const import *


def normalize(c, entry_ids, is_character):
    if c not in variant_patch:
        return c
    res = variant_patch[c]
    if is_character:
        if '@' in res:
            if not any(i in entry_ids for i in res.split('@')[1:]):
                return c
        elif '*' in res or '#' in res:
            return c
    else:
        if '@' in res and '*' not in res:
            return c
        if '^' in res:
            return c
        if '#' in res:
            if not any(i in entry_ids for i in res.split('#')[1:]):
                return c
    return normalize(res[:1], entry_ids, is_character)


def extract_fanqie(explanation):
    fanqies = [i for i in explanation.split('.')
               if not i.startswith('又') and i.endswith('反')]
    if fanqies:
        if len(fanqies[0]) != 3:
            print(explanation, fanqies)
        else:
            return fanqies[0][:2]
    return ''


def simplify_pair(pair, remove_empty=True, keep_size=True):
    if remove_empty:
        pair = [i for i in pair if i]
    if pair[:1] == pair[1:]:
        pair = pair[:1]
    if keep_size:
        while len(pair) < 2:
            pair.append('')
    return pair


def process_line_pair(small_rime_id, line_pair, fanqie_dict, correspondence):
    line = [[*pair] for pair in zip(*line_pair)]
    entry_ids = line[5]
    entry_id = str(min([int(i) for i in entry_ids if i]))
    rime = simplify_pair(line[4])[0]
    description = description_patch.get(entry_id, simplify_pair(line[2])[0])
    characters = line[8]
    explanations = line[9]
    for i in range(2):
        for pair in explanation_patch.items():
            explanations[i] = explanations[i].replace(*pair)
    old_fanqies = [extract_fanqie(e) for e in explanations]
    fanqie_uppers = [fanqie[:1] for fanqie in old_fanqies]
    fanqie_lowers = [fanqie[1:] for fanqie in old_fanqies]
    phonetic = phonetic_patch.get(entry_id, '')
    if not any(old_fanqies) and not phonetic:
        print(entry_id, characters, explanations, 'no phonetic')

    if characters[0] == characters[1]:
        new_character = normalize(characters[0], entry_ids, True)
        if new_character != characters[0]:
            print(entry_id, characters[0], new_character)
    for i in range(2):
        characters[i] = normalize(characters[i], entry_ids, True)
        fanqie_uppers[i] = normalize(fanqie_uppers[i], entry_ids, False)
        fanqie_lowers[i] = normalize(fanqie_lowers[i], entry_ids, False)
    new_fanqies = [''.join(fanqie) for fanqie
                   in zip(fanqie_uppers, fanqie_lowers)]

    if entry_id in fanqie_upper_patch:
        assert fanqie_uppers[0] == fanqie_uppers[1]
        fanqie_uppers = [fanqie_upper_patch[entry_id] for _ in fanqie_uppers]
    if entry_id in fanqie_lower_patch:
        assert fanqie_lowers[0] == fanqie_lowers[1]
        fanqie_lowers = [fanqie_lower_patch[entry_id] for _ in fanqie_lowers]
    fanqie_upper_descriptions = [fanqie and fanqie_dict[fanqie if len(fanqie) == 1 else fanqie[-2]]
                                 for fanqie in fanqie_uppers]
    fanqie_lower_descriptions = [fanqie and fanqie_dict[fanqie if len(fanqie) == 1 else fanqie[-2]]
                                 for fanqie in fanqie_lowers]
    for i, (old_fanqie, new_fanqie) in enumerate(zip(old_fanqies, new_fanqies)):
        if old_fanqie:
            explanations[i] = explanations[i].replace(old_fanqie, new_fanqie)

    note = ''
    if not characters[0]:
        note = '藤田無此小韻'
    elif not characters[1]:
        note = '李永富無此小韻'
    else:
        assert characters[0] == characters[1]
    characters = simplify_pair(characters)[0]
    fanqie_uppers = simplify_pair(fanqie_uppers)
    fanqie_lowers = simplify_pair(fanqie_lowers)
    fanqie_upper_descriptions = simplify_pair(fanqie_upper_descriptions)
    fanqie_lower_descriptions = simplify_pair(fanqie_lower_descriptions)
    explanations = simplify_pair(explanations)
    return [
        small_rime_id, entry_id, rime, description,
        characters, fanqie_uppers[0], fanqie_lowers[0], fanqie_uppers[1], fanqie_lowers[1], phonetic,
        fanqie_upper_descriptions[0], fanqie_lower_descriptions[0], fanqie_upper_descriptions[1], fanqie_lower_descriptions[1],
        correspondence[small_rime_id], note, explanations[0], explanations[1],
    ]


def read_data():
    with open('fanqie_dict.csv', encoding='utf-8') as f:
        next(f)
        fanqie_dict = dict([line.strip().split(',') for line in f])
    with open('correspondence.csv', encoding='utf-8') as f:
        next(f)
        correspondence = dict([line.strip().split(',') for line in f])

    k_to_entry_id = {}
    small_rimess = [{}, {}]
    for filename, small_rimes in zip([
        '../切韻 藤田拓海復元.csv',
        '../切韻 李永富復元.csv',
    ], small_rimess):
        with open(filename, encoding='utf-8') as f:
            next(f)
            for line in f:
                line = line.strip().split(',')
                rime, entry_id, small_rime_id, onset = line[4:8]
                sub = ''
                if entry_id == '9667':
                    sub = 'a'
                if entry_id in ('9668', '9669'):
                    sub = 'b'
                k = (rime, small_rime_id, onset, sub)
                if k not in k_to_entry_id:
                    k_to_entry_id[k] = int(entry_id)
                if k not in small_rimes:
                    small_rimes[k] = line
    ks = sorted(k_to_entry_id, key=lambda k: k_to_entry_id[k])
    lines = []
    small_rime_num = 1
    for k in ks:
        line_pair = [small_rimes.get(k, [''] * 10)
                     for small_rimes in small_rimess]
        lines.append(process_line_pair(
            str(small_rime_num) + k[-1],
            line_pair, fanqie_dict, correspondence))
        if k[-1] != 'a':
            small_rime_num += 1
    return lines


lines = read_data()
with open('small_rimes.csv', 'w', encoding='utf-8') as f:
    for line in [[
        '小韻號', '藤田條目號', '韻目原貌', '音韻地位',
        '代表字', '反切上字', '反切下字', '反切上字-又', '反切下字-又', '直音',
        '反切上字地位', '反切下字地位', '反切上字地位-又', '反切下字地位-又',
        '對應廣韻小韻號', '兩家差異注釋', '代表字釋義', '代表字釋義-又（又 = 李永富資料之與前一列不同者）',
    ]] + lines:
        f.write(','.join(line) + '\n')
