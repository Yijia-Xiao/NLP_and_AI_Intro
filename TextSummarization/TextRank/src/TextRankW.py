# Homework for NLP & TM
# Prof: Ji Wu. TA: Jian Song
# Author: Yijia Xiao
# Ref: letian @ www.letiantian.me


import networkx as nx
import numpy as np
import utils
from Segmentation import Segmentation

class TextRank4Keyword(object):
    def __init__(self, stop_words_file = None, allow_speech_tags = utils.allow_speech_tags, delimiters = utils.sentence_delimiters):
        self.seg = Segmentation(stop_words_file=stop_words_file, allow_speech_tags=allow_speech_tags, delimiters=delimiters)
        # [s1, s2, ...]
        self.sentences = None
        # 2-dim list: [[w1, w2, ...], [w1, w2, ...]]
        self.words_no_filter = None
        self.words_no_stop_words = None
        self.words_all_filters = None

        self.text = ''
        self.keywords = None
        self.sentences = None

    # vertex_mode is used to choose which set to choose, to construct the nodes in the text rank graph
    # edge_mode is similar
    def analyze(self, text, window=2, lower=False, vertex_mode='all_filters', edge_mode='no_stop_words', damping_coeffi=0.85):
        self.word_index = dict()
        self.index_word = dict()
        self.text = text
        self.keywords = list()
        self.graph = None

        res = self.seg.segment(text=text, lower=lower)
        self.sentences = res.sentences
        self.words_no_filter = res.words_no_filter
        self.words_no_stop_words = res.words_no_stop_words
        self.words_all_filters = res.words_all_filters

        options = ['no_filter', 'no_stop_words', 'all_filters']
        if vertex_mode in options:
            # vertex = res['words_' + vertex_mode]
            vertex = res['words_' + vertex_mode]
        else:
            vertex = res['words_all_filters']

        if edge_mode in options:
            edge = res['words_' + edge_mode]
        else:
            edge = res['words_no_stop_words']
        self.keywords = utils.sort_words(vertex, edge, window=window, damping_coeffi=damping_coeffi)

    def get_keywords(self, num=6, word_min_len = 1):
        # logic is alike the one of sentences
        res = list()
        cnt = 0
        for item in self.keywords:
            if cnt >= num:
                break
            if len(item.word) >= word_min_len:
                res.append(item)
                cnt += 1
        return res

    def get_keyphrases(self, keywords_num = 12, min_occur_num = 2):
        keywords_set = set([item.word for item in self.get_keywords(num=keywords_num, word_min_len=1)])
        keyphrases = set()
        # sentence is a list of words
        for sentence in self.words_no_filter:
            one = list()
            for word in sentence:
                if word in keywords_set:
                    one.append(word)
                else:
                    # we find a word not in keyword set, that mean it breaks the consecutive words string
                    if len(one) > 1:
                        keyphrases.add(''.join(one))
                    if len(one) == 0:
                        continue
                    else:
                        # clear the existing words (because they can no longer link with others)
                        one = []
            if len(one) > 1:
                keyphrases.add(''.join(one))
        return [phrase for phrase in keyphrases if self.text.count(phrase) >= min_occur_num]
