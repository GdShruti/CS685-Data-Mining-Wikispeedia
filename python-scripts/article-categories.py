#!/usr/bin/env python

#importing libraries
import pandas as pd
import csv

#loading datasets
tsv_file = open("wikispeedia_paths-and-graph/categories.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
article = pd.read_csv("csv-files/article-ids.csv").set_index("Article_Name")
category = pd.read_csv("csv-files/category-ids.csv").set_index("Category_Name")

d={}

for x in read_tsv:
    if len(x)==2:
        c = category.loc[x[1]][0]
        a = article.loc[x[0]][0]
        if a in d:
            d[a] = [d[a][0] +  "," + c]
        else:
            d[a] = [c]


df= pd.DataFrame(data=d)

df = df.transpose()

df.rename(columns={0 : "Category_ID"},inplace=True)
df.index.name = "Article_ID"

category_not_defined=[x for x in ["A{:0>4}".format(i) for i in range(1,4605) ] if x not in list(df.index)]

for x in category_not_defined:
    df.loc[x]="C0001"

df.sort_index()



#writing into output file
df.to_csv("csv-files/article-categories.csv")

print("q3")
