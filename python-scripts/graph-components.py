#!/usr/bin/env python

#importing libraries
import pandas as pd
import networkx as nx


#creating graph
g = nx.Graph()
for i in range(1,4605):
    g.add_node("A{:0>4}".format(i))
edges = pd.read_csv("csv-files/edges.csv")
for x in edges.values:
    g.add_edge(x[0],x[1])


ds=[]
for c in nx.connected_components(g):
    g1=g.subgraph(c).copy()
    ds.append([ nx.number_of_nodes(g1)  ,nx.number_of_edges(g1),nx.diameter(g1)])


#writing into output file
pd.DataFrame(ds).rename(columns={0:"Nodes", 1:"Edges", 2:"Diameter"}).to_csv("csv-files/graph-components.csv",index=None)

print("q5")
