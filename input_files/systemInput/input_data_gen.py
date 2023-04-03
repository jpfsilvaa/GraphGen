import random
import sys
from itertools import product

def vmGen(vmsQtt):
    # units: storage(MB), cpu(MIPS), RAM(MB)
    VMs = []
    simMIPS = 2000

    chosenVm = {
        "vId": 'v0', 
        "vmType": 'gp1',
        "bid": random.gauss(100, 3),
        "avgSpeed": 16,
        "initialTime": 0,
        "route": ('n0', 'n2', 'n3', 'n5'),
        "v_storage": 3 * 1024, 
        "v_CPU": 2 * simMIPS, 
        "v_RAM": 4 * 1024
    }
    VMs.append(chosenVm)

    return VMs

def cloudletGen(cloudletQtt):
    # units: storage(MB), cpu(MIPS), RAM(MB)
    Cloudlets = []
    cloudletsArg = int(args[1])
    outFilePath = args[2]
    random.seed(args[3])

    cloudlets = cloudletGen(cloudletsArg)
    mainObject = {
                    "UserVMs": vmGen(vmsArg), 
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