import jieba
import json
from tqdm import tqdm
from operator import itemgetter
import heapq
# summary = list()
# text = list()


# 先归一化，再求和、平均
def tf_func():
    tot = dict()
    with open('./data/text.txt', 'r') as f:
        for l in tqdm(f.readlines()):
            doc = dict()
            for seg in l.split():
                if seg in doc:
                    doc[seg] += 1
                else:
                    doc[seg] = 1
            terms = 0
            for v in doc.values():
                terms += v
            for k in doc:
                if k in tot:
                    tot[k] += doc[k] / terms
                else:
                    tot[k] = doc[k] / terms
    return tot
# json.dump(tf_func(), open('term_freq.json', 'w'))

'''
def idf_func():
    # 250000...个set，用来指示出现过的词语
    doc_set = list()
    # idf 结果字典
    tot = dict()
    with open('./data/text.txt', 'r') as f:
        tot_doc_num = 0
        for l in tqdm(f.readlines()[:10000]):
            tot_doc_num += 1
            doc = set()
            for seg in l.split():
                doc.add(seg)
                if seg not in tot:
                    tot[seg] = 0
            doc_set.append(doc)
        for w in tot:
            for s in doc_set:
                if w in s:
                    tot[w] += 1
    return tot
'''
def idf_func():
    # 250000...个set，用来指示出现过的词语
    doc_set = list()
    # idf 结果字典
    tot = dict()
    with open('./data/text.txt', 'r') as f:
        tot_doc_num = 0
        for l in tqdm(f.readlines()):
            tot_doc_num += 1
            doc = set()
            for seg in l.split():
                doc.add(seg)
                if seg not in tot:
                    tot[seg] = 0
            doc_set.append(doc)
        for s in tqdm(doc_set):
            for w in s:
                tot[w] += 1
    return tot
# json.dump(idf_func(), open('raw_idf.json', 'w'))



tf = json.load(open('term_freq.json', 'r'))
idf = json.load(open('raw_idf.json', 'r'))
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

stopwords = set()
with open('./data/stopwords.txt', 'r') as f:
    for l in f.readlines():
        stopwords.add(l.strip())

import sys
import os

len_gamma = float(sys.argv[1])

def summarize(text):
    news = text.split()
    news = [s for s in news if s not in stopwords]
    # print(''.join(news))
    score = [tf[seg] / (idf[seg]) if not is_number(seg) else 1e10 for seg in news]
    i_val = heapq.nlargest((int(len(news) * len_gamma)), enumerate(score), key=itemgetter(1))
    idx = [i for (i, val) in sorted(i_val)]
    return  ''.join([news[i] for i in idx])


with open('./data/text.txt', 'r') as f:
    for l in tqdm(f.readlines()):
        # print(l)
        print(summarize(l))
