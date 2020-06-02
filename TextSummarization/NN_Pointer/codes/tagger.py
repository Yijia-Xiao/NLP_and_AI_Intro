import jieba
import os
import time
import sys

ARTICL_PAHT = 'data/text.txt'
SUMMARY_PATH = 'data/summary.txt'
TRAIN_PAHT = './data/train.txt'
VAL_PAHT = './data/val.txt'


def read_text_file(text_file):
    lines = []
    with open(text_file, "r", encoding='utf-8') as f:
        for line in f:
            line = ' '.join(jieba.cut(line))
            lines.append(line.strip())
    return lines


def mergeText(articlText, summaryText):
    trainList = []
    valList = []
    linum = 0
    for seq1, seq2 in zip(articlText, summaryText):
        linum = linum + 1
        if linum < 600000:

            trainList.append(seq1)
            trainList.append(seq2)
        else:

            valList.append(seq1)
            valList.append(seq2)
    return trainList, valList


def data_writer(finishList, path):
    with open(path, 'w', encoding='utf-8') as writer:
        for item in finishList:
            writer.write(item + '\n')


if __name__ == '__main__':
    articls = read_text_file(ARTICL_PAHT)
    summays = read_text_file(SUMMARY_PATH)
    trainlist, vallist = mergeText(articls, summays)
    data_writer(trainlist, TRAIN_PAHT)
    data_writer(vallist, VAL_PAHT)
