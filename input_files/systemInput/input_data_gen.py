import json
import random
import sys
from itertools import product
import xml.etree.ElementTree as ET

NUMBER_BUS_TRACES = 10

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
    for child in root:
        if child.tag == 'links':
            for link in child:
                latitudes = [lat for lat in link.attrib['shapeLat'].split(',')]
                longitudes = [lng for lng in link.attrib['shapeLng'].split(',')]
                if len(latitudes) > 1 and len(longitudes) > 1:
                    pointsPerLink[link.attrib['id']] = [(lat, lng) for lat, lng in zip(latitudes, longitudes)]
    return pointsPerLink            

def getCloudletsPositions(subtraces):
    cloudletsPositions = []
    for link in subtraces:
        for i in range(0, len(subtraces[link]), 17):
            cloudletsPositions.append(subtraces[link][i])
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

    for i in range(vmsQtt):
        busTraces = readBusTraces(busFilePath)
        chosenBus = random.choice(list(busTraces.keys()))

        gp1 = {
            "vmType": 'gp1',
            "bid": random.gauss(100, 5),
            "v_storage": 3 * 1024, 
            "v_CPU": 2 * simMIPS, 
            "v_RAM": 4 * 1024
        }

        gp2 = {
            "vmType": 'gp2',
            "bid": random.gauss(100, 5),
            "v_storage": 16 * 1024, 
            "v_CPU": 4 * simMIPS, 
            "v_RAM": 16 * 1024
        }

        ramIntensive = {
            "vmType": 'ramIntensive',
            "bid": random.gauss(150, 5),
            "v_storage": 16 * 1024, 
            "v_CPU": 8 * simMIPS, 
            "v_RAM": 64 * 1024
        }

        cpuIntensive = {
            "vmType": 'cpuIntensive',
            "bid": random.gauss(150, 5),
            "v_storage": 16 * 1024, 
            "v_CPU": 16 * simMIPS, 
            "v_RAM": 32 * 1024
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
        print("VM " + str(i) + " generated!")


    return VMs

def cloudletGen(linksInputFilePath):

    subtraces = readSubtraces(linksInputFilePath)
    cloudletsPositions = getCloudletsPositions(subtraces)

    Cloudlets = []
    simMIPS = 2000

    for c in range(len(cloudletsPositions)):
        cloudlet = {
            "cId": 'c' + str(c),
            "position": cloudletsPositions[c],
            "coverageRadius": 500,
            "c_storage": 512 * 1024, 
            "c_CPU": 80 * simMIPS,
            "c_RAM": 512 * 1024
        }
        Cloudlets.append(cloudlet)

    return Cloudlets

def build(args):
    vmsArg = int(args[0])
    linksFilePath = args[1]
    outFilePath = args[2]
    random.seed(args[3])
    busFilePath = args[4]

    cloudlets = cloudletGen(linksFilePath)
    mainObject = {
                    "UserVMs": vmGen(vmsArg, busFilePath), 
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