from classes.Graph import Graph
from classes.Node import Node
import utils.json_utils as json_utils
import sys

def createGraph():
    nNodes = int(input())
    graphNodes = []
    for _ in range(nNodes):
        line = input().split(' ')
        graphNodes.append(Node(nId=line[0],
                            posX=int(line[1]),
                            posY=int(line[2])))
    graph = Graph(graphNodes)

    nEdges = int(input())
    for _ in range(nEdges):
        line = input().split(' ')
        node1 = graph.findNodeById(line[0])
        node2 = graph.findNodeById(line[1])
        weight = int(line[2])
        graph.addEdge(node1, node2, weight)
    return graph

def main(jsonFilePath):
    mainGraph = createGraph()
    mainGraph.printAdjList()
        
    jsonData = json_utils.readJsonInput(jsonFilePath)
    cloudlets = json_utils.buildCloudlets(jsonData['Cloudlets'])
    users = json_utils.buildUserVms(jsonData['UserVMs'])

    cloudletsNodes = [mainGraph.findNodeById(c.nodeId) for c in cloudlets]
    cloudletsSubgraph = mainGraph.getSubgraph(cloudletsNodes)
    
    usersRoutes = []
    for u in users:
        userRouteNodes = [mainGraph.findNodeById(routeNode) for routeNode in u.route]
        curr = mainGraph.getSubgraph(userRouteNodes)
        usersRoutes.append(curr)

    # output: mainGraph, cloudlets, users, cloudletsSubgraph, usersRoutes

if __name__ == '__main__':
    inputFilePath = sys.argv[1:][0]
    main(inputFilePath)