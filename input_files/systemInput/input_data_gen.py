import json
import random
import sys
from itertools import product
import xml.etree.ElementTree as ET
import heapq
import cloudletPosGen as cpg

# NUMBER_BUS_TRACES = 10
# BUS_LINES_IDS = ['274P-10-0', '4112-10-0', '4113-10-0', '4114-10-0', '4115-10-0', 
#                  'N508-11-0', '209P-10-0', '407M-10-0', '177H-10-0', '748R-10-1', 
#                  '7282-10-0', '199D-10-0', '476G-41-0', '477A-10-0', '478P-10-0', 
#                  '5705-10-0', '574A-10-0', '874T-10-0', '107T-10-0', 'N537-11-0']

# BUS_LINES_IDS = ['106A-10-0', '107T-10-0', '609F-10-0', '701A-10-0', '701U-10-0',
#              '6403-10-0', '702C-10-0', '702U-10-0', '2127-10-0', '3390-10-0']

# BUS_LINES_IDS = ['609F-10-0', '701A-10-0', '702C-10-0', '8544-10-0', '3390-10-0',
#                  '509M-10-0', '5108-10-0', '5290-10-0', '5630-10-0', '179X-10-0']

# BUS_LINES_IDS = ['8594-10-0', '2290-10-0', '5318-10-0', '6291-10-0'] # Figure_100_2

# BUS_LINES_IDS = ['1177-31-0', '175T-10-0', '3390-10-0', '208V-10-0']

# BUS_LINES_IDS = ['7282-10-0', '199D-10-0', '847P-10-0', '8600-22-0'] # newInst100_f

# BUS_LINES_IDS = ['N236-11-0', '1775-10-0', '1018-10-0', '2020-10-0'] # newInst100_f2_

# BUS_LINES_IDS = ['118C-10-0', '1732-10-0', '178L-10-0', '271C-10-0'] # newInst100_f3_

# BUS_LINES_IDS = ['1018-10-0', '1775-10-0', '2740-10-0', '1722-10-0', '1760-10-0',
#              '148L-10-0', '148P-10-0', '1742-10-0', '118C-10-0', '9653-10-0']  # newInst250_f

# BUS_LINES_IDS = ['199D-10-0', '7272-10-0', '7725-10-0', '8400-10-0', '9050-10-0',
            #  '9181-10-0', '809N-10-0', '775A-10-0', '8019-10-0', '8026-10-0'] # newInst250_f2

# BUS_LINES_IDS = ['1785-10-0', '1786-10-0', '1787-10-0', '1018-10-0', '2020-10-0', '2740-10-0'] # newInst150_f

# longest lines: ['N331-11-0', '213C-31-1', '5194-10-0', '213C-10-1', 'N536-11-0', '213C-31-0', '213C-10-0', 'N533-11-0', '7282-10-0', '477P-10-0']

import xml.etree.ElementTree as ET

def find_intersections(bus_lines, k):
    intersections = set()

    for i in range(len(bus_lines)):
        for j in range(i + 1000, len(bus_lines)):
            stops_i = set(bus_lines[i]['stops'].split(','))
            stops_j = set(bus_lines[j]['stops'].split(','))
            if (len(stops_i) > 60) and (len(stops_j) > 60):
                common_stops = stops_i.intersection(stops_j)

                if common_stops:
                    intersections.add(bus_lines[i]['id'])
                    intersections.add(bus_lines[j]['id'])

                if len(intersections) >= k:
                    return intersections

    return intersections

def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    bus_lines = []

    for bus_elem in root.findall('.//bus'):
        bus_info = {
            'id': bus_elem.attrib['id'],
            'stops': bus_elem.attrib['stops']
        }
        bus_lines.append(bus_info)

    return bus_lines

def getKLargestLists(dictionary, k):
    heap = []
    for key, value in dictionary.items():
        length = len(value)
        if len(heap) < k:
            heapq.heappush(heap, (length, key, value))
        elif length > heap[0][0]:
            heapq.heappushpop(heap, (length, key, value))
    result = {item[1]: item[2] for item in heapq.nlargest(k, heap)}
    return result

def readBusTraces(inputFilePath, busLinesIds):
    tree = ET.parse(inputFilePath)
    root = tree.getroot()

    busTraces = {}
    chosenBusTraces = {}
    for child in root:
        if child.tag == 'bus':
            busId = child.attrib['id']
            busTrace = [i for i in child.attrib['stops'].split(',')]
        # if len(busTrace) > 60:
            # busTrace = busTrace[:60]
            busTraces[busId] = busTrace
    # chosen = random.sample(list(busTraces.keys()), NUMBER_BUS_TRACES)
    chosenBusTraces = {i: busTraces[i] for i in busLinesIds}
    return chosenBusTraces

def routeGen(busTrace):
    routeJumps = len(busTrace)
    route = []
    firstNode = random.randint(0, routeJumps // 4)
    lastNode = random.randint(3*(routeJumps // 4), routeJumps - 1)
    route.append(busTrace[firstNode])
    for i in range(firstNode + 1, lastNode):
        route.append(busTrace[i])
    route.append(busTrace[lastNode])
    return route

def vmGen(vmsQtt, busFilePath, busLinesIds):
    # units: storage(MB), cpu(MIPS), RAM(MB)
    VMs = []
    simMIPS = 2000
    busTraces = readBusTraces(busFilePath, busLinesIds)
    chosenBusTraces = {}

    for i in range(vmsQtt):
        chosenBus = random.choice(list(busTraces.keys()))
        chosenBusTraces[chosenBus] = busTraces[chosenBus]

        gp1 = {
            "vmType": 'gp1',
            "bid": random.gauss(100, 5),
            "v_storage": random.gauss(3 * 1024, 100),
            "v_CPU": random.gauss(2 * simMIPS, 100),
            "v_RAM": random.gauss(4 * 1024, 100)
        }

        gp2 = {
            "vmType": 'gp2',
            "bid": random.gauss(400, 5),
            "v_storage": random.gauss(16 * 1024, 100),
            "v_CPU": random.gauss(4 * simMIPS, 100),
            "v_RAM": random.gauss(16 * 1024, 100)
        }

        ramIntensive = {
            "vmType": 'ramIntensive',
            "bid": random.gauss(800, 10),
            "v_storage": random.gauss(16 * 1024, 100),
            "v_CPU": random.gauss(8 * simMIPS, 100),
            "v_RAM": random.gauss(64 * 1024, 100)
        }

        cpuIntensive = {
            "vmType": 'cpuIntensive',
            "bid": random.gauss(800, 10),
            "v_storage": random.gauss(16 * 1024, 100),
            "v_CPU": random.gauss(16 * simMIPS, 100),
            "v_RAM": random.gauss(32 * 1024, 100)
        }

        vmTypes = [gp1, gp2, ramIntensive, cpuIntensive]
        chosenVm = random.choice(vmTypes)

        vm = {
            "vId": 'v' + str(i), 
            "vmType": chosenVm["vmType"],
            "bid": int(chosenVm["bid"]),
            "avgSpeed": 16,
            "initialTime": 0,
            "route": busTraces[chosenBus] if i <= (vmsQtt/4) else routeGen(busTraces[chosenBus]),
            "busId": chosenBus,
            "v_storage": chosenVm["v_storage"], 
            "v_CPU": chosenVm["v_CPU"], 
            "v_RAM": chosenVm["v_RAM"]
        }

        VMs.append(vm)
    return VMs, chosenBusTraces

def cloudletGen(linksInputFilePath, chosenBusTraces, seed):
    cloudletsPositions = cpg.main(chosenBusTraces, seed)

    Cloudlets = []
    simMIPS = 2000

    for c in range(len(cloudletsPositions)):
        cloudlet = {
            "cId": 'c' + str(c),
            "position": [cloudletsPositions[c][0], cloudletsPositions[c][1]],
            "lineAndcolor": cloudletsPositions[c][2],
            "coverageRadius": 500,
            "c_storage": 144 * 1024, 
            "c_CPU": 112 * simMIPS,
            "c_RAM": 304 * 1024
        }
        Cloudlets.append(cloudlet)
    return Cloudlets

def build(args):
    vmsArg = int(args[0])
    linksFilePath = args[1]
    outFilePath = args[2]
    seed = args[3]
    busFilePath = args[4]

    random.seed(seed)
    bus_lines = parse_xml(busFilePath)
    k = 40
    intersections = find_intersections(bus_lines, k)

    BUS_LINES_IDS = list(intersections)

    vms, chosenBusTraces = vmGen(vmsArg, busFilePath, BUS_LINES_IDS)
    cloudlets = cloudletGen(linksFilePath, chosenBusTraces, seed)
    mainObject = {
                    "UserVMs": vms, 
                    "Cloudlets": cloudlets
                 }

    jsonString = json.dumps(mainObject, indent=4)
    jsonFile = open(outFilePath, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def validateArgs(args):
    if args:
        if args[0] and args[0]:
            return True
        else:
            return False
    else:
        return False

def main():
    args = sys.argv[1:]
    if validateArgs(args):
        build(args)

if __name__ == "__main__":
    main()

# python3 input_data_gen.py 1000 /home/jps/GraphGenFrw/Simulator/GraphGen/BusMovementModel/raw_data/map_20171024.xml newInst.json 11 /home/jps/GraphGenFrw/Simulator/GraphGen/BusMovementModel/raw_data/buses_20171024.xml