import json
import math
import sys
from config import config
from loaddict import load_dict


TOP_K = 5


pinyin_dic, freq_dict, trans_dict, emit_dict, bi_freq_dict, trip_dict = load_dict(
    triple=True)


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


def score_triple(Dict, bichars, thirdchar):
    if bichars not in Dict:
        return get_value_two_wrap(trans_dict, bichars[1], thirdchar) * 1e-25
    else:
        if thirdchar == 'bifreq':
            return bi_freq_dict[bichars]
        if thirdchar not in Dict[bichars]:
            return (0.1) * (get_value_two_wrap(trans_dict, bichars[1], thirdchar))
        else:
            return get_value_two_wrap(Dict, bichars, thirdchar)


def triviterbi(List):
    # because we need to use List[0] and List[1] in the following, make sure
    # length >= 2
    if len(List) < 2:
        print('single pinyin input')
        return None
    V = list()
    for _ in range(len(List)):
        V.append(dict())

    prelist = pinyin_dic[List[0]]
    curlist = pinyin_dic[List[1]]
    for curchar in curlist:
        for prechar in prelist:
            V[1][prechar + curchar] = list()
            # the 0 layer is left empty
            # V[][] is used for storing path and its score
            # multiply the score of triple(means the frequency of bi-chars)
            # with the transition probability between first and second char
            score = math.log(score_triple(trip_dict, prechar + curchar, 'bifreq')) + \
                math.log(get_value_two_wrap(trans_dict, prechar, curchar))
            path = [prechar, curchar]
            # V[1][prechar + curchar] = list()
            V[1][prechar + curchar].append((path, score))

    for layer in range(2, len(List)):
        # first layer in the consecutive 3 layers
        fstlayer = prelist
        prelist = curlist
        curlist = pinyin_dic[List[layer]]

        for curnode in curlist:
            topK = list()
            for sndnode in prelist:
                V[layer][sndnode + curnode] = list()
                waitinglist = list()
                for fstnode in fstlayer:
                    # loop over the candidate nodes
                    try:
                        for i in range(0, len(V[layer - 1][fstnode + sndnode])):
                            score = V[layer - 1][fstnode + sndnode][i][1] + \
                                math.log(score_triple(trip_dict, fstnode + sndnode, curnode)) + \
                                1.5 * \
                                math.log(get_value_two_wrap(
                                    emit_dict, curnode, List[layer]))
                            waitinglist.append(
                                (V[layer-1][fstnode + sndnode][i][0], fstnode+sndnode, score))
                    except Exception as e:
                        print(e)
                # high scores first
                topK = sorted(
                    waitinglist, key=lambda elem: elem[2], reverse=True)
                for i in range(0, min(len(topK), TOP_K)):
                    # append path + its_score
                    newpath = topK[i][0].copy()
                    newpath.append(curnode)
                    V[layer][sndnode + curnode].append((newpath, topK[i][2]))

    return V


def trisearch(V, List):
    if len(List) < 2:
        return [('Too short pinyin', 0)]

    possibles = list()
    for key in V[-1]:
        for item in V[-1][key]:
            possibles.append(item)
    sorted_path_score = sorted(
        possibles, key=lambda item: item[1], reverse=True)
    ResK = list()
    for i in range(TOP_K):
        charline = ''.join(sorted_path_score[i][0])
        ResK.append((charline, sorted_path_score[i][1]))
    return ResK


'''
print('Loaded, please input...')

line = 'wo ai zu guo'
line = line.replace("\n", "")
line = line.replace("qv", "qu")
line = line.replace("xv", "xu")
line = line.replace("jv", "ju")
line = line.lower()
pyl = line.split()
chinese = trisearch(triviterbi(pyl), pyl)
print(chinese)


print('please input pinyin line\n')
s = ''
while s != 'exit':
    s = input()
    if s == 'exit':
        sys.exit(0)
    try:
        s = s.replace('\n', '')
        s = s.strip()
        s = s.lower()
        s = s.split()
        print(trisearch(triviterbi(s), s))
    except:
        print('again')

sys.exit(0)
'''
