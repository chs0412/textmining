import os

import sys
# while True:
#     a = str(sys.stdin.readline().rstrip())
#     if a=="qqq":
#         break
#     f=open(a+".py",'w')
#     f.close()
#     f=open(a+".csv",'w')
#     f.close()


for i in range(1,51):
    #f=open("test/Art"+str(i)+".csv",'w')
    print("nohup python3 Art.py Art "+str(i)+" 144 &")
    #f.close()

