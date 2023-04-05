from GraphGen.classes.graph import Graph
from GraphGen.classes.node import Node
import sys
import GraphGen.BusMovementModel.data_processing.xmlParser as xmlParser
import GraphGen.utils.json_utils as json_utils
import sim_utils

TAG = 'instanceGen.py:'

def createGraph(graphFilePath):
    sim_utils.log(TAG, 'createGraph')
    nodes, edges = xmlParser.readNodesAndEdges(graphFilePath)
    graph = Graph(nodes)

    for e in edges:
        node_1 = e[0]
        node_2 = e[1]
        distanceWeight = e[2]
        avgSpeed = e[3]
        graph.addEdge(node_1, node_2, (float(weight), avgSpeed))
    return graph

def main(jsonFilePath, graphFilePath):
    sim_utils.log(TAG, 'main')
    mainGraph = createGraph(graphFilePath)
        
    jsonData = json_utils.readJsonInput(jsonFilePath)
    cloudlets = json_utils.buildCloudlets(jsonData['Cloudlets'])
    users = json_utils.buildUserVms(jsonData['UserVMs'])
    subtraces = xmlParser.readSubtraces(graphFilePath)  

    return [cloudlets, users, mainGraph, subtraces]

if __name__ == '__main__':
    jsonFilePath = sys.argv[1:][0]
    graphFilePath = sys.argv[1:][1]
    main(jsonFilePath, graphFilePath)