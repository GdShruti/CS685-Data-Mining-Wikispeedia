#!/usr/bin/env python


import pandas as pd
import csv
import networkx as nx
g= nx.DiGraph()
tsv_file = open("wikispeedia_paths-and-graph/paths_finished.tsv")
path_finished = csv.reader(tsv_file, delimiter="\t")

article = pd.read_csv("csv-files/article-ids.csv")
article.set_index("Article_Name",inplace=True)
category = pd.read_csv("csv-files/category-ids.csv")
cat_id_name = category.set_index("Category_ID")
cat_name_id = category.set_index("Category_Name")
art_cat =pd.read_csv("csv-files/article-categories.csv")
art_cat.set_index("Article_ID", inplace=True)




di = {}



edges = pd.read_csv("csv-files/edges.csv")
for x in edges.values:
    g.add_edge(x[0],x[1])



def get_sub_category(n):
    cats = [cat_id_name.loc[x]["Category_Name"] for x in art_cat.loc[n]["Category_ID"].split(",")]
    sub_cat = set()            
    for x in cats:
        x_list = x.split(".")
        for i,y in enumerate(x_list):
            sub_cat.add(cat_name_id.loc[".".join(x_list[0:i+1])]["Category_ID"])
    return sub_cat 



art_sub_cat ={}
for x in list(article["Article_ID"]):
    art_sub_cat[x]= list(get_sub_category(x))




i=0
for x in path_finished:
    if len(x)==5:

        path = x[3]
        temp=[]       
        try:
            without_b = [x for x in path.split(";")]
            if len(without_b)>1:
                s_id = article.loc[without_b[0]]["Article_ID"]
                d_id = article.loc[without_b[-1]]["Article_ID"]
               
                s_cat = art_sub_cat[s_id]
             
                d_cat = art_sub_cat[d_id]
                
                e= len(without_b)-1 -(2* without_b.count("<"))
                shortest_path = nx.shortest_path_length(g,s_id,d_id)
                
                #cross-product of source and destination categories
                l=[(x,y) for x in s_cat for y in d_cat] 
                for (s,d) in l:
                    #print((s,d))
                    if (s,d) in di:
                        di[(s,d)]["human_path"] +=  e
                        di[(s,d)]["shortest_path"] +=  shortest_path
                    else:
                        di[(s,d)] = {"human_path": e ,"shortest_path": shortest_path}
                
        except:
          
            pass
       
        i+=1




df=pd.DataFrame(columns=["From_Category","To_Category","Ratio_of_human_to_shortest"])


i=0
for k in di:
    h = di[k]["human_path"]
    s = di[k]["shortest_path"]
    df.loc[i] = [k[0],k[1], h/s] 
    i+=1



df.sort_values(by=["From_Category","To_Category"],inplace=True)


df.to_csv("csv-files/category-ratios.csv",index=None)

print("q11")



