#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import csv
import networkx as nx
g= nx.DiGraph()
tsv_file = open("wikispeedia_paths-and-graph/paths_finished.tsv")
path_finished = csv.reader(tsv_file, delimiter="\t")

tsv_file = open("wikispeedia_paths-and-graph/paths_unfinished.tsv")
path_unfinished = csv.reader(tsv_file, delimiter="\t")


article = pd.read_csv("csv-files/article-ids.csv")
article.set_index("Article_Name",inplace=True)
category = pd.read_csv("csv-files/category-ids.csv")
cat_id_name = category.set_index("Category_ID")
cat_name_id = category.set_index("Category_Name")
art_cat =pd.read_csv("csv-files/article-categories.csv")
art_cat.set_index("Article_ID", inplace=True)





incorrect_spellings={"USA":"United_States" , 
                     "Mustard":"Mustard_plant",
                     "Long_peper": "Long_pepper",
                     "Adolph_Hitler":"Adolf_Hitler" ,
                     "Charlottes_web": "Charlotte%27s_Web",
                     "_Zebra":"Zebra", 
                     "Kashmir" :"Kashmir_region", 
                     "Rss" : "RSS_%28file_format%29",
                     "Georgia":"Georgia_%28country%29",
                     "English": "English_language",
                     "Macedonia" : "Republic_of_Macedonia"
                    }




pf_dict ={}
puf_dict ={}


# In[4]:


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




for x in path_finished:
    if len(x)==5:
        path = x[3]
        temp=[]       
        
        try:
            l=path.split(";")
            if(len(l)>1):
                '''for x in l:
                    if x=="<":
                        temp.pop()
                    else:
                        temp.append(article.loc[x]["Article_ID"])'''
                s_id = article.loc[l[0]]["Article_ID"]
                d_id = article.loc[l[-1]]["Article_ID"]
                
                s_cat = art_sub_cat[s_id]
                d_cat = art_sub_cat[d_id]
               
                
                #cross-product of source and destination categories
                l=[(x,y) for x in s_cat for y in d_cat] 
                for (s,d) in l:
                    if (s,d) in pf_dict:
                        pf_dict[(s,d)] += 1
                    else:
                        pf_dict[(s,d)] = 1
                    
        except:
            pass
       





for x in path_unfinished:
    if len(x)==6:
        path = x[3]
        temp=[]       
        
        try:
            l=path.split(";")
            
            if l[0] in incorrect_spellings:
                s_id = article.loc[incorrect_spellingso[l[0]]]["Article_ID"]
            else:
                s_id = article.loc[l[0]]["Article_ID"]
            if x[4] in incorrect_spellings:
                d_id = article.loc[incorrect_spellings[x[4]]]["Article_ID"]
            else:
                d_id = article.loc[x[4]]["Article_ID"]
            
            s_cat = art_sub_cat[s_id]
            d_cat = art_sub_cat[d_id]
            
            
            #cross-product of source and destination categories
            l=[(x,y) for x in s_cat for y in d_cat] 
            for (s,d) in l:
                if (s,d) in puf_dict:
                    puf_dict[(s,d)] += 1
                else:
                    puf_dict[(s,d)] = 1
                    
        except:
            pass




df=pd.DataFrame(columns=["From_Category","To_Category","Percentage_of_finished_paths","Percentage_of_unfinished_paths"])



i=0
for k in pf_dict:
    pf = pf_dict[k]
    puf=0
    if k in puf_dict:
        puf= puf_dict[k]
    df.loc[i] = [k[0],k[1], (pf*100)/(pf+puf) ,(puf*100)/(pf+puf)] 
    i+=1


df.sort_values(by=["From_Category","To_Category"],inplace=True )
df.to_csv("csv-files/category-pairs.csv",index=None)


print("q10")
