from subprocess import call
import sys
if len(sys.argv) < 8:
	print("Usage: python steiner_tree_mult_files.py steiner_scores.js number_of_graphs model={single flow, multi-comodity flow} root={/Users/abureyanahmed/Desktop/testenv/venv/Graph\ generator/steiner_app} variables.js time.js constraints.js minimum_graph_index")
	quit()
file = open(sys.argv[1],"w")
file.write("var scores = [");
file.close()
file = open(sys.argv[5],"w")
file.write("var number_of_variables = [");
file.close()
file = open(sys.argv[6],"w")
file.write("var time = [");
file.close()
file = open(sys.argv[7],"w")
file.write("var number_of_constraints = [");
file.close()
#size=1
size=int(sys.argv[2])
min_index = int(sys.argv[8])
for i in range(min_index, size):
	#print(sys.argv[4]+str(i+1)+".txt")
	call(["python", "my_steiner_tree1.py", sys.argv[4]+str(i+1)+".txt", sys.argv[1], sys.argv[3], sys.argv[5], sys.argv[6], sys.argv[7]])
	if i<(size-1):
		file = open(sys.argv[1],"a")
		file.write(",")
		file.close()
		file = open(sys.argv[5],"a")
		file.write(",")
		file.close()
		file = open(sys.argv[6],"a")
		file.write(",")
		file.close()
		file = open(sys.argv[7],"a")
		file.write(",")
		file.close()
file = open(sys.argv[1],"a")
file.write("];\n")
file.close()
file = open(sys.argv[5],"a")
file.write("];\n")
file.close()
file = open(sys.argv[6],"a")
file.write("];\n")
file.close()
file = open(sys.argv[7],"a")
file.write("];\n")
file.close()
