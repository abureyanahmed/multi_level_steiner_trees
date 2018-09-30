import sys
if len(sys.argv) < 2:
    #print("Usage: python3 mlst_heuristic.py root={/Users/abureyanahmed/Desktop/testenv/venv/Graph\ generator/steiner_app} steiner_scores_heuristic.js number_of_graphs minimum_graph_index heuristic={0/bottom_up,1/top_down,2/kruskal}")
    print("Usage: python3 create_qsubs_heu.py experiment7")
    quit()
import numpy as np
experiment_name = sys.argv[1] 

#name_of_graph_class = ['WS','ER','BA','GE']
name_of_graph_class = ['ER','BA']
#number_of_nodes_progression = [50, 100, 150]
#number_of_nodes_progression = [50, 100]
number_of_nodes_progression = [100]
number_of_levels = [2,3,4,5]
#number_of_levels = [5]
node_distribution_in_levels = ['L','E']
#node_distribution_in_levels = ['L']
graphs_per_fixed_setup = 5
param1 = ['6', '.25', '5', '1.62']
param2 = ['.2', '0', '0', '0']
#heuristic_names = ['BU', 'TD', 'HY', 'QoS', 'BC', 'CMP_opt']
heuristic_names = ['BU']
#heuristics = ["0", "1", "2", "3", "4", "5"]
heuristics = ["0"]
f = open('qsub_commands_heu.sh','w')
f_lpc = open('qsub_commands_heu_lpc.sh','w')
f_lpc.write('module load python/3/3.5.2\n')
for cl in range(len(name_of_graph_class)):
 for prog in range(len(number_of_nodes_progression)):
  for l in range(len(number_of_levels)):
   for nd in range(len(node_distribution_in_levels)):
    for fs in range(graphs_per_fixed_setup):
#    for fs in range(4,5):
     if number_of_nodes_progression[prog]==50:
      common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
      print(common_part_of_name)
#      for heu in range(len(heuristics)):
#       file = open(sys.argv[2]+"steiner_scores_"+common_part_of_name+"_"+heuristic_names[heu]+".js","w")
#       file.write("var scores = [");
#       file.close()

#       size=number_of_nodes_progression[prog]-10
#       min_index = 0
#       heuristic = heuristics[heu]
#       for i in range(min_index, size):
#        G=nx.Graph()
#        file = open(sys.argv[1]+common_part_of_name+"/graph_"+str(i+1)+".txt","r")
#        m = int(file.readline())
#        edge_list = list()
#        for j in range(m):
#         #edge_list.append([int(x) for x in file.readline().split()])
#         t_arr1 = []
#         t_arr2 = file.readline().split()
#         t_arr1.append(int(t_arr2[0]))
#         t_arr1.append(int(t_arr2[1]))
#         t_arr1.append(float(t_arr2[2]))
#         edge_list.append(t_arr1)

#        n = max(max(u, v) for [u, v, w] in edge_list) # Get size of matrix
#        G.add_nodes_from([i for i in range(n)])
#        for j in range(m):
#          G.add_edge(edge_list[j][0]-1, edge_list[j][1]-1, weight=edge_list[j][2])


#        levels = int(file.readline())
#        tree_ver=[]
#        #tree_ver = [(int(x)-1) for x in raw_input().split()]
#        for l2 in range(levels):
#          tree_ver.append([(int(x)-1) for x in file.readline().split()])
#        file.close()
#        TT = (tree_ver[0],)
#        for l2 in range(1,levels):
#          TT = TT + (tree_ver[l2],)
#        if heuristic=="0":
#          TT2 = MLST_BOT(G,TT)
#        elif heuristic=="1":
#          TT2 = MLST_TOP(G,TT)
#        else:
#          TT2 = MLST_Hybrid(G,TT)

#        file = open(sys.argv[2]+"steiner_scores_"+common_part_of_name+"_"+heuristic_names[heu]+".js","a")
#        file.write(str(MLST_Costs(G,TT2)[1]))
#        if i<(size-1):
#         file.write(",")
#        file.close()

#       file = open(sys.argv[2]+"steiner_scores_"+common_part_of_name+"_"+heuristic_names[heu]+".js","a")
#       file.write("];\n");
#       file.close()
     elif number_of_nodes_progression[prog]==100:
      seq_of_name_arr = ['_10_70']
      NUMBER_OF_GRAPHS_arr = [60]
      INITIAL_NUMBER_OF_NODES_arr = [10]
      MINIMUM_GRAPH_INDEX_arr = [0]
      for node_start in np.arange(70,100,5):
       seq_of_name_arr.append('_'+str(node_start)+'_'+str(node_start+5))
       NUMBER_OF_GRAPHS_arr.append(node_start-5)
       INITIAL_NUMBER_OF_NODES_arr.append(node_start)
       MINIMUM_GRAPH_INDEX_arr.append(node_start-10)
      common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
      #for part in range(len(seq_of_name_arr)):
      for part in range(1, len(seq_of_name_arr)):
       seq_of_name = seq_of_name_arr[part]
       print(common_part_of_name+seq_of_name)
       for heu in range(len(heuristics)):
        f.write('export PATTERN_OF_FILE_NAME=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/graph_'+'\n')
        #f.write('export PATH_TO_RESULT_FOLDER=log_files_heuristics_4/'+'\n')
        f.write('export PATH_TO_RESULT_FOLDER=log_files_heuristics_5/'+'\n')
        f.write('export STEINER_SCORE_FILE_NAME='+"steiner_scores_"+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+".js"+'\n')
        f.write('export NUMBER_OF_GRAPHS='+str(NUMBER_OF_GRAPHS_arr[part])+'\n')
        f.write('export MINIMUM_GRAPH_INDEX='+str(MINIMUM_GRAPH_INDEX_arr[part])+'\n')
        f.write('export HEURISTIC='+heuristics[heu]+'\n')
        f.write('export TIME_FILE_NAME=time_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.js'+'\n')
        #f.write('qsub -N mlst_heu_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+' -o log_files/mlst_heu_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.out -e log_files/mlst_heu_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.err -V mlst_heu.sh'+'\n')
        f.write('qsub -N mlst_heu_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+' -o log_files_heuristics_5/mlst_heu_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.out -e log_files_heuristics_5/mlst_heu_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.err -V mlst_heu.sh'+'\n')
        f_lpc.write('python3 mlst_heuristic.py Graph_generator/'+experiment_name+'/'+common_part_of_name+'/graph_'+' log_files_heuristics_4/ '+"steiner_scores_"+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+".js"+' '+str(NUMBER_OF_GRAPHS_arr[part])+' '+str(MINIMUM_GRAPH_INDEX_arr[part])+' '+heuristics[heu]+' time_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.js'+'\n')
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
f.close()
f_lpc.close()
