#!/usr/bin/env python

#importing libraries
import pandas as pd

edges=[]

#loading dataset
f = open("wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt")

f_a=1
t_a=1
for i in f:
    if len(i)==4605:
        f_id = "A{:0>4}".format(f_a)
        t_a  = 1
        tmp = i[:-1]
        for j in tmp:
            if(j=="1"):
                t_id = "A{:0>4}".format(t_a)
                edges.append([f_id,t_id])
            t_a += 1    
        f_a+=1
       

#writing into output file
pd.DataFrame(data=edges,columns=["From_ArticleID","To_ArticleID"]).to_csv("csv-files/edges.csv",sep=",",index=None)



print("q4")
