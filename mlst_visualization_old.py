import numpy as np
import os
import sys
if len(sys.argv) < 4:
 print('usage:python mlst_visualization.py /path/to/exact/score/files/directory /path/to/plots/directory /path/to/heuristic/score/')
 quit()
path_to_directory = sys.argv[1]
path_to_plots_directory = sys.argv[2]
path_to_heuristic = sys.argv[3]
if path_to_directory[len(path_to_directory)-1]!='/':
 path_to_directory = path_to_directory+'/'
if path_to_plots_directory[len(path_to_plots_directory)-1]!='/':
 path_to_plots_directory = path_to_plots_directory+'/'
if path_to_heuristic[len(path_to_heuristic)-1]!='/':
 path_to_heuristic = path_to_heuristic+'/'
steiner_scores = []
steiner_scores_h = []
run_times = []
run_times_h = []
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
heuristic_names = ['BU', 'TD', 'HY', 'QoS', 'BC', 'CMP_opt']
for cl in range(len(name_of_graph_class)):
 steiner_scores.append([])
 steiner_scores_h.append([])
 run_times.append([])
 run_times_h.append([])
 #print("cl:"+str(cl))
 for prog in range(len(number_of_nodes_progression)):
  steiner_scores[cl].append([])
  steiner_scores_h[cl].append([])
  run_times[cl].append([])
  run_times_h[cl].append([])
  #print("prog:"+str(prog))
  for l in range(len(number_of_levels)):
   steiner_scores[cl][prog].append([])
   steiner_scores_h[cl][prog].append([])
   run_times[cl][prog].append([])
   run_times_h[cl][prog].append([])
   #print("l:"+str(l))
   for nd in range(len(node_distribution_in_levels)):
    steiner_scores[cl][prog][l].append([])
    steiner_scores_h[cl][prog][l].append([])
    run_times[cl][prog][l].append([])
    run_times_h[cl][prog][l].append([])
    #print("nd:"+str(nd))
    for fs in range(graphs_per_fixed_setup):
     steiner_scores[cl][prog][l][nd].append([])
     steiner_scores_h[cl][prog][l][nd].append([])
     run_times[cl][prog][l][nd].append([])
     run_times_h[cl][prog][l][nd].append([])
     #print("fs:"+str(fs))
     if number_of_nodes_progression[prog]==50:
      common_part_of_name = name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[prog])+'_'+str(number_of_levels[l])+'_'+node_distribution_in_levels[nd]+'_'+str(fs)
      if os.path.exists(path_to_directory+'steiner_scores_'+common_part_of_name+'.js'):
       #print(path_to_directory+'steiner_scores_'+common_part_of_name+'.js')
       f = open(path_to_directory+'steiner_scores_'+common_part_of_name+'.js')
       f_time = open(path_to_directory+'time_'+common_part_of_name+'.js')
       tmp_arr = f.readline().split('[')[1].split(']')[0].split(',')
       tmp_arr_time = f_time.readline().split('[')[1].split(']')[0].split(',')
       for i in range(len(tmp_arr)):
        steiner_scores[cl][prog][l][nd][fs].append(tmp_arr[i])
        run_times[cl][prog][l][nd][fs].append(tmp_arr_time[i])
       for heu in range(len(heuristic_names)):
        steiner_scores_h[cl][prog][l][nd][fs].append([])
        run_times_h[cl][prog][l][nd][fs].append([])
        #print("heu:"+str(heu))
        if os.path.exists(path_to_heuristic+'steiner_scores_'+common_part_of_name+"_"+heuristic_names[heu]+'.js'):
         f2 = open(path_to_heuristic+'steiner_scores_'+common_part_of_name+"_"+heuristic_names[heu]+'.js')
         f2_time = open(path_to_heuristic+'time_'+common_part_of_name+"_"+heuristic_names[heu]+'.js')
         tmp_arr2 = f2.readline().split('[')[1].split(']')[0].split(',')
         tmp_arr2_time = f2_time.readline().split('[')[1].split(']')[0].split(',')
         for i in range(len(tmp_arr2)):
          steiner_scores_h[cl][prog][l][nd][fs][heu].append(tmp_arr2[i])
          run_times_h[cl][prog][l][nd][fs][heu].append(tmp_arr2_time[i])
         f2.close()
         f2_time.close()
       f.close()
       f_time.close()
      #else:
       #print(path_to_directory+'steiner_scores_'+common_part_of_name+'.js does not exist.')
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
      for part in range(len(seq_of_name_arr)):
       seq_of_name = seq_of_name_arr[part]
       if os.path.exists(path_to_directory+'steiner_scores_'+common_part_of_name+seq_of_name+'.js'):
        f = open(path_to_directory+'steiner_scores_'+common_part_of_name+seq_of_name+'.js')
        f_time = open(path_to_directory+'time_'+common_part_of_name+seq_of_name+'.js')
        tmp_arr = f.readline().split('[')[1].split(']')[0].split(',')
        tmp_arr_time = f_time.readline().split('[')[1].split(']')[0].split(',')
        for i in range(len(tmp_arr)):
         steiner_scores[cl][prog][l][nd][fs].append(float(tmp_arr[i]))
         run_times[cl][prog][l][nd][fs].append(float(tmp_arr_time[i]))
        f.close()
        f_time.close()
        for heu in range(len(heuristic_names)):
         steiner_scores_h[cl][prog][l][nd][fs].append([])
         run_times_h[cl][prog][l][nd][fs].append([])
         if os.path.exists(path_to_heuristic+'steiner_scores_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.js'):
          f2 = open(path_to_heuristic+'steiner_scores_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.js')
          f2_time = open(path_to_heuristic+'time_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.js')
          tmp_arr2 = f2.readline().split('[')[1].split(']')[0].split(',')
          tmp_arr2_time = f2_time.readline().split('[')[1].split(']')[0].split(',')
          for i in range(len(tmp_arr2)):
           if tmp_arr2[i]=='' or tmp_arr2[i]=='\n':
            print(path_to_heuristic+'steiner_scores_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.js')
            #print(tmp_arr2)
            #if len(tmp_arr2)!=5 and len(tmp_arr2)!=60:
            if seq_of_name == '_10_70':
             for ae in range(60-len(tmp_arr2)+1):
              steiner_scores_h[cl][prog][l][nd][fs][heu].append(-1)
              run_times_h[cl][prog][l][nd][fs][heu].append(-1)
            else:
             for ae in range(5-len(tmp_arr2)+1):
              steiner_scores_h[cl][prog][l][nd][fs][heu].append(-1)
              run_times_h[cl][prog][l][nd][fs][heu].append(-1)
            #if tmp_arr2[i]=='':
            # steiner_scores_h[cl][prog][l][nd][fs][heu].append(-1)
            #print(steiner_scores_h[cl][prog][l][nd][fs][heu])
           else:
            steiner_scores_h[cl][prog][l][nd][fs][heu].append(float(tmp_arr2[i]))
            run_times_h[cl][prog][l][nd][fs][heu].append(float(tmp_arr2[i]))
          f2.close()
          f2_time.close()
         else:
          #print(path_to_heuristic+'steiner_scores_'+common_part_of_name+seq_of_name+"_"+heuristic_names[heu]+'.js does not exist.')
          if seq_of_name == '_10_70':
           for ae in range(60):
            steiner_scores_h[cl][prog][l][nd][fs][heu].append(-1)
            run_times_h[cl][prog][l][nd][fs][heu].append(-1)
          else:
           for ae in range(5):
            steiner_scores_h[cl][prog][l][nd][fs][heu].append(-1)
            run_times_h[cl][prog][l][nd][fs][heu].append(-1)
       else:
        print(path_to_directory+'steiner_scores_'+common_part_of_name+seq_of_name+'.js does not exist.')
#print(len(steiner_scores))
#print(len(steiner_scores[0]))
#print(len(steiner_scores[0][0]))
#print(len(steiner_scores[0][0][0]))
#print(len(steiner_scores[0][0][0][0]))
#print(len(steiner_scores[0][0][0][0][0]))
#print(steiner_scores[0][0][0][0][0])

#print(len(steiner_scores_h))
#print(len(steiner_scores_h[0]))
#print(len(steiner_scores_h[0][0]))
#print(len(steiner_scores_h[0][0][0]))
#print(len(steiner_scores_h[0][0][0][0]))
#print(len(steiner_scores_h[0][0][0][0][0]))
#print(len(steiner_scores_h[0][0][0][0][0][0]))
#print(steiner_scores_h[0][0][0][0][0][0])

# Time calculation of ILP
total_time_ILP = 0
total_time = []
for cl in range(len(name_of_graph_class)):
 total_time.append(0)
 for prog in range(len(number_of_nodes_progression)):
  for l in range(len(number_of_levels)):
   for nd in range(len(node_distribution_in_levels)):
    for fs in range(graphs_per_fixed_setup):
     for i in range(number_of_nodes_progression[prog]-10):
      total_time_ILP = total_time_ILP + run_times[cl][prog][l][nd][fs][i]
      total_time[cl] = total_time[cl] + run_times[cl][prog][l][nd][fs][i]
print('total_time_ILP: '+str(total_time_ILP))
for cl in range(len(name_of_graph_class)):
 print(name_of_graph_class[cl] + ': '+ str(total_time[cl]))

quit()

heuristics1 = [0, 1, 4]
heuristics2 = [2, 3, 5]
heuristics3 = [0, 1, 4, 5]
heuristics4 = [1, 4, 5]

#single_level_exact = False
single_level_exact = True

if single_level_exact==True:
 number_of_nodes_progression[0] = 70

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig_count = 1
init_nodes = 10
size = number_of_nodes_progression[0]-10
#print(size)
for cl in range(len(name_of_graph_class)):
 max_label = 0
 heu_range = []
 if single_level_exact==False:
  heu_range = range(len(heuristic_names))
 elif single_level_exact==True:
  heu_range = heuristics3
 for heu in heu_range:
  max_rat = []
  min_rat = []
  avg_rat = []
  cnt = [0]*size
  for i in range(size):
   max_rat.append(0)
   min_rat.append(10000)
   avg_rat.append(0)
   for j in range(graphs_per_fixed_setup):
    for l in range(len(number_of_levels)):
     for nd in range(len(node_distribution_in_levels)):
      #print(cl)
      #print(l)
      #print(nd)
      #print(j)
      #print(heu)
      #print(i)
      if steiner_scores_h[cl][0][l][nd][j][heu][i]==-1:
       continue
      cur_rat = float(steiner_scores_h[cl][0][l][nd][j][heu][i])*1.0/float(steiner_scores[cl][0][l][nd][j][i])
      if max_rat[i]<cur_rat:
       max_rat[i]=cur_rat
      if min_rat[i]>cur_rat:
       min_rat[i]=cur_rat
      avg_rat[i] = avg_rat[i] + cur_rat
      cnt[i] = cnt[i]+1
#   if max_label < max_rat[i]:
#    max_label = max_rat[i]
  for i in range(size):
   #avg_rat[i] = avg_rat[i]/(graphs_per_fixed_setup*len(number_of_levels)*len(node_distribution_in_levels))
   avg_rat[i] = avg_rat[i]/cnt[i]
  plt.figure(fig_count)
  fig_count = fig_count + 1
  max_rat2 = []
  min_rat2 = []
  avg_rat2 = []
  for i in range(size):
   if i%2==0:
    max_rat2.append(max_rat[i])
    min_rat2.append(min_rat[i])
    avg_rat2.append(avg_rat[i])
    if max_label < max_rat[i]:
     max_label = max_rat[i]
  plt.plot(range(init_nodes,init_nodes+size,2), max_rat2, 'r--', range(init_nodes,init_nodes+size,2), avg_rat2, 'bs', range(init_nodes,init_nodes+size,2), min_rat2, 'g^')
  plt.xlabel('Number of vertices', fontsize=20)
  plt.ylabel('Ratio', fontsize=20)
  #plt.ylim(1,max_label)
  #plt.ylim(.94,1.8)
  #plt.ylim(.94,1.45)
  if name_of_graph_class[cl]=='GE':
   plt.ylim(.94,4.2)
  else:
   plt.ylim(.94,1.6)
  plt.legend(['max', 'avg', 'min'], loc='upper right', fontsize=16)
  plt.tick_params(axis='x', labelsize=16)
  plt.tick_params(axis='y', labelsize=16)
  plt.show()
  plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_NVR_'+heuristic_names[heu]+'.png', bbox_inches='tight')
  plt.close()
init_levels = 2
size = len(number_of_levels)
#print(size)
for cl in range(len(name_of_graph_class)):
 for heu in range(len(heuristic_names)):
  max_rat = []
  min_rat = []
  avg_rat = []
  for i in range(size):
   max_rat.append(0)
   min_rat.append(10000)
   avg_rat.append(0)
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      cur_rat = float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k])
      if max_rat[i]<cur_rat:
       max_rat[i]=cur_rat
      if min_rat[i]>cur_rat:
       min_rat[i]=cur_rat
      avg_rat[i] = avg_rat[i] + cur_rat
  for i in range(size):
   avg_rat[i] = avg_rat[i]/(graphs_per_fixed_setup*(number_of_nodes_progression[0]-10)*len(node_distribution_in_levels))
  plt.figure(fig_count)
  fig_count = fig_count + 1
  plt.plot(range(init_levels,init_levels+size), max_rat, 'r--', range(init_levels,init_levels+size), avg_rat, 'bs', range(init_levels,init_levels+size), min_rat, 'g^')
  plt.xlabel('Levels')
  plt.ylabel('ratio')
  plt.show()
  plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR_'+heuristic_names[heu]+'.png')
  plt.close()
init_levels = 2
size = len(number_of_levels)
#print(size)
for cl in range(len(name_of_graph_class)):
 max_rat = []
 min_rat = []
 avg_rat = []
 for heu in range(len(heuristic_names)):
  max_rat.append([])
  min_rat.append([])
  avg_rat.append([])
  for i in range(size):
   max_rat[heu].append(0)
   min_rat[heu].append(10000)
   avg_rat[heu].append(0)
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      cur_rat = float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k])
      if max_rat[heu][i]<cur_rat:
       max_rat[heu][i]=cur_rat
      if min_rat[heu][i]>cur_rat:
       min_rat[heu][i]=cur_rat
      avg_rat[heu][i] = avg_rat[heu][i] + cur_rat
  for i in range(size):
   avg_rat[heu][i] = avg_rat[heu][i]/(graphs_per_fixed_setup*(number_of_nodes_progression[0]-10)*len(node_distribution_in_levels))
 min_rat_top_bottom = []
 min_rat_all = []
 for i in range(size):
  min_rat_top_bottom.append(min(avg_rat[0][i],avg_rat[1][i]))
  min_rat_all.append(min(avg_rat[0][i],avg_rat[1][i],avg_rat[2][i]))
 plt.figure(fig_count)
 fig_count = fig_count + 1
 plt.plot(range(init_levels,init_levels+size), min_rat_top_bottom, 'r--', label='min(top,bottom)')
 plt.plot(range(init_levels,init_levels+size), min_rat_all, 'bs', label='min of all')
 plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
 plt.xlabel('Levels')
 plt.ylabel('ratio')
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR'+'.png')
 plt.close()
init_levels = 2
size = len(number_of_levels)
for cl in range(len(name_of_graph_class)):
 for heu in range(len(heuristic_names)):
  data = []
  for i in range(size):
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      data[i].append(float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k]))
  plt.figure(fig_count)
  fig_count = fig_count + 1
  plt.boxplot(data, 0, '', whis=1000)
  plt.xticks(range(1,size+1), range(init_levels,init_levels+size))
  plt.xlabel('Levels')
  plt.ylabel('ratio')
  plt.show()
  plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR_'+heuristic_names[heu]+'_box.png')
  plt.close()
import matplotlib.patches as mpatches
init_levels = 2
size = len(number_of_levels)
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in range(len(heuristic_names)):
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      data[len(data)-1].append(float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k]))
  data.append([])
  for j in range(graphs_per_fixed_setup):
   for k in range(number_of_nodes_progression[0]-10):
    for nd in range(len(node_distribution_in_levels)):
     data[len(data)-1].append(min(data[len(data)-3][int(nd + k*len(node_distribution_in_levels) + j*(number_of_nodes_progression[0]-10)*len(node_distribution_in_levels))], data[len(data)-4][int(nd + k*len(node_distribution_in_levels) + j*(number_of_nodes_progression[0]-10)*len(node_distribution_in_levels))]))
  data.append([])
  for j in range(graphs_per_fixed_setup):
   for k in range(number_of_nodes_progression[0]-10):
    for nd in range(len(node_distribution_in_levels)):
     data[len(data)-1].append(min(data[len(data)-3][int(nd + k*len(node_distribution_in_levels) + j*(number_of_nodes_progression[0]-10)*len(node_distribution_in_levels))], data[len(data)-2][int(nd + k*len(node_distribution_in_levels) + j*(number_of_nodes_progression[0]-10)*len(node_distribution_in_levels))]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'yellow', 'cyan', 'violet', 'orange']
 text = ['BU', 'TD', 'HY', 'QoS', 'min(BU, TD)', 'min(BU, TD, HY)']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 plt.legend(handles=handles)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = init_levels
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==2:
   tmp2.append(cur_lab)
   cur_lab = cur_lab + 1
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 plt.xlabel('Levels')
 plt.ylabel('ratio')
 plt.ylim(.94,1.8)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR_box.png')
 plt.close()
init_levels = 2
size = len(number_of_levels)
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in heuristics4:
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      if steiner_scores_h[cl][0][i][nd][j][heu][k]==-1:
       continue
      data[len(data)-1].append(float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green']
 text = ['TOP', 'CMP', 'CMP(Q'+r'$^*$'+')']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 plt.legend(handles=handles, fontsize=16)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = init_levels
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==1:
   tmp2.append(cur_lab)
   cur_lab = cur_lab + 1
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 plt.xlabel('Levels', fontsize=25)
 plt.ylabel('Ratio', fontsize=25)
 plt.ylim(.94,1.8)
 plt.tick_params(axis='x', labelsize=16)
 plt.tick_params(axis='y', labelsize=16)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR_box_part4.png', bbox_inches='tight')
 plt.close()
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in heuristics1:
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      if steiner_scores_h[cl][0][i][nd][j][heu][k]==-1:
       continue
      data[len(data)-1].append(float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green']
 text = ['BOT', 'TOP', 'CMP']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 plt.legend(handles=handles, fontsize=16)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = init_levels
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==1:
   tmp2.append(cur_lab)
   cur_lab = cur_lab + 1
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 plt.xlabel('Levels', fontsize=25)
 plt.ylabel('Ratio', fontsize=25)
 plt.ylim(.94,1.8)
 plt.tick_params(axis='x', labelsize=16)
 plt.tick_params(axis='y', labelsize=16)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR_box_part1.png', bbox_inches='tight')
 plt.close()
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in range(len(heuristic_names)):
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      if steiner_scores_h[cl][0][i][nd][j][heu][k]==-1:
       continue
      tmp = float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k])
      if tmp < 1.0:
       data[len(data)-1].append(1.0)
      else:
       data[len(data)-1].append(tmp)
      #data[len(data)-1].append(float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green', 'cyan', 'violet', 'orange']
 text = ['BOT', 'TOP', 'HY', 'QoS', 'CMP', 'CMP(Q'+r'$^*$'+')']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 plt.legend(handles=handles)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = init_levels
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==2:
   tmp2.append(cur_lab)
   cur_lab = cur_lab + 1
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 plt.xlabel('Levels', fontsize=20)
 plt.ylabel('ratio', fontsize=20)
 plt.ylim(.94,1.8)
 plt.tick_params(axis='x', labelsize=16)
 plt.tick_params(axis='y', labelsize=16)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR_box_part2.png', bbox_inches='tight')
 plt.close()
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in heuristics3:
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for nd in range(len(node_distribution_in_levels)):
      if steiner_scores_h[cl][0][i][nd][j][heu][k]==-1:
       continue
      tmp = float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k])
      if tmp < 1.0:
       data[len(data)-1].append(1.0)
      else:
       data[len(data)-1].append(tmp)
      #data[len(data)-1].append(float(steiner_scores_h[cl][0][i][nd][j][heu][k])*1.0/float(steiner_scores[cl][0][i][nd][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green', 'cyan']
 text = ['BOT', 'TOP', 'CMP', 'CMP(Q'+r'$^*$'+')']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 plt.legend(handles=handles)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = init_levels
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==2:
   tmp2.append(cur_lab)
   cur_lab = cur_lab + 1
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 plt.xlabel('Levels', fontsize=20)
 plt.ylabel('Ratio', fontsize=20)
 plt.ylim(.94,4.2)
 plt.tick_params(axis='x', labelsize=16)
 plt.tick_params(axis='y', labelsize=16)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_LVR_box_part3.png', bbox_inches='tight')
 plt.close()
size = len(node_distribution_in_levels)
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in range(len(heuristic_names)):
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for l in range(len(number_of_levels)):
      data[len(data)-1].append(float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k]))
  data.append([])
  for j in range(graphs_per_fixed_setup):
   for k in range(number_of_nodes_progression[0]-10):
    for l in range(len(number_of_levels)):
     data[len(data)-1].append(min(data[len(data)-4][int(l + k*len(number_of_levels) + j*(number_of_nodes_progression[0]-10)*len(number_of_levels))], data[len(data)-5][int(l + k*len(number_of_levels) + j*(number_of_nodes_progression[0]-10)*len(number_of_levels))]))
  data.append([])
  for j in range(graphs_per_fixed_setup):
   for k in range(number_of_nodes_progression[0]-10):
    for l in range(len(number_of_levels)):
     data[len(data)-1].append(min(data[len(data)-4][int(l + k*len(number_of_levels) + j*(number_of_nodes_progression[0]-10)*len(number_of_levels))], data[len(data)-2][int(l + k*len(number_of_levels) + j*(number_of_nodes_progression[0]-10)*len(number_of_levels))]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'yellow', 'cyan', 'violet', 'orange']
 text = ['BU', 'TD', 'HY', 'QoS', 'min(BU, TD)', 'min(BU, TD, HY)']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 if cl==3:
  plt.legend(handles=handles, loc='upper left')
 else:
  plt.legend(handles=handles)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = 'Linear'
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==2: 
   tmp2.append(cur_lab)
   cur_lab = 'Exponential'
  else:
   tmp2.append('') 
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 plt.xlabel('Node distribution in levels')
 plt.ylabel('ratio')
 plt.ylim(.94,1.8)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_NDVR_box.png')
 plt.close()
size = len(node_distribution_in_levels)
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in heuristics4:
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for l in range(len(number_of_levels)):
      if steiner_scores_h[cl][0][l][i][j][heu][k]==-1:
       continue
      tmp = float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k])
      if tmp < 1.0:
       data[len(data)-1].append(1.0)
      else:
       data[len(data)-1].append(tmp)
      #data[len(data)-1].append(float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green']
 text = ['TOP', 'CMP', 'CMP(Q'+r'$^*$'+')']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 if cl==3:
  plt.legend(handles=handles, loc='upper left', fontsize=16)
 else:
  plt.legend(handles=handles, fontsize=16)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = 'Linear'
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==1:
   tmp2.append(cur_lab)
   cur_lab = 'Exponential'
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 #plt.xlabel('Node distribution in levels', fontsize=25)
 plt.ylabel('Ratio', fontsize=25)
 plt.ylim(.94,1.8)
 plt.tick_params(axis='x', labelsize=25)
 plt.tick_params(axis='y', labelsize=16)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_NDVR_box_part4.png', bbox_inches='tight')
 plt.close()
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in heuristics1:
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for l in range(len(number_of_levels)):
      if steiner_scores_h[cl][0][l][i][j][heu][k]==-1:
       continue
      tmp = float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k])
      if tmp < 1.0:
       data[len(data)-1].append(1.0)
      else:
       data[len(data)-1].append(tmp)
      #data[len(data)-1].append(float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green']
 text = ['BOT', 'TOP', 'CMP']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 if cl==3:
  plt.legend(handles=handles, loc='upper left', fontsize=16)
 else:
  plt.legend(handles=handles, fontsize=16)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = 'Linear'
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==1:
   tmp2.append(cur_lab)
   cur_lab = 'Exponential'
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 #plt.xlabel('Node distribution in levels', fontsize=25)
 plt.ylabel('Ratio', fontsize=25)
 plt.ylim(.94,1.8)
 plt.tick_params(axis='x', labelsize=25)
 plt.tick_params(axis='y', labelsize=16)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_NDVR_box_part1.png', bbox_inches='tight')
 plt.close()
size = len(node_distribution_in_levels)
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in range(len(heuristic_names)):
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for l in range(len(number_of_levels)):
      if steiner_scores_h[cl][0][l][i][j][heu][k]==-1:
       continue
      tmp = float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k])
      if tmp < 1.0:
       data[len(data)-1].append(1.0)
      else:
       data[len(data)-1].append(tmp)
      #data[len(data)-1].append(float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green', 'cyan', 'violet', 'orange']
 text = ['BOT', 'TOP', 'HY', 'QoS', 'CMP', 'CMP(Q'+r'$^*$'+')']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 if cl==3:
  plt.legend(handles=handles, loc='upper left')
 else:
  plt.legend(handles=handles)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = 'Linear'
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==2:
   tmp2.append(cur_lab)
   cur_lab = 'Exponential'
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 plt.xlabel('Node distribution in levels', fontsize=20)
 plt.ylabel('ratio', fontsize=20)
 plt.tick_params(axis='x', labelsize=16)
 plt.tick_params(axis='y', labelsize=16)
 plt.ylim(.94,1.8)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_NDVR_box_part2.png', bbox_inches='tight')
 plt.close()
size = len(node_distribution_in_levels)
for cl in range(len(name_of_graph_class)):
 data = []
 for i in range(size):
  for heu in heuristics3:
   data.append([])
   for j in range(graphs_per_fixed_setup):
    for k in range(number_of_nodes_progression[0]-10):
     for l in range(len(number_of_levels)):
      if steiner_scores_h[cl][0][l][i][j][heu][k]==-1:
       continue
      tmp = float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k])
      if tmp < 1.0:
       data[len(data)-1].append(1.0)
      else:
       data[len(data)-1].append(tmp)
      #data[len(data)-1].append(float(steiner_scores_h[cl][0][l][i][j][heu][k])*1.0/float(steiner_scores[cl][0][l][i][j][k]))
  # add some gap
  if i < size - 1:
   data.append([])
   data.append([])
 plt.figure(fig_count)
 fig_count = fig_count + 1
 color = ['red', 'blue', 'green', 'cyan']
 text = ['BOT', 'TOP', 'CMP', 'CMP(Q'+r'$^*$'+')']
 bp = plt.boxplot(data, 0, '', whis=1000, patch_artist=True)
 i = 0
 for box in bp['boxes']:
  # change outline color
  # check whether it is a gap, if gap no need to color
  c_i = i%(len(text)+2)
  if c_i<len(text):
   box.set(color=color[c_i], linewidth=2)
  i = i + 1
  # change fill color
  #box.set(facecolor = 'green' )
  # change hatch
  #box.set(hatch = '/')
 handles = []
 for i in range(len(text)):
  patch = mpatches.Patch(color=color[i], label=text[i])
  handles.append(patch)
 if cl==3:
  plt.legend(handles=handles, loc='upper left')
 else:
  plt.legend(handles=handles)
 # labels computation is complex, it has add 2 for gaps, negate 2 for boundary condition 
 tmp = range(1,size*(len(text)+2)+1-2)
 tmp2 = []
 cur_lab = 'Linear'
 for i in range(len(tmp)):
  # Add 2 with len(text) because we want two gaps between groups of boxes
  if i%(len(text)+2)==1:
   tmp2.append(cur_lab)
   cur_lab = 'Exponential'
  else:
   tmp2.append('')
 #plt.title("BU, TD, HY, min(BU, TD), min(BU, TD, HY) for "+name_of_graph_class[cl])
 plt.xticks(tmp, tmp2)
 #plt.xlabel('Node distribution in levels', fontsize=20)
 plt.ylabel('Ratio', fontsize=20)
 plt.tick_params(axis='x', labelsize=25)
 plt.tick_params(axis='y', labelsize=16)
 plt.ylim(.94,4.2)
 plt.show()
 plt.savefig(path_to_plots_directory+name_of_graph_class[cl]+'_'+str(number_of_nodes_progression[0])+'_NDVR_box_part3.png', bbox_inches='tight')
 plt.close()
#quit()
# lp plots
import math

def lp_plots():
 global fig_count
 out_arr = []
 f = open('log_files_heuristics_lp/results.txt')
 for i in range(22):
  out_arr.append(float(f.readline()))
 f.close()
 plt.figure(fig_count)
 fig_count = fig_count + 1
 plt.plot(range(1,23), out_arr, 'bo', range(1,23), out_arr, 'k', range(1,23), [math.e]*22, 'r--', range(1,23), [2.45]*22, 'g--')
 plt.xlabel(r'Number of levels ($\ell$)', fontsize=16)
 plt.ylabel('Approximation ratio '+r'$(t/\rho)$', fontsize=16)
 plt.xticks(range(1,23,3))
 plt.show()
 plt.savefig(path_to_plots_directory+'LVR.png')
 plt.close()
 # lp plots
 plt.figure(fig_count)
 fig_count = fig_count + 1
 for i in range(1,23):
  out_arr = []
  f = open('log_files_heuristics_lp/S_'+str(i)+'.txt')
  #print('t = '+str(i))
  f.readline()
  den = 0
  for j in range(1,i+1):
   den = den + 1.0/math.factorial(j)
  for j in range(1,i+1):
   line = f.readline()
   t_arr = line.split(" ")
   out_arr.append(float(t_arr[len(t_arr)-1]))
   #print(out_arr[j-1])
   #print(1.0/(math.factorial(i-j+1)*den))
  f.close()
  plt.plot(range(1,i+1), out_arr)
 plt.xlabel('Level index')
 plt.ylabel('Worst case distribution of each level Steiner tree costs')
 plt.xticks(range(1,23,3))
 plt.show()
 plt.savefig(path_to_plots_directory+'VVV.png')
 plt.close()

lp_plots()

