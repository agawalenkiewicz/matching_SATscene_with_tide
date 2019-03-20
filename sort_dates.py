# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:41:58 2018

@author: mp877190
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import pandas as pd
from datetime import datetime
from scipy import interpolate



file = sys.argv[1]

f = open(file)

F = []

for line in f:
	x = str(line[:-2])
	date = datetime.strptime(x, '%Y/%m/%d %H:%M:%S')
	print date
	F.append(date)
    

    
print(F)
F.sort()
print(F)
for i in F:
	i = str(i)
	date_new = datetime.strptime(i, '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
	print(date_new)
#g=open('C://Users/mp877190/Desktop/Heysham_date_time_all.txt','w')
#with open('C://Users/mp877190/Desktop/Sizewell_date_time_all2.txt','w') as text_file: text_file.write(F)

