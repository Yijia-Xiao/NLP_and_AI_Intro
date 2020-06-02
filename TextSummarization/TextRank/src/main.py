# Homework for NLP & TM
# Prof: Ji Wu. TA: Jian Song
# Author: Yijia Xiao
# Ref: letian @ www.letiantian.me
# 新华社受权于18日全文播发修改后的《中华人民共和国立法法》，修改后的立法法分为“总则”“法律”“行政法规”“地方性法规、自治条例和单行条例、规章”“适用与备案审查”“附则”等6章，共计105条	

# 日前，深圳市交警局对事故进行通报：从目前证据看，事故系司机超速行驶且操作不当导致	一辆小轿车，一名女司机，竟造成9死24伤	目前24名伤员已有6名治愈出院，其余正接受治疗，预计事故赔偿费或超一千万元	

# 新形势下，希望全国政法机关主动适应新形势，为公正司法和提高执法司法公信力提供有力制度保障	1月18日，习近平总书记对政法工作作出重要指示：2014年，政法战线各项工作特别是改革工作取得新成效	


# from __future__ import print_function
# from TextRank4Keyword import TextRank4Keyword

# import sys
# try:
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
# except:
#     pass
 
# import codecs
from TextRankW import TextRank4Keyword
from TextRankS import TextRank4Sentence


''' 
tr4w = TextRank4Keyword()

tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

print( '关键词：' )
for item in tr4w.get_keywords(20, word_min_len=1):
    print(item.word, item.weight)
 
print()
print( '关键短语：' )
for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
    print(phrase)
''' 
tr4s = TextRank4Sentence()

'''
tr4s.analyze(text=text, lower=True, source = 'all_filters')
'''

# print()
# print( '摘要：' )
fw = open('topwords.txt', 'w')
fp = open('topphras.txt', 'w')
fs = open('topsents.txt', 'w')

with open('text.txt', 'r') as f:
    for l in f.readlines():
        l = l.strip()
        tr4w = TextRank4Keyword()
        tr4s = TextRank4Sentence()
        tr4w.analyze(text=l, lower=True, window=2)
        tr4s.analyze(text=l, lower=True, source = 'all_filters')
        for item in tr4w.get_keywords(20, word_min_len=1):
            fw.write(item.word + '\t')
        fw.write('\n')
        for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 1):
            fp.write(phrase + '\t')
        fp.write('\n')
        for item in tr4s.get_key_sentences(num=3):
            fs.write(item.sentence + '\t')
        fs.write('\n')
#    print(item.index, item.weight, item.sentence)  # index是语句在文本中位置，weight是权重
