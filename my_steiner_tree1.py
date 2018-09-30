import sys
sys.path.append('/cm/shared/uaapps/cplex/12.6.2/cplex/python/2.6/x86-64_linux/')
import cplex
from cplex.exceptions import CplexError
import time

#take input
start_time = time.time()
output_file = sys.argv[2]
flow_type = sys.argv[3]
variable_count_file = sys.argv[4]
time_file = sys.argv[5]
constraint_count_file = sys.argv[6]
file = open(sys.argv[1],"r")
print "File name: "+sys.argv[1]
#print "Number of edges:"
#m = int(raw_input())
m = int(file.readline())
#print "Edge list (u v w, u,v>0):"
edge_list = list()
for i in range(m):
    #edge_list.append([int(x) for x in raw_input().split()])
    #edge_list.append([int(x) for x in file.readline().split()])
    t_arr1 = []
    t_arr2 = file.readline().split()
    t_arr1.append(int(t_arr2[0]))
    t_arr1.append(int(t_arr2[1]))
    t_arr1.append(float(t_arr2[2]))
    edge_list.append(t_arr1)

n = max(max(u, v) for [u, v, w] in edge_list) # Get size of matrix
matrix = [[0] * n for i in range(n)]

for [u, v, w] in edge_list:
    #matrix[u-1][v-1] = w
    matrix[u-1][v-1] = matrix[v-1][u-1] = w

#for row in matrix:
#    print(row)
#print "Number of levels:"
levels = int(file.readline())
tree_ver=[]
#tree_ver = [(int(x)-1) for x in raw_input().split()]
for l in range(levels):
    #print "Steiner tree vertices of level "+str(l+1)+":"
    tree_ver.append([(int(x)-1) for x in file.readline().split()])
file.close()

total_columns = 0
get_column = dict()
my_obj = list()
my_colnames = list()
edge_list_dict = dict()

# flow_types: multi commodity (0), signle commodity (1) and single level signle commodity (2)
if flow_type == "0":
    for l in range(levels):
        for i in range(n):
            for j in range(n):
                if matrix[i][j]>0:
                    my_obj.append(matrix[i][j])
                    #e_i_j -> y_{ij}
                    var_name = "e_"+str(i)+"_"+str(j)+"_"+str(l)
                    #print var_name
                    edge_list_dict[var_name] = [i,j]
                    my_colnames.append(var_name)
                    get_column[var_name] = total_columns
                    total_columns = total_columns + 1
                    for k in range(1,len(tree_ver[l])):
                        my_obj.append(0)
                        var_name = "x_"+str(i)+"_"+str(j)+"_"+str(k)+"_"+str(l)
                        my_colnames.append(var_name)
                        get_column[var_name] = total_columns
                        total_columns = total_columns + 1
elif flow_type == "1":
    for l in range(levels):
        for i in range(n):
            for j in range(n):
                if matrix[i][j]>0:
                    my_obj.append(matrix[i][j])
                    #e_i_j -> y_{ij}
                    var_name = "e_"+str(i)+"_"+str(j)+"_"+str(l)
                    #print var_name
                    edge_list_dict[var_name] = [i,j]
                    my_colnames.append(var_name)
                    get_column[var_name] = total_columns
                    total_columns = total_columns + 1

                    # we do not need to loop over all tree vertices
                    my_obj.append(0)
                    var_name = "x_"+str(i)+"_"+str(j)+"_"+str(l)
                    my_colnames.append(var_name)
                    get_column[var_name] = total_columns
                    total_columns = total_columns + 1
elif flow_type == "2":
    for i in range(n):
        for j in range(n):
            if matrix[i][j]>0:
                my_obj.append(matrix[i][j])
                var_name = "e_"+str(i)+"_"+str(j)
                edge_list_dict[var_name] = [i,j]
                my_colnames.append(var_name)
                get_column[var_name] = total_columns
                total_columns = total_columns + 1

                my_obj.append(0)
                var_name = "x_"+str(i)+"_"+str(j)
                my_colnames.append(var_name)
                get_column[var_name] = total_columns
                total_columns = total_columns + 1


#print "objective:"
#print my_obj

# find max flow possible
max_ub = -levels
for l in range(levels):
    #max_ub = max_ub + (levels - (l+1) + 1)*len(tree_ver[l])
    max_ub = max_ub + len(tree_ver[l])

my_ub = list()
my_lb = list()
my_ctype = ""
if flow_type == "0":
    for i in range(len(my_obj)):
        my_ub.append(1)
        my_lb.append(0)
        my_ctype = my_ctype + "I"
elif flow_type == "1":
    #test
    my_ctype = list()
    for i in range(len(my_obj)):
        if my_colnames[i][0]=='x':
            #find level
            l = int(my_colnames[i].split('_')[len(my_colnames[i].split('_'))-1])
            my_ub.append(len(tree_ver[l])-1)
            #test
            my_ctype.append(cplex.Cplex().variables.type.continuous)
        else:
            my_ub.append(1)
            #test
            my_ctype.append(cplex.Cplex().variables.type.integer) 
        my_lb.append(0)
        #test
        #my_ctype = my_ctype + "I"
elif flow_type == "2":
    my_ctype = list()
    for i in range(len(my_obj)):
        if my_colnames[i][0]=='x':
            my_ub.append(max_ub)
            my_ctype.append(cplex.Cplex().variables.type.continuous)
        else:
            my_ub.append(1)
            my_ctype.append(cplex.Cplex().variables.type.integer)
        my_lb.append(0)

#my_obj = [4.0, 8.0, 8.0, 11.0, 7.0, 4.0, 2.0, 9.0, 14.0, 10.0, 2.0, 1.0, 6.0, 7.0]
#my_ub = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#my_lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#my_ctype = "IIIIIIIIIIIIII"
#my_colnames = ["xab", "xah", "xbc", "xbh", "xcd", "xcf", "xci", "xde", "xdf", "xef", "xfg", "xgh", "xgi", "xhi"]

#write code for rows, one row for every steiner tree node
my_rhs = list()
my_rownames = list()
my_sense = ""
rows = list()
cols = list()
vals = list()
total_rows = 0

def find_top_level(v):
    for l in range(levels):
        if v in tree_ver[l][1:len(tree_ver[l])]:
            return l
    return -1

if flow_type == "0":
    for l in range(levels):
        for k in range(1,len(tree_ver[l])):
            for i in range(n):
                if i==tree_ver[l][0]:
                    my_rhs.append(1)
                #elif i in tree_ver:
                elif i==tree_ver[l][k]:
                    my_rhs.append(-1)
                else:
                    my_rhs.append(0)
                # row count should be modified: there may be same i for multiple tree vertices!!!!!!!!
                #my_rownames.append("r"+str(i))
                my_rownames.append("r_"+str(total_rows))
                my_sense = my_sense + "E"
                for j in range(n):
                    if matrix[i][j]>0:
                        rows.append(total_rows)
                        #rows.append(i)
                        cols.append(get_column["x_"+str(i)+"_"+str(j)+"_"+str(k)+"_"+str(l)])
                        vals.append(1)
                    if matrix[j][i]>0:
                        rows.append(total_rows)
                        #rows.append(i)
                        cols.append(get_column["x_"+str(j)+"_"+str(i)+"_"+str(k)+"_"+str(l)])
                        vals.append(-1)
                total_rows = total_rows + 1
            for i in range(n):
                for j in range(n):
                    if matrix[i][j]>0:
                        #my_rhs.append(1)
                        my_rhs.append(0)
                        my_rownames.append("r_"+str(total_rows))
                        my_sense = my_sense + "L"
                        rows.append(total_rows)
                        cols.append(get_column["x_"+str(i)+"_"+str(j)+"_"+str(k)+"_"+str(l)])
                        vals.append(1)
                        rows.append(total_rows)
                        cols.append(get_column["e_"+str(i)+"_"+str(j)+"_"+str(l)])
                        vals.append(-1)
                        total_rows = total_rows + 1
        if l>0:
            for i in range(n):
                for j in range(n):
                    if matrix[i][j]>0:
                        my_rhs.append(0)
                        my_rownames.append("r_"+str(total_rows))
                        my_sense = my_sense + "L"
                        rows.append(total_rows)
                        cols.append(get_column["e_"+str(i)+"_"+str(j)+"_"+str(l-1)])
                        vals.append(1)
                        rows.append(total_rows)
                        cols.append(get_column["e_"+str(i)+"_"+str(j)+"_"+str(l)])
                        vals.append(-1)
                        total_rows = total_rows + 1
elif flow_type == "1":
    for l in range(levels):
        # we do not need to loop over all tree vertices
        for i in range(n):
            if i==tree_ver[l][0]:
                my_rhs.append(len(tree_ver[l])-1)
            #elif i in tree_ver:
            elif i in tree_ver[l][1:len(tree_ver[l])]:
                my_rhs.append(-1)
            else:
                my_rhs.append(0)
            # row count should be modified: there may be same i for multiple tree vertices!!!!!!!!
            #my_rownames.append("r"+str(i))
            my_rownames.append("r_"+str(total_rows))
            my_sense = my_sense + "E"
            for j in range(n):
                if matrix[i][j]>0:
                    rows.append(total_rows)
                    #rows.append(i)
                    cols.append(get_column["x_"+str(i)+"_"+str(j)+"_"+str(l)])
                    vals.append(1)
                if matrix[j][i]>0:
                    rows.append(total_rows)
                    #rows.append(i)
                    cols.append(get_column["x_"+str(j)+"_"+str(i)+"_"+str(l)])
                    vals.append(-1)
            total_rows = total_rows + 1
        for i in range(n):
            for j in range(n):
                if matrix[i][j]>0:
                    #my_rhs.append(1)
                    my_rhs.append(0)
                    my_rownames.append("r_"+str(total_rows))
                    my_sense = my_sense + "L"
                    rows.append(total_rows)
                    cols.append(get_column["x_"+str(i)+"_"+str(j)+"_"+str(l)])
                    vals.append(1)
                    rows.append(total_rows)
                    cols.append(get_column["e_"+str(i)+"_"+str(j)+"_"+str(l)])
                    vals.append(-(len(tree_ver[l])-1))
                    total_rows = total_rows + 1
        if l>0:
            for i in range(n):
                for j in range(n):
                    if matrix[i][j]>0:
                        my_rhs.append(0)
                        my_rownames.append("r_"+str(total_rows))
                        my_sense = my_sense + "L"
                        rows.append(total_rows)
                        cols.append(get_column["e_"+str(i)+"_"+str(j)+"_"+str(l-1)])
                        vals.append(1)
                        rows.append(total_rows)
                        cols.append(get_column["e_"+str(i)+"_"+str(j)+"_"+str(l)])
                        vals.append(-1)
                        total_rows = total_rows + 1
elif flow_type == "2":
    for i in range(n):
        if i==tree_ver[0][0]:
            my_rhs.append(max_ub)
        elif find_top_level(i)!=-1:
            top_level = find_top_level(i)
            my_rhs.append(-(levels - (top_level+1) + 1))
        else:
            my_rhs.append(0)
        my_rownames.append("r_"+str(total_rows))
        my_sense = my_sense + "E"
        for j in range(n):
            if matrix[i][j]>0:
                rows.append(total_rows)
                #rows.append(i)
                cols.append(get_column["x_"+str(i)+"_"+str(j)])
                vals.append(1)
            if matrix[j][i]>0:
                rows.append(total_rows)
                #rows.append(i)
                cols.append(get_column["x_"+str(j)+"_"+str(i)])
                vals.append(-1)
        total_rows = total_rows + 1
    # need to work on this!!
    for i in range(n):
        for j in range(n):
            if matrix[i][j]>0:
                #my_rhs.append(1)
                my_rhs.append(0)
                my_rownames.append("r_"+str(total_rows))
                my_sense = my_sense + "L"
                rows.append(total_rows)
                cols.append(get_column["x_"+str(i)+"_"+str(j)])
                vals.append(1)
                rows.append(total_rows)
                cols.append(get_column["e_"+str(i)+"_"+str(j)])
                vals.append(-max_ub)
                total_rows = total_rows + 1

#my_rhs = [3, 2, 2, 2, 2]
#my_rownames = ["c1", "c2", "c3", "c4", "c5"]
#my_sense = "ELLLL"

#print "Number of edges:"
#print m
#print "edge_list:"
#print edge_list
#print "Number of vertices:"
#print n
#print "matrix:"
#print matrix
#print "levels:"
#print levels
#print "tree_ver"
#print tree_ver
#print "total_columns"
#print total_columns
#print "get_column:"
#print get_column
#print "Objective:"
#print my_obj
#print "Column names:"
#print my_colnames
#print "upper bound:"
#print my_ub
#print "lower bound:"
#print my_lb
#print "column type:"
#print my_ctype
#print "row names:"
#print my_rownames
#print "row values:"
#print my_rhs
#print "Sense:"
#print my_sense
#print "rows:"
#print rows
#print "cols:"
#print cols
#print "values:"
#print vals
#print "total_rows:"
#print total_rows
#print "******************************************"


try:
 prob = cplex.Cplex()
 prob.objective.set_sense(prob.objective.sense.minimize)
 prob.linear_constraints.add(rhs = my_rhs, senses = my_sense, names = my_rownames)
 prob.variables.add(obj = my_obj, ub = my_ub, lb = my_lb, types=my_ctype, names = my_colnames)

 name_indices = [i for i in range(len(my_obj))]
 names = prob.variables.get_names(name_indices)

 #rows = [0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4]
 #cols = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5]
 #vals = [1,1,1,1,1,1,1,1,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0]

 prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
 prob.write("model.lp")
 prob.solve()
except CplexError, exc:
 print exc


print "Solution value  = ", prob.solution.get_objective_value()
file = open(output_file,"a")
file.write(str(prob.solution.get_objective_value()))
file.close()
file = open(variable_count_file,"a")
file.write(str(total_columns))
file.close()
file = open(time_file,"a")
file.write(str(time.time() - start_time))
file.close()
file = open(constraint_count_file,"a")
file.write(str(total_rows))
file.close()
numcols = prob.variables.get_num()
x = prob.solution.get_values()
for j in range(numcols):
 print("Column %s:  Value = %10f" % (names[j], x[j]))

#print("For graphviz app:")
#for l in range(levels):
#    print("level "+str(l+1)+":")
#    for j in range(numcols):
#        if names[j][0]=='e':
#            if int(names[j].split('_')[len(names[j].split('_'))-1])==l:
#                if x[j] == 1:
#                    print(str(edge_list_dict[names[j]][0]+1) + " " + str(edge_list_dict[names[j]][1]+1))
#print("For canvas app:")

def compute_cost(adj_mat):
 total = 0
 for i in range(len(adj_mat)):
  for j in range(len(adj_mat[0])):
   if adj_mat[i][j]!=0:
    total = total + adj_mat[i][j]
 return total


def prune_terminals(adj_mat, ver_list):
 return 0

if flow_type == "0" or flow_type == "1":
    for l in range(levels):
        print("level "+str(l+1)+":")
        for j in range(numcols):
            if names[j][0]=='e':
                if int(names[j].split('_')[len(names[j].split('_'))-1])==l:
                    if x[j] == 1:
                        print(str(edge_list_dict[names[j]][0]) + " " + str(edge_list_dict[names[j]][1]))
elif flow_type == "2":
    bottom_layer_soln = [[0] * n for i in range(n)]
    soln_edges = []
    for j in range(numcols):
        if names[j][0]=='e':
            if x[j] == 1:
                u = edge_list_dict[names[j]][0]
                v = edge_list_dict[names[j]][1]
                bottom_layer_soln[u][v] = matrix[u][v]
                soln_edges.append((u, v))
    total_value = 0
    for l in range(levels-1, -1, -1):
        total_value = total_value + compute_cost(bottom_layer_soln)
        prune_terminals(bottom_layer_soln, tree_ver[l])
    print('cost: '+str(total_value))

