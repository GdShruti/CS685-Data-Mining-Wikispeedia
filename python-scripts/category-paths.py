#!/usr/bin/env python

#importing libraries
import pandas as pd
import csv
import networkx as nx


#loading datasets
tsv_file = open("wikispeedia_paths-and-graph/paths_finished.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
article = pd.read_csv("csv-files/article-ids.csv")
article.set_index("Article_Name",inplace=True)
category = pd.read_csv("csv-files/category-ids.csv")
art_cat =pd.read_csv("csv-files/article-categories.csv")
art_cat.set_index("Article_ID", inplace=True)


#creating graph
g= nx.DiGraph()
edges = pd.read_csv("csv-files/edges.csv")
for x in edges.values:
    g.add_edge(x[0],x[1])



s_paths = {"C{:0>4}".format(i):0 for i in range(1,147)}
s_times = {"C{:0>4}".format(i):0 for i in range(1,147)}
h_paths = {"C{:0>4}".format(i):0 for i in range(1,147)}
h_times = {"C{:0>4}".format(i):0 for i in range(1,147)}



for x in read_tsv:
    if len(x)==5:
        path = x[3]
        temp=[]       
        
        try:
            l=path.split(";")
            if(len(l)>1):
                for x in l:
                    if x=="<":
                        temp.pop()
                    else:
                        temp.append(article.loc[x]["Article_ID"])
                s_id = temp[0]
                d_id = temp[-1]
                cat= []
                for n in temp:
                    cat.extend(art_cat.loc[n]["Category_ID"].split(","))
                for i in set(cat):
                    h_paths[i]+=1
                for i in cat:
                    h_times[i]+=1

                shortest_path = nx.shortest_path(g,s_id,d_id) 
                cat= []
                for n in shortest_path:
                    cat.extend(art_cat.loc[n]["Category_ID"].split(","))
                for i in set(cat):
                    s_paths[i]+=1
                for i in cat:
                    s_times[i]+=1
                    
        except:
            pass
       


df = pd.DataFrame(columns=["C{:0>4}".format(i) for i in range(1,147)])
df.loc["Number_of_human_paths_traversed"] = h_paths
df.loc["Number_of_human_times_traversed"] = h_times
df.loc["Number_of_shortest_paths_traversed"] = s_paths
df.loc["Number_of_shortest_times_traversed"] = s_times
df=df.transpose()
df.index.name="Categoty_ID"


#writing into output file
df.to_csv("csv-files/category-paths.csv")

print("q8")

