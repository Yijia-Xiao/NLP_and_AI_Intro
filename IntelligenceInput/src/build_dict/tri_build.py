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


def bi_freq():
    bi_freq_dic = dict()
    with open('../data/corpus.txt', 'r') as f:
        for line in tqdm(f.readlines()):
            for headpos in range(len(line) - 1):
                if (line[headpos] in chars) and (line[headpos + 1] in chars):
                    if (line[headpos] + line[headpos + 1]) in bi_freq_dic:
                        bi_freq_dic[line[headpos] + line[headpos + 1]] += 1
                    else:
                        bi_freq_dic[line[headpos] + line[headpos + 1]] = 1
    cnt_all_bi_chars = 0
    for freq in bi_freq_dic.values():
        cnt_all_bi_chars += freq
    for k in bi_freq_dic.keys():
        bi_freq_dic[k] /= cnt_all_bi_chars
    return bi_freq_dic


'''
bi_freq_dic = bi_freq()
with open('../data/bi_freq_dic.json', 'w') as f:
    json.dump(bi_freq_dic, f)
sys.exit(0)
'''


with open('../data/bi_freq_dic.json', 'r') as f:
    bi_freq_dic = json.load(f)


def triple_trans():
    trans = dict()

    # build 2-words set
    bichars_dic = set()
    for char2 in bi_freq_dic.keys():
        bichars_dic.add(char2)
        trans[char2] = dict()
        # trans[char2]['bifreq'] = bi_freq_dic[char2]

    with open('../data/corpus.txt', 'r') as f:
        for line in tqdm(f.readlines()):
            for index in range(len(line) - 2):
                two_chars = line[index] + line[index + 1]
                if (two_chars not in bichars_dic) or (line[index + 2] not in chars):
                    continue
                if line[index + 2] not in trans[two_chars]:
                    trans[two_chars][line[index + 2]] = 1
                else:
                    trans[two_chars][line[index + 2]] = 1

    for subdickey in trans.keys():
        tot = 0
        for freq in trans[subdickey].values():
            tot += freq
        if tot == 0:
            continue
        for k in trans[subdickey].keys():
            trans[subdickey][k] /= tot
    return trans


trip_dic = triple_trans()

with open('../data/trip_dic.json', 'w', encoding='utf-8') as f:
    json.dump(trip_dic, f)

# print(trans_dic['我']['爱'])
