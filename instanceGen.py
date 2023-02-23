from GraphGen.classes.graph import Graph
import GraphGen.classes.node
import GraphGen.utils.json_utils as json_utils
import GraphGen.utils.pycgr_utils as pycgr_utils
import sys

TAG = 'instanceGen.py:'

def createGraph(graphFilePath):
    print(TAG, 'createGraph')
    nodes, edges = pycgr_utils.readNodesAndEdges(graphFilePath)
    graph = Graph(nodes)

    for e in edges:
        node_1 = e[0]
        node_2 = e[1]
        weight = e[2] # distance
        graph.addEdge(node_1, node_2, float(weight))
    return graph

def main(jsonFilePath, graphFilePath):
    print(TAG, 'main')
    mainGraph = createGraph(graphFilePath)
    # mainGraph.printAdjList()
        
    jsonData = json_utils.readJsonInput(jsonFilePath)
    cloudlets = json_utils.buildCloudlets(jsonData['Cloudlets'])
    users = json_utils.buildUserVms(jsonData['UserVMs'])

    """ 
    In fact, these subgraphs might be useful but I don't really need to return it...
    I can make then when necessary through the main graph
    cloudletsNodes = [mainGraph.findNodeById(c.nodeId) for c in cloudlets]
    cloudletsSubgraph = mainGraph.getSubgraph(cloudletsNodes)
    
    usersRoutes = []
    for u in users:
        userRouteNodes = [mainGraph.findNodeById(routeNode) for routeNode in u.route]
        curr = mainGraph.getSubgraph(userRouteNodes)
        usersRoutes.append(curr) """

    

    return [cloudlets, users, mainGraph]

if __name__ == '__main__':
    jsonFilePath = sys.argv[1:][0]
    graphFilePath = sys.argv[1:][1]
    main(jsonFilePath, graphFilePath)