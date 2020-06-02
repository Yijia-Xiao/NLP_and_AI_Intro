# Homework for NLP & TM
# Prof: Ji Wu. TA: Jian Song
# Author: Yijia Xiao
# Ref: letian @ www.letiantian.me

# import position segmentation
import jieba.posseg as pseg
import os
import utils

class WordSegmentation(object):
    def __init__(self, allow_speech_tags=utils.allow_speech_tags):
        allow_speech_tags = list(allow_speech_tags)
        self.default_speech_tag_filter = allow_speech_tags
        self.stopwords = set()
        with open('stopwords.txt', 'r') as f:
            for w in f.readlines():
                self.stopwords.add(w.strip())

    def segment(self, text, lower = True, use_stop_words = True, use_speech_tags_filter = False):
        """segment text, and return a list of segments and tags"""
        text = text
        jieba_res = pseg.cut(text)
        # for seg in jieba_res:
        #     print(seg)

        if use_speech_tags_filter:
            jieba_res = [w for w in jieba_res if w.flag in self.default_speech_tag_filter]
        else:
            jieba_res = [w for w in jieba_res]

        # remove unnecessary symbols
        # x means '非语素字'
        word_list = [w.word.strip() for w in jieba_res if w.flag != 'x']
        word_list = [word for word in word_list if len(word) > 0]

        if lower:
            word_list = [word.lower() for word in word_list]
        if use_stop_words:
            word_list = [word.strip() for word in word_list if word.strip() not in self.stopwords]
        return word_list

    def segment_sentences(self, sentences, lower=True, use_stop_words = True, use_speech_tags_filter=False):
        """sentence is a list of words, we convert them into seg + label"""
        res = list()
        for sentence in sentences:
            res.append(self.segment(text=sentence, lower=lower, use_stop_words=use_stop_words, use_speech_tags_filter=use_speech_tags_filter))
        return res


class SentenceSegmentation(object):
    def __init__(self, delimiters=utils.sentence_delimiters):
        self.delimiters = set(delimiters)

    def segment(self, text):
        # TODO
        # check data type
        res = [text]
        for sep in self.delimiters:
            text, res = res, []
            for seq in text:
                res += seq.split(sep)
        res = [s.strip() for s in res if len(s.strip()) > 0]
        return res

class Segmentation(object):
    def __init__(self, stop_words_file=None, allow_speech_tags=utils.allow_speech_tags, delimiters=utils.sentence_delimiters):
        self.ws = WordSegmentation(allow_speech_tags=allow_speech_tags)
        self.ss = SentenceSegmentation(delimiters=delimiters)

    def segment(self, text, lower=False):
        sentences = self.ss.segment(text)
        words_no_filter = self.ws.segment_sentences(sentences=sentences, lower=lower, use_stop_words=False, use_speech_tags_filter=False)
        words_no_stop_words = self.ws.segment_sentences(sentences=sentences, lower=lower, use_stop_words=True, use_speech_tags_filter=False)
        words_all_filters = self.ws.segment_sentences(sentences=sentences, lower=lower, use_stop_words=True, use_speech_tags_filter=True)

        return utils.AttrDict(sentences=sentences, words_no_filter=words_no_filter, words_no_stop_words=words_no_stop_words, words_all_filters=words_all_filters)
