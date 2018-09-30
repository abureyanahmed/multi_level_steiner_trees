#graph_sizes = [10, 110, 160, 190, 200, 205, 210, 215, 220]
#graph_sizes = [215, 220]
#for i in range(221, 352):
#for i in range(221, 224):
#	graph_sizes.append(i)
#print(graph_sizes)
import sys
import numpy as np
if len(sys.argv) < 2:
 print('usage:python create_qsubs.py experiment7')
 quit()
experiment_name = sys.argv[1]
from subprocess import call
#call(["rm", "-rf", "Graph_generator/"+experiment_name])
#call(["mkdir", "Graph_generator/"+experiment_name])
name_of_graph_class = ['WS','ER','BA','GE']
#name_of_graph_class = ['WS']
#number_of_nodes_progression = [50, 100, 150]
number_of_nodes_progression = [100]
number_of_levels = [2,3,4,5]
#number_of_levels = [2, 3]
node_distribution_in_levels = ['L','E']
graphs_per_fixed_setup = 5
param1 = ['6', '.25', '5', '1.62']
param2 = ['.2', '0', '0', '0']
f = open('qsub_commands_generate_graphs.sh','w')
for cl in range(len(name_of_graph_class)):
 for prog in range(len(number_of_nodes_progression)):
  for l in range(len(number_of_levels)):
   for nd in range(len(node_distribution_in_levels)):
    for fs in range(graphs_per_fixed_setup):
     common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
     f.write('export GRAPH_FOLDER=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/'+'\n')
     f.write('export NUMBER_OF_GRAPHS='+str(number_of_nodes_progression[prog]-10)+'\n')
     f.write('export NUMBER_OF_LEVELS='+str(number_of_levels[l])+'\n')
     f.write('export INITIAL_NUMBER_OF_NODES='+str(10)+'\n')
     f.write('export CLASS_OF_GRAPH='+str(cl)+'\n')
     f.write('export PARAM1='+param1[cl]+'\n')
     f.write('export PARAM2='+param2[cl]+'\n')
     f.write('export NODE_DISTRIBUTION='+str(nd)+'\n')
     f.write('export COMPRESSED_FILE=mlst_'+common_part_of_name+'.tar.gz'+'\n')
     f.write('export TEMP_FOLDER_NAME=/tmp/mlst_'+common_part_of_name+'\n')
     f.write('export STEINER_SCORE_FILE_NAME=steiner_scores_'+common_part_of_name+'.js'+'\n')
     f.write('export MODEL=0'+'\n')
     f.write('export PATTERN_OF_FILE_NAME=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/graph_'+'\n')
     f.write('export VARIABLE_FILE_NAME=variables_'+common_part_of_name+'.js'+'\n')
     f.write('export TIME_FILE_NAME=time_'+common_part_of_name+'.js'+'\n')
     f.write('export CONSTRAINTS_FILE_NAME=constraints_'+common_part_of_name+'.js'+'\n')
     f.write('export MINIMUM_GRAPH_INDEX=0'+'\n')
     f.write('qsub -N mlst_generate_graphs_'+common_part_of_name+' -o log_files/mlst_generate_graphs_'+common_part_of_name+'.out -e log_files/mlst_generate_graphs_'+common_part_of_name+'.err -V mlst_generate_graphs.sh'+'\n')
f.close()
f = open('qsub_commands_compute.sh','w')
for cl in range(len(name_of_graph_class)):
 for prog in range(len(number_of_nodes_progression)):
  for l in range(len(number_of_levels)):
   for nd in range(len(node_distribution_in_levels)):
    for fs in range(graphs_per_fixed_setup):
     if number_of_nodes_progression[prog]==50:
      common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
      f.write('export GRAPH_FOLDER=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/'+'\n')
      f.write('export NUMBER_OF_GRAPHS='+str(number_of_nodes_progression[prog]-10)+'\n')
      f.write('export NUMBER_OF_LEVELS='+str(number_of_levels[l])+'\n')
      f.write('export INITIAL_NUMBER_OF_NODES='+str(10)+'\n')
      f.write('export CLASS_OF_GRAPH='+str(cl)+'\n')
      f.write('export PARAM1='+param1[cl]+'\n')
      f.write('export PARAM2='+param2[cl]+'\n')
      f.write('export NODE_DISTRIBUTION='+str(nd)+'\n')
      f.write('export COMPRESSED_FILE=mlst_'+common_part_of_name+'.tar.gz'+'\n')
      f.write('export TEMP_FOLDER_NAME=/tmp/mlst_'+common_part_of_name+'\n')
      f.write('export STEINER_SCORE_FILE_NAME=steiner_scores_'+common_part_of_name+'.js'+'\n')
      f.write('export MODEL=0'+'\n')
      f.write('export PATTERN_OF_FILE_NAME=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/graph_'+'\n')
      f.write('export VARIABLE_FILE_NAME=variables_'+common_part_of_name+'.js'+'\n')
      f.write('export TIME_FILE_NAME=time_'+common_part_of_name+'.js'+'\n')
      f.write('export CONSTRAINTS_FILE_NAME=constraints_'+common_part_of_name+'.js'+'\n')
      f.write('export MINIMUM_GRAPH_INDEX=0'+'\n')
      f.write('qsub -N mlst_compute_'+common_part_of_name+' -o log_files/mlst_compute_'+common_part_of_name+'.out -e log_files/mlst_compute_'+common_part_of_name+'.err -V mlst_compute.sh'+'\n')
     elif number_of_nodes_progression[prog]==100:
      #seq_of_name_arr = ['_10_70', '_70_90', '_90_95', '_95_100']
      #NUMBER_OF_GRAPHS_arr = [60, 80, 85, 90]
      #INITIAL_NUMBER_OF_NODES_arr = [10, 70, 90, 95]
      #MINIMUM_GRAPH_INDEX_arr = [0, 60, 80, 85]
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
      for part in range(len(seq_of_name_arr)):
       seq_of_name = seq_of_name_arr[part]
       f.write('export GRAPH_FOLDER=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/'+'\n')
       f.write('export NUMBER_OF_GRAPHS='+str(NUMBER_OF_GRAPHS_arr[part])+'\n')
       f.write('export NUMBER_OF_LEVELS='+str(number_of_levels[l])+'\n')
       f.write('export INITIAL_NUMBER_OF_NODES='+str(INITIAL_NUMBER_OF_NODES_arr[part])+'\n')
       f.write('export CLASS_OF_GRAPH='+str(cl)+'\n')
       f.write('export PARAM1='+param1[cl]+'\n')
       f.write('export PARAM2='+param2[cl]+'\n')
       f.write('export NODE_DISTRIBUTION='+str(nd)+'\n')
       f.write('export COMPRESSED_FILE=mlst_'+common_part_of_name+seq_of_name+'.tar.gz'+'\n')
       f.write('export TEMP_FOLDER_NAME=/tmp/mlst_'+common_part_of_name+seq_of_name+'\n')
       f.write('export STEINER_SCORE_FILE_NAME=steiner_scores_'+common_part_of_name+seq_of_name+'.js'+'\n')
       #test
       #f.write('export MODEL=0'+'\n')
       f.write('export MODEL=1'+'\n')
       f.write('export PATTERN_OF_FILE_NAME=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/graph_'+'\n')
       f.write('export VARIABLE_FILE_NAME=variables_'+common_part_of_name+seq_of_name+'.js'+'\n')
       f.write('export TIME_FILE_NAME=time_'+common_part_of_name+seq_of_name+'.js'+'\n')
       f.write('export CONSTRAINTS_FILE_NAME=constraints_'+common_part_of_name+seq_of_name+'.js'+'\n')
       f.write('export MINIMUM_GRAPH_INDEX='+str(MINIMUM_GRAPH_INDEX_arr[part])+'\n')
       f.write('qsub -N mlst_compute_'+common_part_of_name+seq_of_name+' -o log_files/mlst_compute_'+common_part_of_name+seq_of_name+'.out -e log_files/mlst_compute_'+common_part_of_name+seq_of_name+'.err -V mlst_compute.sh'+'\n')
     else:
      #seq_of_name_arr = ['_10_70', '_70_95', '_95_110', '_110_120', '_120_130', '_130_135', '_135_140', '_140_145', '_145_149', '_149_150']
      #NUMBER_OF_GRAPHS_arr = [60, 85, 100, 110, 120, 125, 130, 135, 139, 140]
      #INITIAL_NUMBER_OF_NODES_arr = [10, 70, 95, 110, 120, 130, 135, 140, 145, 149]
      #MINIMUM_GRAPH_INDEX_arr = [0, 60, 85, 100, 110, 120, 125, 130, 135, 139]
      seq_of_name_arr = ['_10_70']
      NUMBER_OF_GRAPHS_arr = [60]
      INITIAL_NUMBER_OF_NODES_arr = [10]
      MINIMUM_GRAPH_INDEX_arr = [0]
      for node_start in np.arange(70,100,5):
       seq_of_name_arr.append('_'+str(node_start)+'_'+str(node_start+5))
       NUMBER_OF_GRAPHS_arr.append(node_start-5)
       INITIAL_NUMBER_OF_NODES_arr.append(node_start)
       MINIMUM_GRAPH_INDEX_arr.append(node_start-10)
      for node_start in np.arange(100,150,2):
       seq_of_name_arr.append('_'+str(node_start)+'_'+str(node_start+2))
       NUMBER_OF_GRAPHS_arr.append(node_start-8)
       INITIAL_NUMBER_OF_NODES_arr.append(node_start)
       MINIMUM_GRAPH_INDEX_arr.append(node_start-10)
      common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
      for part in range(len(seq_of_name_arr)):
       seq_of_name = seq_of_name_arr[part]
       f.write('export GRAPH_FOLDER=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/'+'\n')
       f.write('export NUMBER_OF_GRAPHS='+str(NUMBER_OF_GRAPHS_arr[part])+'\n')
       f.write('export NUMBER_OF_LEVELS='+str(number_of_levels[l])+'\n')
       f.write('export INITIAL_NUMBER_OF_NODES='+str(INITIAL_NUMBER_OF_NODES_arr[part])+'\n')
       f.write('export CLASS_OF_GRAPH='+str(cl)+'\n')
       f.write('export PARAM1='+param1[cl]+'\n')
       f.write('export PARAM2='+param2[cl]+'\n')
       f.write('export NODE_DISTRIBUTION='+str(nd)+'\n')
       f.write('export COMPRESSED_FILE=mlst_'+common_part_of_name+seq_of_name+'.tar.gz'+'\n')
       f.write('export TEMP_FOLDER_NAME=/tmp/mlst_'+common_part_of_name+seq_of_name+'\n')
       f.write('export STEINER_SCORE_FILE_NAME=steiner_scores_'+common_part_of_name+seq_of_name+'.js'+'\n')
       f.write('export MODEL=0'+'\n')
       f.write('export PATTERN_OF_FILE_NAME=Graph_generator/'+experiment_name+'/'+common_part_of_name+'/graph_'+'\n')
       f.write('export VARIABLE_FILE_NAME=variables_'+common_part_of_name+seq_of_name+'.js'+'\n')
       f.write('export TIME_FILE_NAME=time_'+common_part_of_name+seq_of_name+'.js'+'\n')
       f.write('export CONSTRAINTS_FILE_NAME=constraints_'+common_part_of_name+seq_of_name+'.js'+'\n')
       f.write('export MINIMUM_GRAPH_INDEX='+str(MINIMUM_GRAPH_INDEX_arr[part])+'\n')
       f.write('qsub -N mlst_compute_'+common_part_of_name+seq_of_name+' -o log_files/mlst_compute_'+common_part_of_name+seq_of_name+'.out -e log_files/mlst_compute_'+common_part_of_name+seq_of_name+'.err -V mlst_compute.sh'+'\n')
f.close()
