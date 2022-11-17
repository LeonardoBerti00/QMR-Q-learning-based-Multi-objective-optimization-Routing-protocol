#-----------------------------------------------------------#
#           _  _ ___  ___  ___  _  _ ___ ___                #
#          | \| |   \| _ \/ _ \| \| | __/ __|               #
#          | .` | |) |   / (_) | .` | _|\__ \               #
#          |_|\_|___/|_|_\\___/|_|\_|___|___/               #
#                                                           #
#-----------------------------------------------------------#


#test others algorithms
for nd in "2" "3";
do
    for alg in "GEO" "RND" "QL";
    do
        echo "run: ${alg} - ndrones ${nd} "
        python -m src.experiments.experiment_ndrones -nd ${nd} -i_s 0 -e_s 1 -alg ${alg} &
        python -m src.experiments.experiment_ndrones -nd ${nd} -i_s 1 -e_s 2 -alg ${alg} &
        python -m src.experiments.experiment_ndrones -nd ${nd} -i_s 2 -e_s 3 -alg ${alg} &
    done;
done;
wait


