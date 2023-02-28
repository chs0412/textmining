import os

import sys
while True:
    a = str(sys.stdin.readline().rstrip())
    if a=="qqq":
        break
    f=open(a+".py",'w')
    f.close()
    f=open(a+".csv",'w')
    f.close()


