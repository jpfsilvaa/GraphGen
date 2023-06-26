RANDOM=$$$(date +%s)
pathToSimulator=/home/jps/GraphGenFrw/Simulator
for i in {0..10}
do
    seed=$RANDOM
    python3 input_data_gen.py \
            20 \
            ${pathToSimulator}/GraphGen/BusMovementModel/raw_data/map_20171024.xml \
            newInst20_s${seed}.json \
            7 \
            ${pathToSimulator}/Simulator/GraphGen/BusMovementModel/raw_data/buses_20171024.xml
    echo 'Done for '${seed}' users and algorithm'
done