import pypinyin
import sys
from tqdm import tqdm
import json


chars = set()
with open('../data/char.txt', 'r', encoding='utf8', errors='ignore') as f:
    for c in f.readlines()[0]:
        chars.add(c)
# print(chars[:5])
print(len(chars))

# sys.exit(0)


def build_freq():
    freq_dic = dict()
    for c in chars:
        freq_dic[c] = 0
    with open('../data/corpus.txt', 'r') as f:
        for line in tqdm(f.readlines()):
            for c in line:
                if c in chars:
                    freq_dic[c] += 1
    all_chars = 0
    for freq in freq_dic.values():
        all_chars += freq
    for k in freq_dic.keys():
        freq_dic[k] /= all_chars
    return freq_dic


'''
freq_dic = build_freq()
# all_chars = 0
# for freq in freq_dic.values():
#     all_chars += freq

# print(freq_dic['爱'])
# print(freq_dic['我'])

with open('../data/freq_dic.json', 'w') as f:
    json.dump(freq_dic, f)
'''


def build_trans():
    trans = dict()
    for c1 in chars:
        trans[c1] = dict()
    with open('../data/corpus.txt', 'r') as f:
        for line in tqdm(f.readlines()):
            for index in range(len(line) - 1):
                if (line[index] not in chars) or (line[index + 1] not in chars):
                    continue
                if line[index + 1] not in trans[line[index]]:
                    trans[line[index]][line[index + 1]] = 1
                else:
                    trans[line[index]][line[index + 1]] += 1
    for subdickey in trans.keys():
        tot = 0
        for freq in trans[subdickey].values():
            tot += freq
        if tot == 0:
            continue
        for k in trans[subdickey].keys():
            trans[subdickey][k] /= tot
    return trans


trans_dic = build_trans()

with open('../data/trans_dic.json', 'w') as f:
    json.dump(trans_dic, f)

print(trans_dic['我']['爱'])
