# Homework for NLP & TM
# Prof: Ji Wu. TA: Jian Song
# Author: Yijia Xiao
# Ref: letian @ www.letiantian.me

# import networkx as nx
import numpy as np
import utils
from Segmentation import Segmentation


class TextRank4Sentence(object):
    def __init__(self, stop_words_file = None, allow_speech_tags = utils.allow_speech_tags, delimiters = utils.sentence_delimiters):
        self.seg = Segmentation(stop_words_file=stop_words_file, allow_speech_tags=allow_speech_tags, delimiters=delimiters)
        # [s1, s2, ...]
        self.sentences = None
        # 2-dim list: [[w1, w2, ...], [w1, w2, ...]]
        self.words_no_filter = None
        self.words_no_stop_words = None
        self.words_all_filters = None

        self.key_sentences = None

    def analyze(self, text, lower = False,
                source = 'no_stop_words',
                sim_func = utils.get_similarity,
                damping_coeffi=0.85):
        self.key_sentences = list()
        result = self.seg.segment(text=text, lower=lower)

        self.sentences = result.sentences

        self.words_no_filter = result.words_no_filter
        self.words_no_stop_words = result.words_no_stop_words
        self.words_all_filters = result.words_all_filters
        options = ['no_filter', 'no_stop_words', 'all_filters']

        if source in options:
            source_ = result['words_' + source]
        else:
            source_ = result['words_no_stop_words']

        self.key_sentences = utils.sort_sentences(sentences=self.sentences, words=source_, sim_func=sim_func, damping_coeffi=damping_coeffi)


    def get_key_sentences(self, num = 5, sentence_min_len = 6):
        """get num sentences whose length is >= min_len"""
        result = list()
        cnt = 0
        for item in self.key_sentences:
            if cnt >= num:
                break
            if len(item['sentence']) >= sentence_min_len:
                result.append(item)
                cnt += 1
        return result
