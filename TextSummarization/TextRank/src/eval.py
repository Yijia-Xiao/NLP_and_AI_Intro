from sumeval.metrics.rouge import RougeCalculator


rouge = RougeCalculator(stopwords=True, lang="zh")

'''
rouge_1 = rouge.rouge_n(
            summary="I went to the Mars from my living town.",
            references="I went to Mars",
            n=1)
 
rouge_2 = rouge.rouge_n(
            summary="I went to the Mars from my living town.",
            references=["I went to Mars", "It's my living town"],
            n=2)
 
rouge_l = rouge.rouge_l(
            summary="I went to the Mars from my living town.",
            references=["I went to Mars", "It's my living town"])
'''
import sys
# gamma = str(sys.argv[1])

std = list()
with open('summary.txt', 'r') as f1:
    std = f1.readlines()

with open('topsents.txt', 'r') as f2:
    with open('rankres.txt', 'w') as o:
        for l2, l1 in zip(std, f2.readlines()):
            o.write(str(rouge.rouge_n(summary=l1, references=l2, n=1)) + '\t' + str(rouge.rouge_n(summary=l1, references=l2, n=2)) + '\t' + str(rouge.rouge_l(summary=l1, references=l2)) + '\n')

