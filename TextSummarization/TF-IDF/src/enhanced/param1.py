import os

for i in range(1, 8):
    os.system("python main1.py {} > log/log_digit{}".format(i / 10, i / 10))
