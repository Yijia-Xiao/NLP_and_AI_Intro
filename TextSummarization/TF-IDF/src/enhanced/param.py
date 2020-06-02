import os

for i in range(7):
    os.system("python main.py {} > log/naive_digit{}".format(i / 10, i / 10))
