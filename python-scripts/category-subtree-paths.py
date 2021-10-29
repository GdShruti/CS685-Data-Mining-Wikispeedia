#!/usr/bin/env python


import pandas as pd
import csv
import networkx as nx
g= nx.DiGraph()
tsv_file = open("wikispeedia_paths-and-graph/paths_finished.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
article = pd.read_csv("csv-files/article-ids.csv")
article.set_index("Article_Name",inplace=True)
category = pd.read_csv("csv-files/category-ids.csv")
cat_id_name = category.set_index("Category_ID")
cat_name_id = category.set_index("Category_Name")
art_cat =pd.read_csv("csv-files/article-categories.csv")
art_cat.set_index("Article_ID", inplace=True)



edges = pd.read_csv("csv-files/edges.csv")
for x in edges.values:
    g.add_edge(x[0],x[1])



def get_sub_category_id(n):
    sub_cat=set()
    x = cat_id_name.loc[n]["Category_Name"]
    x_list = x.split(".")
    for i,y in enumerate(x_list):
        sub_cat.add(cat_name_id.loc[".".join(x_list[0:i+1])]["Category_ID"])
    return sub_cat 


sub_cat_dict = {}
for x in list(category["Category_ID"]):
    sub_cat_dict[x] = list(get_sub_category_id(x))



s_paths = {"C{:0>4}".format(i):0 for i in range(1,147)}
s_times = {"C{:0>4}".format(i):0 for i in range(1,147)}
h_paths = {"C{:0>4}".format(i):0 for i in range(1,147)}
h_times = {"C{:0>4}".format(i):0 for i in range(1,147)}


# In[5]:


for x in read_tsv:
    if len(x)==5:
        path = x[3]
        temp=[]
        l=path.split(";")
        if(len(l)>1):
            for x in l:
                if x=="<":
                    temp.pop()
                else:
                    temp.append(article.loc[x]["Article_ID"])
            s_id = temp[0]
            d_id = temp[-1]
            
            try:
                sub_cat1=set()
                for n in temp:
                    cat = art_cat.loc[n]["Category_ID"].split(",")
                    sub_cat=set()
                    for x in cat:
                        sub_cat= sub_cat.union(set(sub_cat_dict[x]))
                      
                    for y in sub_cat:
                        h_times[y] +=1
       
                    sub_cat1 = sub_cat1.union(sub_cat)
                     
                for x in sub_cat1:
                    h_paths[x] +=1

                
                shortest_path = nx.shortest_path(g,s_id,d_id) 
                sub_cat1=set()
                for n in shortest_path:
                    cat = art_cat.loc[n]["Category_ID"].split(",")
                    sub_cat=set()
                    for x in cat:
                        sub_cat= sub_cat.union(set(sub_cat_dict[x]))
                      
                    for y in sub_cat:
                        s_times[y] +=1
       
                    sub_cat1 = sub_cat1.union(sub_cat)
                     
                for x in sub_cat1:
                    s_paths[x] +=1

            except:
                pass
          


df = pd.DataFrame(columns=["C{:0>4}".format(i) for i in range(1,147)])
df.loc["Number_of_human_paths_traversed"] = h_paths
df.loc["Number_of_human_times_traversed"] = h_times
df.loc["Number_of_shortest_paths_traversed"] = s_paths
df.loc["Number_of_shortest_times_traversed"] = s_times
df=df.transpose()
df.index.name="Categoty_ID"

df.to_csv("csv-files/category-subtree-paths.csv")

print("q9")
