# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 20:47:18 2024

@author: sophi
"""
import pandas as pd

ukdata = open("ukb45089.csv", "rt")
line1 = ukdata.readline()
line1 = line1.rstrip()
line1split = line1.split(",")
fil_cols = ["eid", "22140", "22160", "22180", "120002", "41202", "41203", 
"41204", "41205", "41262", "41263", "41270", "41271", "41280", "41281", "2453",
"84", "134", "20001", "20006", "20007", "20012", "40005", "40006", "40008", "40009",
"40011", "40012", "40013", "40001", "40002", "40007", "40010", "31", "33",
"34", "52" , "23098", "23099", "21002", "21000"]
inds = []
for j in range(len(fil_cols)):
    for i, ele in enumerate (line1split):
        elelist = ele.split("-")
        if fil_cols[j] in elelist[0]:
            inds.append(i)
ukdata.close()
data = pd.read_csv("ukb45089.csv", usecols = inds)
print ("csv file has been read into dataframe")
data.to_csv("ukb45089_filtered1.csv", index = False) 