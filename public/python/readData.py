import sys
import numpy as np

k = sys.argv[1]
f = open("F:\Programs\Python\demofile2.txt","r")
data = f.read()
d=data.split(" ")
print(data[k])

sys.stdout.flush()