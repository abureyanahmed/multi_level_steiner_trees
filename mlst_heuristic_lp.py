import sys
sys.path.append('/cm/shared/uaapps/cplex/12.6.2/cplex/python/2.6/x86-64_linux/')
import cplex
from cplex.exceptions import CplexError
import time
import math
if len(sys.argv) < 3:
        print("Usage: python mlst_heuristic_lp.py k log_files_heuristics_lp")
        quit()

def gen_P(i):
 if i == 1:
  return [[1]]
 else:
  t_arr = gen_P(i-1)
  arr = []
  t = int(math.pow(2,i-2))
  for j in range(t):
   arr.append([])
   for k in range(1):
    arr[j].append(1)
   for k in range(i-1):
    arr[j].append(0)
  for j in range(t):
   arr.append([])
   for k in range(1):
    arr[t+j].append(0)
   for k in range(i-1):
    arr[t+j].append(t_arr[j][k])
  return arr

def add_mat(A,B):
 C = []
 for i in range(len(A)):
  C.append([])
  for j in range(len(A[0])):
   C[i].append(A[i][j]+B[i][j])
 return C

def gen_A(i):
 if i==1:
  return [[1]]
 else:
  t_A = gen_A(i-1)
  t_S = add_mat(t_A,gen_P(i-1))
  arr = []
  t = int(math.pow(2,i-2))
  for j in range(t):
   arr.append([])
   for k in range(1):
    arr[j].append(i)
   for k in range(i-1):
    arr[j].append(t_A[j][k])
  for j in range(t):
   arr.append([])
   for k in range(1):
    arr[t+j].append(0)
   for k in range(i-1):
    arr[t+j].append(t_S[j][k])
  return arr


def get_t(k):
 my_obj = list()
 my_sense = ""
 my_rownames = list()
 total_rows = 0
 my_colnames = list()
 total_columns = 0
 my_ub = list()
 my_lb = list()
 my_ctype = list()

 my_obj.append(1)

 my_ub.append(cplex.infinity)
 my_lb.append(0.0)
 #my_ctype.append(cplex.Cplex().variables.type.continuous)
 var_name = "t"
 my_colnames.append(var_name)
 total_columns = total_columns + 1
 for i in range(k):
  my_obj.append(0)
  my_ub.append(cplex.infinity)
  my_lb.append(0.0)
 # my_ctype.append(cplex.Cplex().variables.type.continuous)
  var_name = "s_"+str(i+1)
  my_colnames.append(var_name)
  total_columns = total_columns + 1

 my_rhs = list()
 rows = list()
 cols = list()
 vals = list()

 # Ak S >= t
 Ak = gen_A(k)
 for r in range(len(Ak)):
  my_rhs.append(0)
  my_sense = my_sense + "G"
  my_rownames.append("r_"+str(total_rows))

  rows.append(total_rows)
  cols.append(0)
  vals.append(-1)

  for c in range(k):
   rows.append(total_rows)
   cols.append(1+c)
   vals.append(Ak[r][c])

  total_rows = total_rows + 1

 # S1 >= 0, Sl >= Sl-1
 for i in range(k):
  my_rhs.append(0)
  my_sense = my_sense + "L"
  my_rownames.append("r_"+str(total_rows))

  if i!=0:
   rows.append(total_rows)
   cols.append(i)
   vals.append(1)

  rows.append(total_rows)
  cols.append(i+1)
  vals.append(-1)

  total_rows = total_rows + 1

 # sum Sl = 1
 my_rhs.append(1)
 my_sense = my_sense + "E"
 my_rownames.append("r_"+str(total_rows))

 for i in range(k):
  rows.append(total_rows)
  cols.append(i+1)
  vals.append(1)

 total_rows = total_rows + 1


 try:
  prob = cplex.Cplex()
  prob.objective.set_sense(prob.objective.sense.maximize)
  prob.linear_constraints.add(rhs = my_rhs, senses = my_sense, names = my_rownames)
 # prob.variables.add(obj = my_obj, ub = my_ub, lb = my_lb, types=my_ctype, names = my_colnames)
  prob.variables.add(obj = my_obj, ub = my_ub, lb = my_lb, names = my_colnames)

  name_indices = [i for i in range(len(my_obj))]
  names = prob.variables.get_names(name_indices)


  prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
  prob.write("model.lp")
  prob.solve()
  numcols = prob.variables.get_num()
  x = prob.solution.get_values()
  file = open(sys.argv[2]+"S_"+str(k)+".txt","w")
  for j in range(numcols):
   print("Column %s:  Value = %10f" % (names[j], x[j]))
   file.write("Column %s:  Value = %10f\n" % (names[j], x[j]));
  file.close()
  return prob.solution.get_objective_value()
 except CplexError, exc:
  print exc

file = open(sys.argv[2]+"results.txt","w")
file.close()

out_arr = []
for k in range(1,int(sys.argv[1])):
 out_arr.append(get_t(k))
 file = open(sys.argv[2]+"results.txt","a")
 file.write(str(out_arr[k-1])+"\n");
 file.close()
print(out_arr)



