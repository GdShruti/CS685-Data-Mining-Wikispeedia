#!/usr/bin/env python

#imporiting libraries 
import pandas as pd

#loading datasets
with_b = pd.read_csv("csv-files/finished-paths-back.csv")
without_b= pd.read_csv("csv-files/finished-paths-no-back.csv")


p_b= {"Equal_Length":0,
      "Larger_by_1":0,
      "Larger_by_2":0,
      "Larger_by_3":0,
      "Larger_by_4":0,
      "Larger_by_5":0,
      "Larger_by_6":0,
      "Larger_by_7":0,
      "Larger_by_8":0,
      "Larger_by_9":0,
      "Larger_by_10":0,
      "Larger_by_more_than_10":0}
p_no_b = {"Equal_Length":0,
      "Larger_by_1":0,
      "Larger_by_2":0,
      "Larger_by_3":0,
      "Larger_by_4":0,
      "Larger_by_5":0,
      "Larger_by_6":0,
      "Larger_by_7":0,
      "Larger_by_8":0,
      "Larger_by_9":0,
      "Larger_by_10":0,
      "Larger_by_more_than_10":0}



def percentage(df , d):
    for [h,s,r] in df.values:
        if(h==s):
            d["Equal_Length"] += 1
        elif (h-s)<11:
            d["Larger_by_"+str(int(h-s))] += 1
        else:
            d["Larger_by_more_than_10"] +=1
    for x in d:
        d[x] = (d[x]/51306)*100



percentage(with_b,p_b)
percentage(without_b,p_no_b)


#writing into output files
pd.DataFrame(p_b,index=[0]).to_csv("csv-files/percentage-paths-back.csv",index=None)
pd.DataFrame(p_no_b,index=[0]).to_csv("csv-files/percentage-paths-no-back.csv",index=None)

print("q7")
