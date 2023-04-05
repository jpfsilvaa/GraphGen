class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adjList = {node.nId: dict() for node in self.nodes}      

    def findNodeById(self, nId):
        for i in self.nodes:
            if i.nId == nId:
                return i
        return None

    def addEdge(self, n1, n2, weightAndSpeed):
        self.adjList[n1][n2] = weightAndSpeed
        self.adjList[n2][n1] = weightAndSpeed

    def printAdjList(self):
        for key in self.adjList.keys():
            print("node", key, ": ", [(n, w) for n, w in self.adjList[key].items()])

    def getSubgraph(self, nodes):
        subgraph = Graph(nodes)
        for n in subgraph.adjList:
            currAdjList = self.adjList[n]
            for node, weight in currAdjList.items():
                if node in subgraph.adjList.keys():
                    subgraph.addEdge(n, node, weight)
        return subgraph
    
    def getEdgeWeight(self, n1, n2):
        return self.adjList[n1][n2]