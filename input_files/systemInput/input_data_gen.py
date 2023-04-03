import json
import random
import sys
from itertools import product
import xml.etree.ElementTree as ET

def readBusTraces(inputFilePath):
    tree = ET.parse(inputFilePath)
    root = tree.getroot()

    busTraces = {}
    for child in root:
        if child.tag == 'bus':
            busId = child.attrib['id']
            busTrace = [int(i) for i in child.attrib['stops'].split(',')]
            busTraces[busId] = busTrace
    return busTraces

def readSubtraces(inputFilePath):
    tree = ET.parse(inputFilePath)
    root = tree.getroot()

    pointsPerLink = {}
    for child in root:
        if child.tag == 'links':
            for link in child:
                latitudes = [lat for lat in link.attrib['shapeLat'].split(',')]
                longitudes = [lng for lng in link.attrib['shapeLng'].split(',')]
                pointsPerLink[link.attrib['id']] = [(lat, lng) for lat, lng in zip(latitudes, longitudes)]
    return pointsPerLink            

def getCloudletsPositions(subtraces):
    cloudletsPositions = []
    for link in subtraces:
        # adiciono uma cloudlet a cada 8 pontos, porque a distancia entre cada ponto é, aprox., 50-70m
        # então, como estou considerando o raio de cobertura como 500 metros, 8 pontos de distancia faz uma 
        # intersecção de aprox. 200 metros entre elas
        for i in range(0, len(subtraces[link]), 8):
            cloudletsPositions.append(subtraces[link][i])
    return cloudletsPositions

def vmGen(vmsQtt, busFilePath):
    # units: storage(MB), cpu(MIPS), RAM(MB)
    VMs = []
    simMIPS = 2000

    for i in range(vmsQtt):
        busTraces = readBusTraces(busFilePath)
        chosenBus = random.choice(list(busTraces.keys()))

        chosenVm = {
            "vId": 'v' + str(i), 
            "vmType": 'gp1',
            "bid": random.gauss(100, 3),
            "avgSpeed": 16,
            "initialTime": 0,
            "route": routeGen(busTraces[chosenBus]),
            "busId": chosenBus,
            "v_storage": 3 * 1024, 
            "v_CPU": 2 * simMIPS, 
            "v_RAM": 4 * 1024
        }
        VMs.append(chosenVm)


    return VMs

def routeGen(busTrace):
    routeJumps = random.choice(range(int(len(busTrace) / 3), len(busTrace)))
    route = []
    for i in range(routeJumps):
        route.append(busTrace[i])
    return route

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
            "c_storage": 250 * 1024, 
            "c_CPU": 12 * simMIPS,
            "c_RAM": 16 * 1024
        }
        Cloudlets.append(cloudlet)
    
    # # units: storage(MB), cpu(MIPS), RAM(MB)
    # Cloudlets = []
    # simMIPS = 2000
    # clA0 = { "cId": "cA_0",
    #     "node": "n0",
    #     "coverageRadius": 500,
    #     "c_storage": 250 * 1024, 
    #     "c_CPU": 12 * simMIPS,
    #     "c_RAM": 16 * 1024
    # }

    # clA1 = { "cId": "cA_1",
    #     "node": "n2",
    #     "coverageRadius": 500,
    #     "c_storage": 250 * 1024, 
    #     "c_CPU": 12 * simMIPS,
    #     "c_RAM": 16 * 1024
    # }

    # clA2 = { "cId": "cA_2",
    #     "node": "n3",
    #     "coverageRadius": 500,
    #     "c_storage": 250 * 1024, 
    #     "c_CPU": 12 * simMIPS,
    #     "c_RAM": 16 * 1024
    # }

    # clA3 = { "cId": "cA_3",
    #     "node": "n5",
    #     "coverageRadius": 500,
    #     "c_storage": 250 * 1024, 
    #     "c_CPU": 12 * simMIPS,
    #     "c_RAM": 16 * 1024
    # }

    # Cloudlets.append(clA0)
    # Cloudlets.append(clA1)
    # Cloudlets.append(clA2)
    # Cloudlets.append(clA3)

    return Cloudlets

def build(args):
    vmsArg = int(args[0])
    cloudletsArg = args[1]
    outFilePath = args[2]
    random.seed(args[3])
    busFilePath = args[4]

    cloudlets = cloudletGen(cloudletsArg)
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