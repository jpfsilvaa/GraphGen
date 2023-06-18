import json, math
from GraphGen.classes.cloudlet import Cloudlet
from GraphGen.classes.resources import Resources
from GraphGen.classes.user import UserVM

def readJsonInput(jsonFilePath):
    jsonFile = open(jsonFilePath)
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def buildCloudlets(jsonData):
    cloudlets = []
    for cloudlet in jsonData:
        cloudlets.append(Cloudlet(cloudlet['cId'],
                            (float(cloudlet['position'][0]), float(cloudlet['position'][1])),
                            int(cloudlet['coverageRadius']),
                            Resources(int(cloudlet['c_CPU']), 
                            int(cloudlet['c_RAM']),
                            int(cloudlet['c_storage']))
                            )
                        )
    return cloudlets

def buildUserVms(jsonData, mainGraph, busTraces):
    vmsList = []
    for user in jsonData:
        vmsList.append(UserVM(str(user['vId']),
                            str(user['vmType']),
                            int(user['bid']),
                            int(user['avgSpeed']),
                            calcTimeToInit(user, mainGraph, user['route'][0], busTraces[user['busId']]),
                            user['route'],
                            Resources(int(user['v_CPU']), 
                            int(user['v_RAM']),
                            int(user['v_storage']))
                            )
                        )
    return vmsList

def calcTimeToInit(user, mainGraph, initPosId, traces):
    initPos = mainGraph.findNodeById(initPosId)
    if initPos.nId == traces[0]:
        return 0
    
    currNodeIdx = 0
    arrivalTime = 0
    while traces[currNodeIdx] != initPos.nId:
        dist = mainGraph.adjList[traces[currNodeIdx]][traces[currNodeIdx+1]][0]
        avgSpeed = mainGraph.getEdgeWeight(traces[currNodeIdx], traces[currNodeIdx+1])[1]
        arrivalTime += dist // avgSpeed
        currNodeIdx += 1
    return arrivalTime