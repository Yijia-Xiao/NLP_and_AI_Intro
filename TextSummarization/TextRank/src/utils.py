# Homework for NLP & TM
# Prof: Ji Wu. TA: Jian Song
# Author: Yijia Xiao
# Ref: letian @ www.letiantian.me

import os
import math
import numpy as np
import networkx as nx


sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']

class AttrDict(dict):
    '''using dot, instead of [] to get elements'''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def conbine(word_list, window = 2):
    """construct the edges in the text rank map"""
    if window < 2:
        window = 2

    # iterate all the possible window sizes
    for x in range(1, window):
        # the window's length is longer than words' number
        if x >= len(word_list):
            break
        word_list2 = word_list[x:]
        # each time, we return a pair of words
        # the distance between them is 'x'
        for r in zip(word_list, word_list2):
            yield r

def get_similarity(word_list1, word_list2):
    """used for calculating the similarity between 2 sentences"""
    # remove the duplicate ones
    words = list(set(word_list1 + word_list2))
    vec1 = [float(word_list1.count(word)) for word in words]
    vec2 = [float(word_list2.count(word)) for word in words]
    vec3 = [vec1[i] * vec2[i] for i in range(len(vec1))]
    vec4 = [1 for mul in vec3 if mul > 0.0]

    co_occur = sum(vec4)
    # the inner product is smaller than threshold
    if abs(co_occur) <= 1e-12:
        return 0.0

    # the Euclidean length of 2 vectors
    denominator = math.log(float(len(word_list1))) + math.log(float(len(word_list2)))

    if abs(denominator) < 1e-12:
        return 0.0

    return co_occur / denominator


def sort_words(vertex, edge, window, damping_coeffi=0.85):
    """sort words in descending order"""
    """vertex is 2 dim list, [ [word1, word2, ...](sentence1) , [](sentence2), ...]
    edge is also 2-dim, similar to vertex"""
    sorted_words = list()
    # map word to index and index to word
    word_index, index_word = dict(), dict()
    words_number = 0

    # indexing part: counting the words, and build 2 mapping dict
    for word_list in vertex:
        for word in word_list:
            if word not in word_index:
                word_index[word] = words_number
                index_word[words_number] = word
                words_number += 1

    # build the weight matrix for ranking
    graph = np.zeros((words_number, words_number))

    for word_list in edge:
        for w1, w2 in conbine(word_list, window):
            # iterate all the possible word pairs
            if w1 in word_index and w2 in word_index:
                index1 = word_index[w1]
                index2 = word_index[w2]
                graph[index1][index2] = 1.0
                graph[index2][index1] = 1.0

    nx_graph = nx.from_numpy_matrix(graph)
    # a dict, mapping words to scores
    scores = nx.pagerank(nx_graph, **{'alpha': damping_coeffi})
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    for index, score in sorted_scores:
        item = AttrDict(word=index_word[index], weight=score)
        sorted_words.append(item)

    return sorted_words


def sort_sentences(sentences, words, sim_func=get_similarity, damping_coeffi=0.85):
    """sentences is a list of sentences [s1, s2, ..., sn]"""
    """words is identical to sort_words' param"""
    sorted_sentences = list()
    sentence_num = len(words)
    graph = np.zeros((sentence_num, sentence_num))

    for i in range(sentence_num):
        for j in range(sentence_num):
            simi = sim_func(words[i], words[j])
            graph[i, j] = simi
            graph[j, i] = simi

    nx_graph = nx.from_numpy_matrix(graph)
    scores = nx.pagerank(nx_graph, **{'alpha': damping_coeffi})
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    for index, score in sorted_scores:
        item = AttrDict(index=index, sentence=sentences[index], weight=score)
        sorted_sentences.append(item)

    return sorted_sentences