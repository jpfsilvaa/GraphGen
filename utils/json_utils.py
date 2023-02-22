import json, math
from classes.Cloudlet import Cloudlet
from classes.Resources import Resources
from classes.User import UserVM

def readJsonInput(jsonFilePath):
    jsonFile = open(jsonFilePath)
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def buildCloudlets(jsonData):
    cloudlets = []
    for cloudlet in jsonData:
        cloudlets.append(Cloudlet(str(cloudlet['cId']),
                            str(cloudlet['node']),
                            int(cloudlet['coverageArea']),
                            Resources(int(cloudlet['c_CPU']), 
                            int(cloudlet['c_RAM']),
                            int(cloudlet['c_storage']))
                            )
                        )
    return cloudlets

def buildUserVms(jsonData):
    vmsList = []
    for user in jsonData:
        vmsList.append(UserVM(str(user['vId']),
                            str(user['vmType']),
                            int(user['bid']),
                            int(user['avgSpeed']),
                            user['initialTime'],
                            user['route'],
                            Resources(int(user['v_CPU']), 
                            int(user['v_RAM']),
                            int(user['v_storage']))
                            )
                        )
    return vmsList
