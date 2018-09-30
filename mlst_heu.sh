###===================
#!/bin/bash
#PBS -l select=1:ncpus=28:mem=168gb:pcmem=6gb -l walltime=02:00:00
#PBS -l cput=56:00:00
#PBS -q windfall
#PBS -W group_list=kobourov
###-------------------

echo "Node name:"
hostname
cd /extra/abureyanahmed
module load python/3.5/3.5.5
python3 mlst_heuristic.py $PATTERN_OF_FILE_NAME $PATH_TO_RESULT_FOLDER $STEINER_SCORE_FILE_NAME $NUMBER_OF_GRAPHS $MINIMUM_GRAPH_INDEX $HEURISTIC $TIME_FILE_NAME
