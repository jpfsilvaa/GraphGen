import xml.etree.ElementTree as ET
from GraphGen.classes.node import Node

def readNodesAndEdges(inputFilePath):
    tree = ET.parse(inputFilePath)
    root = tree.getroot()

    nodes = []
    links = []
    for child in root:
        if child.tag == 'nodes':
            for node in child:
                n = Node(nId=node.attrib['id'], 
                            posX=float(node.attrib['x']), 
                            posY=float(node.attrib['y']))
                nodes.append(n)

        if child.tag == 'links':
            for link in child:
                avgSpeeds = [float(i) for i in link.attrib['avgspeed'].split(', ') if float(i) > 0]
                
                if len(avgSpeeds) == 0:
                    linkAvgSpeed = 10
                else:
                    linkAvgSpeed = sum(avgSpeeds) / len(avgSpeeds)
                links.append((link.attrib['from'], 
                                link.attrib['to'], 
                                float(link.attrib['length']),
                                linkAvgSpeed))
    return nodes, links

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