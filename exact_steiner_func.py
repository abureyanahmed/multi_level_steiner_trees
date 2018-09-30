import networkx as nx
import sys
sys.path.append('/cm/shared/uaapps/cplex/12.7.1/cplex/python/3.5/x86-64_linux/')
import cplex
from cplex.exceptions import CplexError
import time


def compute_cost(adj_mat):
    total = 0
    for i in range(len(adj_mat)):
        for j in range(len(adj_mat[0])):
            if adj_mat[i][j]!=0:
                total = total + adj_mat[i][j]
    return total


def prune_terminals(adj_mat, ver_list):
    return 0

def build_networkx_graph(filename):
 G=nx.Graph()
 file = open(filename,"r")
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
  TT = TT + (tree_ver[l2],)

 return G, TT


def build_networkx_graph_from_edges(edge_list, matrix):
 G=nx.Graph()
 for j in range(len(edge_list)):
  G.add_edge(edge_list[j][0], edge_list[j][1], weight=matrix[edge_list[j][0]][edge_list[j][1]])

 return G


def SteinerTree(G,T):
    #print(G.edges())
    #print(T)

    m = len(G.edges())
    edge_list = list()

    for (u,v,d) in G.edges(data='weight'):
        t_arr1 = []
        t_arr1.append(u+1)
        t_arr1.append(v+1)
        t_arr1.append(d)
        edge_list.append(t_arr1)

    n = max(max(u, v) for [u, v, w] in edge_list) # Get size of matrix
    matrix = [[0] * n for i in range(n)]
    bin_matrix = [[0] * n for i in range(n)]

    for [u, v, w] in edge_list:
        #matrix[u-1][v-1] = w
        matrix[u-1][v-1] = matrix[v-1][u-1] = w
        bin_matrix[u-1][v-1] = bin_matrix[v-1][u-1] = 1

    levels = 1
    tree_ver=[]
    #tree_ver = [(int(x)-1) for x in raw_input().split()]
    tree_ver.append(T)

    total_columns = 0
    get_column = dict()
    my_obj = list()
    my_colnames = list()
    edge_list_dict = dict()

    def find_top_level(v):
        for l in range(levels):
            if v in tree_ver[l][1:len(tree_ver[l])]:
                return l
        return -1

    for i in range(n):
        for j in range(n):
            #if matrix[i][j]>0:
            if matrix[i][j]>=0 and bin_matrix[i][j]>0:
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

    # find max flow possible
    max_ub = -levels
    for l in range(levels):
        #max_ub = max_ub + (levels - (l+1) + 1)*len(tree_ver[l])
        max_ub = max_ub + len(tree_ver[l])

    my_ub = list()
    my_lb = list()
    my_ctype = list()
    for i in range(len(my_obj)):
        if my_colnames[i][0]=='x':
            my_ub.append(max_ub)
            my_ctype.append(cplex.Cplex().variables.type.continuous)
        else:
            my_ub.append(1)
            my_ctype.append(cplex.Cplex().variables.type.integer)
        my_lb.append(0)

    #write code for rows, one row for every steiner tree node
    my_rhs = list()
    my_rownames = list()
    my_sense = ""
    rows = list()
    cols = list()
    vals = list()
    total_rows = 0

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
            #if matrix[i][j]>0:
            if matrix[i][j]>=0 and bin_matrix[i][j]>0:
                rows.append(total_rows)
                #rows.append(i)
                cols.append(get_column["x_"+str(i)+"_"+str(j)])
                vals.append(1)
            #if matrix[j][i]>0:
            if matrix[j][i]>=0 and bin_matrix[j][i]>0:
                rows.append(total_rows)
                #rows.append(i)
                cols.append(get_column["x_"+str(j)+"_"+str(i)])
                vals.append(-1)
        total_rows = total_rows + 1
    # need to work on this!!
    for i in range(n):
        for j in range(n):
            #if matrix[i][j]>0:
            if matrix[i][j]>=0 and bin_matrix[i][j]>0:
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

    try:
        prob = cplex.Cplex()

        prob.set_log_stream(None)
        prob.set_error_stream(None)
        prob.set_warning_stream(None)
        prob.set_results_stream(None)

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
    except CplexError as exc:
        print(exc)


    #print("Solution value  = ", prob.solution.get_objective_value())
    numcols = prob.variables.get_num()
    x = prob.solution.get_values()
    #for j in range(numcols):
    #    print("Column %s:  Value = %10f" % (names[j], x[j]))

    bottom_layer_soln = [[0] * n for i in range(n)]
    soln_edges = []
    for j in range(numcols):
        if names[j][0]=='e':
            #if x[j] == 1:
            if x[j] > 0:
                u = edge_list_dict[names[j]][0]
                v = edge_list_dict[names[j]][1]
                bottom_layer_soln[u][v] = matrix[u][v]
                soln_edges.append((u, v))
    total_value = 0
    for l in range(levels-1, -1, -1):
        total_value = total_value + compute_cost(bottom_layer_soln)
        prune_terminals(bottom_layer_soln, tree_ver[l])
    #print('cost: '+str(total_value))
    return build_networkx_graph_from_edges(soln_edges, matrix)

#G, TT = build_networkx_graph('Graph_generator/experiment3/ER_100_2_L_0/graph_1.txt')
#G, TT = build_networkx_graph('Graph_generator/experiment3/WS_100_2_L_0/graph_22.txt')
#print(TT[0])
#G_res = SteinerTree(G,TT[0])
#print(G_res.edges())


