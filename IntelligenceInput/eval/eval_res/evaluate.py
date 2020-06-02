import os
import os.path
 
 
rootdir = './param_res/'
file_list = os.listdir(rootdir)

std = list()
with open('stdres1000.txt', 'r') as f:
    std = f.readlines()

# f = open('400eval.txt', 'w+')
for fname in file_list:
    with open('./param_res/' + fname, 'r') as f:
        res = f.readlines()
    cnt = 0
    char_cnt = 0
    char_tot = 0
    for p, q in zip(std, res):
        if p == q:
            cnt += 1
        for m, n in zip(p, q):
            if m == n:
                char_cnt += 1
        char_tot += len(p)

    E = int(fname.split('F')[0][2:])
    F = int(fname.split('F')[1][1:-4])
    print(E, F, cnt / len(std), char_cnt / char_tot)

# f.close()