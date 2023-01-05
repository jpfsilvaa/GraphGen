class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adjList = {node.nId: set() for node in self.nodes}      

    def findNodeById(self, nId):
        for i in self.nodes:
            if i.nId == nId:
                return i
        return None

    def addEdge(self, n1, n2, weight=1):
        self.adjList[n1.nId].add((n2, weight))
        self.adjList[n2.nId].add((n1, weight))
    

    def printAdjList(self):
        for key in self.adjList.keys():
            print("node", key, ": ", [(n.nId, w) for (n, w) in self.adjList[key]])

    def getSubgraph(self, nodes):
        subgraph = Graph(nodes)
        for n in subgraph.adjList:
            currAdjList = self.adjList[n]
            for node in currAdjList:
                if node[0].nId in subgraph.adjList.keys():
                    subgraph.addEdge(self.findNodeById(n), node[0], node[1])
        return subgraph