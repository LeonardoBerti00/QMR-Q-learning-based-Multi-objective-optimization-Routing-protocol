#-----------------------------------------------------------#
#           _  _ ___  ___  ___  _  _ ___ ___                #
#          | \| |   \| _ \/ _ \| \| | __/ __|               #
#          | .` | |) |   / (_) | .` | _|\__ \               #
#          |_|\_|___/|_|_\\___/|_|\_|___|___/               #
#                                                           #
#-----------------------------------------------------------#
source ~/.zprofile

#test others algorithms
for nd in "5" "10" "15" "20" "25" "30";
do
    for alg in "GEO" "RND" "QL";
    do
        echo "run: ${alg} - ndrones ${nd} "
        python3.7.9 ../../main.py -nd ${nd} -i_s 0 -e_s 10 -alg ${alg} &
        python3.7.9 ../../main.py -nd ${nd} -i_s 10 -e_s 20 -alg ${alg} &
        python3.7.9 ../../main.py -nd ${nd} -i_s 20 -e_s 30 -alg ${alg} &
    done;
done;
wait


