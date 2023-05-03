seeds=(173 978 659 293 176 392 549 633 798 327 
        109 127 158 218 227 241 374 489 531 543 
        564 615 686 688 708 791 794 807 814 943 
        914 259 651 683 403 679 412 825 436 579 
        379 754 687 257 429 411 175 251 902 164)

for i in {0..49}
do
    fileNumber=$i
    python3 /home/jps/GraphGenFrw/Simulator/GraphGen/input_files/systemInput/input_data_gen.py \
    500 \
    /home/jps/GraphGenFrw/Simulator/GraphGen/BusMovementModel/raw_data/map_20171024.xml \
    /home/jps/GraphGenFrw/Simulator/GraphGen/input_files/systemInput/500users/inst_${fileNumber}.json \
    ${seeds[i]} \
    /home/jps/GraphGenFrw/Simulator/GraphGen/BusMovementModel/raw_data/buses_20171024.xml
done