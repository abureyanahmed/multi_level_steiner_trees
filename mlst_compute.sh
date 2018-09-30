###===================
#!/bin/bash
#PBS -l select=1:ncpus=28:mem=168gb:pcmem=6gb -l walltime=240:00:00
#PBS -l cput=6720:00:00
#PBS -q windfall
#PBS -W group_list=kobourov
###-------------------

echo "Node name:"
hostname

cd /extra/abureyanahmed
#rm -rf $GRAPH_FOLDER
#mkdir $GRAPH_FOLDER
#module load python/3/3.5.2
#python3 Graph_generator/graph_generator.py $NUMBER_OF_GRAPHS $NUMBER_OF_LEVELS $INITIAL_NUMBER_OF_NODES $GRAPH_FOLDER $CLASS_OF_GRAPH $PARAM1 $PARAM2 $NODE_DISTRIBUTION
tar -czvf $COMPRESSED_FILE my_steiner_tree1.py steiner_tree_mult_files.py $GRAPH_FOLDER

# put data in /tmp/
mkdir $TEMP_FOLDER_NAME
cp $COMPRESSED_FILE $TEMP_FOLDER_NAME
rm $COMPRESSED_FILE
cd $TEMP_FOLDER_NAME
tar -xvzf $COMPRESSED_FILE

module load cplex/12/12.6.2
python steiner_tree_mult_files.py $STEINER_SCORE_FILE_NAME $NUMBER_OF_GRAPHS $MODEL $PATTERN_OF_FILE_NAME $VARIABLE_FILE_NAME $TIME_FILE_NAME $CONSTRAINTS_FILE_NAME $MINIMUM_GRAPH_INDEX
cp $STEINER_SCORE_FILE_NAME /extra/abureyanahmed/
cp $VARIABLE_FILE_NAME /extra/abureyanahmed/
cp $TIME_FILE_NAME /extra/abureyanahmed/
cp $CONSTRAINTS_FILE_NAME /extra/abureyanahmed/

# clean up
rm -rf $TEMP_FOLDER_NAME
