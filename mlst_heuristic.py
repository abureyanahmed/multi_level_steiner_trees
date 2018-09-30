
# coding: utf-8

# # Steiner Tree Problem
# 
# The classical Steiner tree problem is as follows: Given an undirected graph $G=(V,E)$, a set of terminal nodes $T$, and a cost function $c: E\mapsto \mathbb{R}^+$, find a tree $\mathcal{T}\subset G$ that connects the terminal nodes with the minimal cost.
# 
# This problem is NP-hard. However, approximation algorithms exists for the Steiner tree problem. In particular, a 2-approximation algorithm is as follows:
# 
# __2-Approximation Algorithm:__ Build an auxiliary graph $\mathcal{G}=(T,{T \choose 2},w)$, where the edge weights are equal to the shortest path length in graph $G$, i.e., $w(u,v)=d_G(u,v)$ for any $u,v\in T$.

# Here we generate a weighted graph.

# In[54]:

import networkx as nx
import copy
import matplotlib.pyplot as plt
from random import *
import time
from exact_steiner_func import *



def Kruskal_old(G):
    
    MST=nx.create_empty_copy(G); # MST(G)
    i=0; # counter for edges of G
    k=0; # counter for MST(G)
    
    edge_list = sorted(G.edges(data=True), key=lambda x:x[2]['weight'])
    
    while k<nx.number_of_nodes(G)-1:
        e=edge_list[i];
        i+=1
        if not nx.has_path(MST,e[0],e[1]):
            MST.add_edge(e[0],e[1],weight=e[2]['weight'])
            k+=1
    
    return(MST)


def Kruskal(G):
    
    MST=nx.create_empty_copy(G); # MST(G)
    N=nx.number_of_nodes(G)
    E=nx.number_of_edges(G)
    i=0; # counter for edges of G
    k=0; # counter for MST(G)
    
    edge_list = sorted(G.edges(data=True), key=lambda x:x[2]['weight'])
    
    while k<(N-1) and i<(E):
        e=edge_list[i];
        i+=1
        if not nx.has_path(MST,e[0],e[1]):
            MST.add_edge(e[0],e[1],weight=e[2]['weight'])
            k+=1
    
    return(MST)

def print_edges(G):
    edg_arr = []
    for (u,v,d) in G.edges(data='weight'):
        tmp = []
        tmp.append(u)
        tmp.append(v)
        tmp.append(d)
        edg_arr.append(tmp)
    print(edg_arr)


# In[59]:

def SteinerTree2Approx(G,T):
#def SteinerTree(G,T):

    HG=nx.Graph()
    HG.add_nodes_from(T)  # Hyper graph with nodes T and edges with weight equal to distance
    n=len(T)
    
    for i in range(n):
        for j in range(i+1,n):
            HG.add_edge(T[i], T[j], weight=nx.shortest_path_length(G,T[i], T[j],'weight'))
        
    HG_MST = Kruskal(HG)

    G_ST=nx.Graph()
    for e in HG_MST.edges(data=False):
        P=nx.shortest_path(G,e[0],e[1],'weight')
        G_ST.add_path(P)
    
    # find the minimum spanning tree of the resultant graph
    
    return(G_ST)
        




def MLST_Costs(G,G_MLST):
    M=len(G_MLST)
    C=[0]*M
    for m in range(M):
        #print(G_MLST[m].edges(data=False))
        #print_edges(G_MLST[m])
        for e in G_MLST[m].edges(data=False):
            C[m]+=G.get_edge_data(e[0],e[1])['weight']
            #print(str(e[0])+","+str(e[1])+":"+str(G.get_edge_data(e[0],e[1])['weight']))
    #print(C)
    #print(sum(C))
    return(C,sum(C))


# ## Bottom-Up Heuristic
# 
# This is the simplest way: compute the Steiner tree on the lowest level with $\cup_{l=1}^L T_l$ nodes as terminals, and prune away leaves for upper levels.
# 
# Here would be a possible implementation:

# In[63]:

def PruneBranches(G,T):
    has_one=False
    for v in G.nodes(data=False):
        if (v not in T) and (G.degree(v)==1):
            has_one=True
            G.remove_edge(v,*G.neighbors(v))
    if has_one:
        PruneBranches(G,T)

def InclusiveTerminals(TT):
    M=len(TT)
    Tm = list(TT)
    for m in range(1,M):
        Tm[m] = Tm[m-1]+TT[m]
    return(tuple(Tm))
    


# In[64]:

def MLST_BOT(G,TT):
    M=len(TT)
    Tm = InclusiveTerminals(TT)
    
    G_ST_BOT=[None]*M
    #G_ST_BOT[M-1] = SteinerTree(G,Tm[M-1])
    G_ST_BOT[M-1] = SteinerTree(G,Tm[M-1])
    
    for m in range(M-2,-1,-1):
        G_ST_BOT[m] = copy.deepcopy(G_ST_BOT[m+1])
        PruneBranches(G_ST_BOT[m],Tm[m])
    return(tuple(G_ST_BOT))



def MLST_TOP(G,TT):
    
    M=len(TT);
    Tm= InclusiveTerminals(TT)
    
    G_ST_TOP=[None]*M
    G_ST_TOP[0] = SteinerTree(G,Tm[0])
    #G_ST_TOP[0] = SteinerTree2Approx(G,Tm[0])
    #print(G_ST_TOP[0].edges())
    
    for m in range(1,M):
        G2=copy.deepcopy(G)
        for e in G_ST_TOP[m-1].edges(data=True):
            #nx.set_edge_attributes(G2, 'weight', {(e[0],e[1]):0})
            nx.set_edge_attributes(G2, {(e[0],e[1]):{'weight':0}})
        #G_ST_TOP[m] = SteinerTree2Approx(G2,Tm[m])
        G_ST_TOP[m] = SteinerTree(G2,Tm[m])

    return(tuple(G_ST_TOP))




def MLST_Hybrid(G,TT):
    M= len(TT)
    if M==1:
        #print(1)
        G_ST_Hybrid = SteinerTree(G,TT[0])
        return((G_ST_Hybrid,))
    if M>2:
        TTp=(TT[0]+TT[1],*TT[2:M])
    else:
        TTp=(TT[0]+TT[1],)
    G_ST_Hybrid_M1 = MLST_Hybrid(G,TTp)
    G2=copy.deepcopy(G)
    for m in range(len(G_ST_Hybrid_M1)):
        Tree_m= G_ST_Hybrid_M1[m]
        for e in Tree_m.edges():
            G2[e[0]][e[1]]['weight']=(m+1)/M*G[e[0]][e[1]]['weight']
    G_ST_Hybrid_M = SteinerTree(G2,TT[0])
    
    Gp=copy.deepcopy(G)
    for e in G_ST_Hybrid_M.edges():
            Gp[e[0]][e[1]]['weight']=0
    G_ST_Hybrid_M = (G_ST_Hybrid_M,*MLST_Hybrid(Gp,TTp))
    
    return(G_ST_Hybrid_M)
    


import math


def MLST_QoS_error(G,TT):
    M= len(TT)
    q=math.ceil(math.log2(M))
    TR=[]; TTR=[];

    for l in range(M):
        qp=math.ceil(math.log2(M-l))
        if qp<q:
            TTR.append(TR)
            q=qp
            TR=[]    
        TR=TR+TT[l]

    TTR.append(TR)

    STq = [None]*len(TTR)
    for q in range(len(TTR)):
        STq[q]=SteinerTree(G,TTR[q])

    G_ST_QoS = [None]*M
    q=math.ceil(math.log2(M))
    Tdummy=TTR[0]; k=0;
    for l in range(M):
        qp=math.ceil(math.log2(M-l))
        if qp<q:
            k+=1
            Tdummy=Tdummy+TTR[k]
            q=qp
            
        if l==0:
            G_ST_QoS[l]=copy.deepcopy(STq[0])
        else:
            STdummy=nx.create_empty_copy(G)
            STdummy.add_edges_from(STq[k].edges(),weight=2)
            STdummy.add_edges_from(G_ST_QoS[l-1].edges(),weight=1)
            STdummy=Kruskal(STdummy)
            PruneBranches(STdummy,Tdummy)
            G_ST_QoS[l]=copy.deepcopy(STdummy);

    return(tuple(G_ST_QoS))




def MLST_QoS(G,TT):
    M= len(TT)
    q=math.ceil(math.log2(M))
    TR=[]; TTR=[]
    Tm= InclusiveTerminals(TT)
    for l in range(M):
        qp=math.ceil(math.log2(M-l))
        if qp<q:
            TTR.append(TR)
            q=qp
            TR=[]    
        TR=TR+TT[l]

    TTR.append(TR)
    

    STq=MLST_TOP(G,TTR)
    
    G_ST_QoS = [None]*M
    q=math.ceil(math.log2(M))
    Tdummy=TTR[0]; k=0;
    for l in range(M):
        qp=math.ceil(math.log2(M-l))
        if qp<q:
            k+=1
            q=qp
            
        if l==0:
            STdummy=copy.deepcopy(STq[0])
            PruneBranches(STdummy,Tm[0])
            G_ST_QoS[0]=copy.deepcopy(STdummy)
        else:
            STdummy=nx.create_empty_copy(G)
            STdummy.add_edges_from(STq[k].edges(),weight=2)
            STdummy.add_edges_from(G_ST_QoS[l-1].edges(),weight=1)
            STdummy=Kruskal(STdummy)
            PruneBranches(STdummy,Tm[l])
            G_ST_QoS[l]=copy.deepcopy(STdummy);
        
    
    return(tuple(G_ST_QoS))


def MLST_CMP(G,TT,Q):
 M= len(TT)
 Tm= InclusiveTerminals(TT)
 Q=sorted(Q)
 # print(Q)
 m= len(Q)
 G_ST_CMP=[None]*M
 G_ST_CMP[Q[0]-1] = SteinerTree(G,Tm[Q[0]-1])
 # print('Start at',Q[0])
 for j in range(Q[0]-2,-1,-1):
  G_ST_CMP[j] = copy.deepcopy(G_ST_CMP[j+1])
  PruneBranches(G_ST_CMP[j],Tm[j])
  # print('1st Prune up',j+1)

 for i in range(1,m):
  G2=copy.deepcopy(G)
  # print('parent',Q[i-1])
  for e in G_ST_CMP[Q[i-1]-1].edges(data=True):
   #nx.set_edge_attributes(G2, 'weight', {(e[0],e[1]):0})
   nx.set_edge_attributes(G2, {(e[0],e[1]):{'weight':0}})
  G_ST_CMP[Q[i]-1] = SteinerTree(G2,Tm[Q[i]-1])
  # print('child',Q[i])
  for j in range(Q[i]-2,Q[i-1]-1,-1):
   # print('prune',j+1)
   G_ST_CMP[j] = copy.deepcopy(G_ST_CMP[j+1])
   PruneBranches(G_ST_CMP[j],Tm[j])

 return(tuple(G_ST_CMP,)) 

#####################

def powerset(seq):

 if len(seq) <= 1:
  yield seq
  yield []
 else:
  for item in powerset(seq[1:]):
   yield [seq[0]]+item
   yield item

######################

def MLST_BC(G,TT):
 M= len(TT)
 CB=-1;
 for Q in powerset(list(range(1,M))):
  G_MLST_CMP = MLST_CMP(G,TT,Q+[M])
  CMP_Q=MLST_Costs(G,G_MLST_CMP)[1]
  #print(CMP_Q,Q+[M])
  if CB==-1 or CB>CMP_Q:
   CB=CMP_Q
   G_MLST_BC = G_MLST_CMP
 #print(CB)

 return(G_MLST_BC)  

#################

def MLST_CMP_opt(G,TT):

 M= len(TT)
 Tm= InclusiveTerminals(TT)

 MIN=[None]*M

 for l in range(M):
  ST = SteinerTree(G,Tm[l])
  C=0;
  for e in ST.edges(data=False):
   C+=G.get_edge_data(e[0],e[1])['weight']
  MIN[l] = C;

 #print(MIN)

 CQ_opt=-1;
 for Q in powerset(list(range(1,M))):
  Qs=sorted(Q+[M])
  #print(Qs)
  CQ=M*MIN[Qs[0]-1]
  for i in range(1,len(Qs)):
   CQ+=(M-Qs[i-1])*MIN[Qs[i]-1]

  if CQ_opt==-1 or CQ_opt>CQ:
   CQ_opt=CQ
   Q_opt=Qs

 # print(CQ_opt/sum(MIN),Q_opt)

 return(MLST_CMP(G,TT,Q_opt))
    


import sys
if len(sys.argv) < 8:
    #print("Usage: python3 mlst_heuristic.py root={/Users/abureyanahmed/Desktop/testenv/venv/Graph\ generator/steiner_app} steiner_scores_heuristic.js number_of_graphs minimum_graph_index heuristic={0/bottom_up,1/top_down,2/kruskal}")
    print("Usage: python3 mlst_heuristic.py /path/to/graph/folder/graph_ /path/to/result/folder/ steiner_scores.js number_of_graphs minimum_graph_index heuristic={0/bottom_up,1/top_down,2/hybrid,3/QoS,4/BC,5/CMP_opt} time.js")
    quit()
import numpy as np

#name_of_graph_class = ['WS','ER','BA','GE']
#name_of_graph_class = ['WS']
#number_of_nodes_progression = [50, 100, 150]
#number_of_nodes_progression = [50, 100]
#number_of_nodes_progression = [100]
#number_of_levels = [2,3,4,5]
#number_of_levels = [4]
#node_distribution_in_levels = ['L','E']
#node_distribution_in_levels = ['L']
#graphs_per_fixed_setup = 5
#param1 = ['6', '.25', '5', '1.62']
#param2 = ['.2', '0', '0', '0']
#heuristic_names = ['BU', 'TD', 'HY']
#heuristics = ["0", "1", "2"]
#for cl in range(len(name_of_graph_class)):
# for prog in range(len(number_of_nodes_progression)):
#  for l in range(len(number_of_levels)):
#   for nd in range(len(node_distribution_in_levels)):
#    for fs in range(graphs_per_fixed_setup):
#     if number_of_nodes_progression[prog]==50:
#      common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
#      print(common_part_of_name)
#      for heu in range(len(heuristics)):
file = open(sys.argv[2]+sys.argv[3],"w")
file.write("var scores = [");
file.close()

file = open(sys.argv[2]+sys.argv[7],"w")
file.write("var times = [");
file.close()

size=int(sys.argv[4])
min_index = int(sys.argv[5])
heuristic = sys.argv[6]
for i in range(min_index, size):
 G=nx.Graph()
 file = open(sys.argv[1]+str(i+1)+".txt","r")
 #print(sys.argv[1]+str(i+1)+".txt")
 m = int(file.readline())
 edge_list = list()
 for j in range(m):
  #edge_list.append([int(x) for x in file.readline().split()])
  t_arr1 = []
  t_arr2 = file.readline().split()
  t_arr1.append(int(t_arr2[0]))
  t_arr1.append(int(t_arr2[1]))
  t_arr1.append(float(t_arr2[2]))
  edge_list.append(t_arr1)

 n = max(max(u, v) for [u, v, w] in edge_list) # Get size of matrix
 G.add_nodes_from([i for i in range(n)])
 for j in range(m):
  G.add_edge(edge_list[j][0]-1, edge_list[j][1]-1, weight=edge_list[j][2])


 levels = int(file.readline())
 tree_ver=[]
 #tree_ver = [(int(x)-1) for x in raw_input().split()]
 for l2 in range(levels):
  tree_ver.append([(int(x)-1) for x in file.readline().split()])
 file.close()

 TT = (tree_ver[0],)
 for l2 in range(1,levels):
  TT = TT + (tree_ver[l2][len(tree_ver[l2-1]):],)

 start_time = time.time()
 if heuristic=="0":
  TT2 = MLST_BOT(G,TT)
 elif heuristic=="1":
  TT2 = MLST_TOP(G,TT)
 elif heuristic=="2":
  TT2 = MLST_Hybrid(G,TT)
 elif heuristic=="3":
  TT2 = MLST_QoS(G,TT)
 elif heuristic=="4":
  TT2 = MLST_BC(G,TT)
 elif heuristic=="5":
  TT2 = MLST_CMP_opt(G,TT)


 file = open(sys.argv[2]+sys.argv[3],"a")
 file.write(str(MLST_Costs(G,TT2)[1]))
 #print(str(MLST_Costs(G,TT2)[1]))
 if i<(size-1):
  file.write(",")
 file.close()

 file = open(sys.argv[2]+sys.argv[7],"a")
 file.write(str(time.time() - start_time))
 if i<(size-1):
  file.write(",")
 file.close()

file = open(sys.argv[2]+sys.argv[3],"a")
file.write("];\n");
file.close()

file = open(sys.argv[2]+sys.argv[7],"a")
file.write("];\n");
file.close()
#     elif number_of_nodes_progression[prog]==100:
#      seq_of_name_arr = ['_10_70']
#      NUMBER_OF_GRAPHS_arr = [60]
#      INITIAL_NUMBER_OF_NODES_arr = [10]
#      MINIMUM_GRAPH_INDEX_arr = [0]
#      for node_start in np.arange(70,100,5):
#       seq_of_name_arr.append('_'+str(node_start)+'_'+str(node_start+5))
#       NUMBER_OF_GRAPHS_arr.append(node_start-5)
#       INITIAL_NUMBER_OF_NODES_arr.append(node_start)
#       MINIMUM_GRAPH_INDEX_arr.append(node_start-10)
#      common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
#      for part in range(len(seq_of_name_arr)):
#       seq_of_name = seq_of_name_arr[part]
#       print(common_part_of_name+seq_of_name)
#       for heu in range(len(heuristics)):
#        file = open(sys.argv[2]+"steiner_scores_"+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+".js","w")
#        file.write("var scores = [");
#        file.close()

#        size=number_of_nodes_progression[prog]-10
#        min_index = 0
#        heuristic = heuristics[heu]
#        for i in range(min_index, size):
#         G=nx.Graph()
#         file = open(sys.argv[1]+common_part_of_name+"/graph_"+str(i+1)+".txt","r")
#         m = int(file.readline())
#         edge_list = list()
#         for j in range(m):
#          #edge_list.append([int(x) for x in file.readline().split()])
#          t_arr1 = []
#          t_arr2 = file.readline().split()
#          t_arr1.append(int(t_arr2[0]))
#          t_arr1.append(int(t_arr2[1]))
#          t_arr1.append(float(t_arr2[2]))
#          edge_list.append(t_arr1)

#         n = max(max(u, v) for [u, v, w] in edge_list) # Get size of matrix
#         G.add_nodes_from([i for i in range(n)])
#         for j in range(m):
#           G.add_edge(edge_list[j][0]-1, edge_list[j][1]-1, weight=edge_list[j][2])


#         levels = int(file.readline())
#         tree_ver=[]
#         #tree_ver = [(int(x)-1) for x in raw_input().split()]
#         for l2 in range(levels):
#           tree_ver.append([(int(x)-1) for x in file.readline().split()])
#         file.close()
#         TT = (tree_ver[0],)
#         for l2 in range(1,levels):
#           TT = TT + (tree_ver[l2],)
#         if heuristic=="0":
#           TT2 = MLST_BOT(G,TT)
#         elif heuristic=="1":
#           TT2 = MLST_TOP(G,TT)
#         else:
#           TT2 = MLST_Hybrid(G,TT)

#         file = open(sys.argv[2]+"steiner_scores_"+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+".js","a")
#         file.write(str(MLST_Costs(G,TT2)[1]))
#         if i<(size-1):
#          file.write(",")
#         file.close()

#        file = open(sys.argv[2]+"steiner_scores_"+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+".js","a")
#        file.write("];\n");
#        file.close()



