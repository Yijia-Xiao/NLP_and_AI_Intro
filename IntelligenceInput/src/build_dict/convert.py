import re
import json
import sys
import numpy

corp = list()

def read(month, mode):
    with open('./2016-{:02d}.txt'.format(month), 'r', encoding=mode) as f:
        for line in f.readlines():
            dic = json.loads(line)
            text = (dic['html']) + (dic['title'])
            segments = re.sub('\W', ' ', text).split()
            for seg in segments:
                corp.append(seg)
            # print(segments)
            # break


for i in range(2, 13):
    if i == 3:
        continue
    if i == 12:
        continue
        with open('2016-12.txt') as f:
            print(f.readlines()[:2])
    read(i, 'gbk')

with open('all.txt', 'w+', encoding='utf-8') as f:
    for line in corp:
        f.write(line + '\n')
