#!/usr/bin/env python

#import libraries
import pandas as pd
import csv
import networkx as nx


#loading dataset
tsv_file = open("wikispeedia_paths-and-graph/paths_finished.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
article = pd.read_csv("csv-files/article-ids.csv")
article.set_index("Article_Name",inplace=True)
category = pd.read_csv("csv-files/category-ids.csv")


shortest_path= pd.DataFrame()
ind = ["A{:0>4}".format(i) for i in range(1,4605)]


#creating graph
g= nx.DiGraph()
edges = pd.read_csv("csv-files/edges.csv")
for x in edges.values:
    g.add_edge(x[0],x[1])


with_b = []
without_b =[]
for x in read_tsv:
    if len(x)==5:
        path = x[3]
        temp = path.split(";")
        e = len(temp)-1
        e1= e - (2* temp.count("<"))
        s_id = article.loc[temp[0]]["Article_ID"]
        d_id = article.loc[temp[-1]]["Article_ID"]
        try:
            shortest_path = nx.shortest_path_length(g,s_id,d_id) 
            with_b.append([e,shortest_path , e/shortest_path])
            without_b.append([e1 , shortest_path , e1/shortest_path ])
        except:
            pass
        
        
   

#writing into output files
pd.DataFrame(with_b).rename(columns={0:"Human_Path_Length" , 1:"Shortest_Path_Length", 2:"Ratio"}).to_csv("csv-files/finished-paths-back.csv",index=None)

pd.DataFrame(without_b).rename(columns={0:"Human_Path_Length" , 1:"Shortest_Path_Length", 2:"Ratio"}).to_csv("csv-files/finished-paths-no-back.csv",index=None)

print("q6")
