from GraphGen.classes.node import Node

def readNodesAndEdges(inputFilePath):
    with open(inputFilePath, "r") as f:
        for _ in range(7):
            next(f)
        
        nNodes = int(f.readline())
        nEdges = int(f.readline())
        
        nodes = []
        for _ in range(nNodes):
            line = f.readline().split(' ')
            n = Node(nId=line[0],
                        posX=float(line[1]),
                        posY=float(line[2]))
            nodes.append(n)
        
        edges = []
        for _ in range(nEdges):
            line = f.readline().split(' ')
            edges.append((line[0], line[1], line[2]))

    return nodes, edges