import json
import random
import sys
from itertools import product
import xml.etree.ElementTree as ET
import heapq
import cloudletPosGen as cpg

NUMBER_BUS_TRACES = 4

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

def readBusTraces(inputFilePath):
    tree = ET.parse(inputFilePath)
    root = tree.getroot()

    busTraces = {}
    chosenBusTraces = {}
    for child in root:
        if child.tag == 'bus':
            busId = child.attrib['id']
            busTrace = [i for i in child.attrib['stops'].split(',')]
            busTraces[busId] = busTrace
    chosen = random.sample(list(busTraces.keys()), NUMBER_BUS_TRACES)
    chosenBusTraces = {}
    for bt in chosen:
       chosenBusTraces[bt] = busTraces.pop(bt)
    return chosenBusTraces

def routeGen(busTrace):
    routeJumps = len(busTrace)
    route = []
    for i in range(routeJumps):
        route.append(busTrace[i])
    return route

def vmGen(vmsQtt, busFilePath):
    # units: storage(MB), cpu(MIPS), RAM(MB)
    VMs = []
    simMIPS = 2000
    busTraces = readBusTraces(busFilePath)
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
            "route": routeGen(busTraces[chosenBus]),
            "busId": chosenBus,
            "v_storage": chosenVm["v_storage"], 
            "v_CPU": chosenVm["v_CPU"], 
            "v_RAM": chosenVm["v_RAM"]
        }

        VMs.append(vm)
    return VMs, chosenBusTraces

def cloudletGen(linksInputFilePath, chosenBusTraces):
    cloudletsPositions = cpg.main(chosenBusTraces)

    Cloudlets = []
    simMIPS = 2000

    for c in range(len(cloudletsPositions)):
        cloudlet = {
            "cId": 'c' + str(c),
            "position": cloudletsPositions[c],
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
    random.seed(args[3])
    busFilePath = args[4]

    vms, chosenBusTraces = vmGen(vmsArg, busFilePath)
    cloudlets = cloudletGen(linksFilePath, chosenBusTraces)
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
    # python data_gen.py <number of vms> <number of cloudlets> <output file path> <seed>
    args = sys.argv[1:]
    if validateArgs(args):
        build(args)

if __name__ == "__main__":
    main()