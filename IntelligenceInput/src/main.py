import sys
import os
from biviterbi import biviterbi
from biviterbi import bisearch
from triviterbi import triviterbi
from triviterbi import trisearch


# print(sys.argv)

if len(sys.argv) == 1:
    print('*'*10 + 'interactive mode' + '*'*10)
    print('Please Input Pinyin Line. Use \'exit\' to quit.\n')
    s = ''
    while s != 'exit':
        s = input()
        if s == 'exit':
            sys.exit(0)
        try:
            s = s.replace('\n', '')
            s = s.replace("lv", "lu")
            s = s.replace("qv", "qu")
            s = s.replace("xv", "xu")
            s = s.replace("jv", "ju")
            s = s.strip()
            s = s.lower()
            s = s.split()
            res = trisearch(triviterbi(s), s)
            for item in res:
                print(item)
            # print(trisearch(triviterbi(s), s))
        except:
            print('again')


if len(sys.argv) == 3:
    print('File mode -- Bi-gram')
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    with open(inpath, 'r') as f:
        lines = f.readlines()

    with open(outpath, 'w') as f:
        for s in lines:
            s = s.replace('\n', '')
            s = s.replace("lv", "lu")
            s = s.replace("qv", "qu")
            s = s.replace("xv", "xu")
            s = s.replace("jv", "ju")
            s = s.strip()
            s = s.lower()
            s = s.split()
            f.write(bisearch(biviterbi(s)) + '\n')


if len(sys.argv) == 4:
    print('File mode -- Tri-gram')
    inpath = sys.argv[1]
    outpath = sys.argv[2]
    with open(inpath, 'r') as f:
        lines = f.readlines()

    with open(outpath, 'w') as f:
        for s in lines:
            s = s.replace('\n', '')
            s = s.replace("lv", "lu")
            s = s.replace("qv", "qu")
            s = s.replace("xv", "xu")
            s = s.replace("jv", "ju")
            s = s.strip()
            s = s.lower()
            s = s.split()
            f.write(trisearch(triviterbi(s), s)[0][0] + '\n')
            # print('\n')


'''
# search parameters mode
if len(sys.argv) == 3 and sys.argv[2] == 'search':
    print('Search mode -- Bi-gram')
    inpath = sys.argv[1]
    with open(inpath, 'r') as f:
        lines = f.readlines()

    for val1 in range(-50, -5, 5):
        default_val1 = (10) ** val1
        with open('One_wrap_val%2d' % (val1), 'w') as f:
            for s in lines:
                s = s.replace('\n', '')
                s = s.replace("lv","lu")
                s = s.replace("qv","qu")
                s = s.replace("xv","xu")
                s = s.replace("jv","ju")
                s = s.strip()
                s = s.lower()
                s = s.split()
                f.write(bisearch(biviterbi(s, default_val1=default_val1)) + '\n')
'''
