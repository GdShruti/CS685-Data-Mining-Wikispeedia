#!/usr/bin/env python

#importing libraries
import pandas as pd
import csv

#loading dataset
tsv_file = open("wikispeedia_paths-and-graph/categories.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")


d={}
for x in read_tsv:
    if len(x)==2:
         for s in x[1].split("."):
                if(s=="subject"):
                    temp=s
                else:
                    temp= temp+"."+s
                    i=temp.count(".")
                    if i in d: 
                        d[i] += [temp]
                    else:
                        d[i] = [temp]

df= pd.DataFrame(columns=["Category_ID"])


df.loc["subject"] = "C0001"
ID = 2 
for x in d:
    for c in sorted(set(d[x])):
        df.loc[c] = "C{:0>4}".format(ID)
        ID+=1

df.index.name="Category_Name"


#writing into output file
df.to_csv('csv-files/category-ids.csv')

print("q2")




