#!/usr/bin/env python


#importing librarires
import pandas as pd

#loading data from input file
df= pd.read_csv("wikispeedia_paths-and-graph/articles.tsv","\t")
df.rename(inplace=True,columns={"# The list of all articles.":"Article_Name"})
df = df.iloc[10:]

ind = list("A{:0>4}".format(i) for i in range(1,4605)) 

df["Article_ID"]= ind

#writing into output csv file 
df.to_csv('csv-files/article-ids.csv',index=False)



print("q1")



