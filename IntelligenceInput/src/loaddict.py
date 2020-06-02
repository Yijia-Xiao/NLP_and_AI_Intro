import json
from config import config


def load_dict(triple=False):
    pinyin_dict = dict()
    freq_dict = dict()
    trans_dict = dict()
    emit_dict = dict()
    with open(config['DATA_PATH'] + 'pinyin.txt', 'r') as f:
        for line in f.readlines():
            pinyin_dict[line.split()[0]] = line.split()[1:]

    with open(config['DATA_PATH'] + 'freq_dic.json', 'r') as f:
        freq_dict = json.load(f)

    with open(config['DATA_PATH'] + 'trans_dic.json', 'r') as f:
        trans_dict = json.load(f)

    with open(config['DATA_PATH'] + 'emit_dic.json', 'r') as f:
        emit_dict = json.load(f)

    if not triple:
        return [pinyin_dict, freq_dict, trans_dict, emit_dict]
    else:
        with open(config['DATA_PATH'] + 'bi_freq_dic.json', 'r') as f:
            bi_freq_dict = json.load(f)
        with open(config['DATA_PATH'] + 'trip_dic.json', 'r') as f:
            trip_dict = json.load(f)
        return [pinyin_dict, freq_dict, trans_dict, emit_dict, bi_freq_dict, trip_dict]


'''
def load_dict():
    pinyin_dict = dict()
    freq_dict = dict()
    trans_dict = dict()
    emit_dict = dict()
    with open('../data/pinyin.txt', 'r') as f:
        for line in f.readlines():
            pinyin_dict[line.split()[0]] = line.split()[1:]

    with open('../data/freq_dic.json', 'r') as f:
        freq_dict = json.load(f)

    with open('../data/trans_dic.json', 'r') as f:
        trans_dict = json.load(f)

    with open('../data/emit_dic.json', 'r') as f:
        emit_dict = json.load(f)

    with open('../data/bi_freq_dic.json', 'r') as f:
        bi_freq_dict = json.load(f)

    with open('../data/trip_dic.json', 'r') as f:
        trip_dict = json.load(f)

    return [pinyin_dict, freq_dict, trans_dict, emit_dict, bi_freq_dict, trip_dict]

'''
