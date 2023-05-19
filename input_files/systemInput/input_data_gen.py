import json
import random
import sys
from itertools import product
import xml.etree.ElementTree as ET

NUMBER_BUS_TRACES = 6

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
    for bt in chosen:
        chosenBusTraces[bt] = busTraces.pop(bt)
    return chosenBusTraces

def readSubtraces(inputFilePath):
    tree = ET.parse(inputFilePath)
    root = tree.getroot()

    pointsPerLink = {}
    nodes = {}
    for child in root:
        if child.tag == 'nodes':
            for node in child:
                nodes[node.attrib['id']] = (node.attrib['x'], node.attrib['y'])
        if child.tag == 'links':
            for link in child:
                latitudes = [lat for lat in link.attrib['shapeLat'].split(',')]
                longitudes = [lng for lng in link.attrib['shapeLng'].split(',')]
                if latitudes[0] != '' and longitudes[0] != '':
                    pointsPerLink[link.attrib['id']] = [(lat, lng) for lat, lng in zip(latitudes, longitudes)]
                else:
                    fromId = link.attrib['from']
                    toId = link.attrib['to']
                    pointsPerLink[link.attrib['id']] = [(nodes[fromId][0], nodes[fromId][1]), (nodes[toId][0], nodes[toId][1])]
    return pointsPerLink     

def getCloudletsPositions(subtraces, chosenBusTraces):
    cloudletsPositions = []
    chosenSubtraces = {}
    for bus in chosenBusTraces:
        for i in range(0, len(chosenBusTraces[bus]) - 1):
            link = chosenBusTraces[bus][i] + '-' + chosenBusTraces[bus][i + 1]
            chosenSubtraces[link] = subtraces[link]

    for link in chosenSubtraces:
        for i in range(0, len(chosenSubtraces[link]), 17):
            cloudletsPositions.append(chosenSubtraces[link][i])
    return cloudletsPositions

def routeGen(busTrace):
    routeJumps = random.choice(range(int(len(busTrace) / 3), len(busTrace)))
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
            "bid": random.gauss(100, 5),
            "v_storage": random.gauss(16 * 1024, 100),
            "v_CPU": random.gauss(4 * simMIPS, 100),
            "v_RAM": random.gauss(16 * 1024, 100)
        }

        ramIntensive = {
            "vmType": 'ramIntensive',
            "bid": random.gauss(150, 5),
            "v_storage": random.gauss(16 * 1024, 100),
            "v_CPU": random.gauss(8 * simMIPS, 100),
            "v_RAM": random.gauss(64 * 1024, 100)
        }

        cpuIntensive = {
            "vmType": 'cpuIntensive',
            "bid": random.gauss(150, 5),
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
    subtraces = readSubtraces(linksInputFilePath)
    cloudletsPositions = getCloudletsPositions(subtraces, chosenBusTraces)

    Cloudlets = []
    simMIPS = 2000

    for c in range(len(cloudletsPositions)):
        cloudlet = {
            "cId": 'c' + str(c),
            "position": cloudletsPositions[c],
            "coverageRadius": 1000,
            "c_storage": 4 * 1000 * 1024, 
            "c_CPU": 50 * simMIPS,
            "c_RAM": 160 * 1024
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