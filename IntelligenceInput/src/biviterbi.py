import json
import math
import sys
from config import config
from loaddict import load_dict


pinyin_dic, freq_dict, trans_dict, emit_dict = load_dict(triple=False)


def get_value_one_wrap(Dict, key, default_val=1e-40):
    if key not in Dict:
        return default_val
    else:
        return Dict[key]


def get_value_two_wrap(Dict, firstkey, secndkey, default_val=1e-150):
    # this function can process both trans and emit probability
    # trans_dict map each char to a dict, the dict map
    if firstkey not in Dict:
        return default_val
    else:
        return get_value_one_wrap(Dict[firstkey], secndkey)


def biviterbi(List, default_val1=1e-40, default_val2=1e-150):
    if len(List) == 0:
        print('Input pinyin string is empty')
        return None

    # comment: 
    # viteb: [layer_index] (dict){character: [score, path_list]}
    # maps layer_index to a dict
    # the dict maps chars in its layer to a (score, path) pair

    viteb = [{}]

    # process the first layer of char nodes
    prelist = curlist = pinyin_dic[List[0]]
    for node in curlist:
        path = [node]
        freq_score = (get_value_one_wrap(freq_dict, node, default_val1))
        emit_score = math.log(get_value_one_wrap(node, List[0], default_val1))
        score = math.log(max(freq_score, config['FREQ_DEFAULT'])) + \
            math.log(max(emit_score, config['EMIT_DEFAULT']))
        viteb[0][node] = (path, score)

    # process the remaining layers
    for layer_index in range(1, len(List)):
        # add a dict: the dict maps chars in its layer to a (score, path) pair
        viteb.append({})
        prelist = curlist
        curlist = pinyin_dic[List[layer_index]]

        for curnode in curlist:
            bestnode = '\0'
            bestscore = -1e100
            for prenode in prelist:
                trans_score = math.log(get_value_two_wrap(
                    trans_dict, prenode, curnode, default_val2))
                emit_score = math.log(get_value_two_wrap(
                    emit_dict, prenode, List[layer_index], default_val2))
                new_score = viteb[layer_index -
                                  1][prenode][1] + trans_score + emit_score

                if new_score > bestscore:
                    bestscore = new_score
                    bestnode = prenode
            new_path = viteb[layer_index - 1][bestnode][0].copy()
            new_path.append(curnode)
            viteb[layer_index][curnode] = (new_path, bestscore)
    return viteb


def bisearch(V):
    l = len(V)-1
    cnt = 0
    for key in V[l]:
        if cnt == 0:
            idx = key
            cnt += 1
        if V[l][key][1] > V[l][idx][1]:
            idx = key
    # print(V[l][idx])
    ans = V[l][idx][0]
    string = "".join(ans)
    return string


# search params
'''inp = list()
with open('../data/generate/in1000.txt', 'r') as f:
    inp = f.readlines()

for E_int in range(-100, 0, 5):
    for F_int in range(-100, 0, 5):
        E = E_int / 10
        F = F_int / 10
        config['EMIT_DEFAULT'] = (10) ** E
        config['FREQ_DEFAULT'] = (10) ** F
        with open('../data/generate/' + 'E=-%3dF=-%3d.txt' % (abs(E_int), abs(F_int)), 'w') as f:
            for s in inp:
                s = s.replace('\n', '')
                s = s.replace("lv","lu")
                s = s.replace("qv","qu")
                s = s.replace("xv","xu")
                s = s.replace("jv","ju")
                s = s.strip()
                s = s.lower()
                s = s.split()
                f.write(bisearch(biviterbi(s)) + '\n')'''
