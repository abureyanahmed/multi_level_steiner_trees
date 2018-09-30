###===================
#!/bin/bash
#PBS -l select=1:ncpus=28:mem=168gb:pcmem=6gb -l walltime=01:40:00
#PBS -l cput=48:00:00
#PBS -q standard
#PBS -W group_list=kobourov
###-------------------

echo "Node name:"
hostname

cd /extra/abureyanahmed
rm -rf $GRAPH_FOLDER
mkdir $GRAPH_FOLDER
module load python/3/3.5.2
python3 Graph_generator/graph_generator.py $NUMBER_OF_GRAPHS $NUMBER_OF_LEVELS $INITIAL_NUMBER_OF_NODES $PATTERN_OF_FILE_NAME $CLASS_OF_GRAPH $PARAM1 $PARAM2 $NODE_DISTRIBUTION
