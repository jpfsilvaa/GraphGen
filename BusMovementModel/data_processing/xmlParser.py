import xml.etree.ElementTree as ET
from classes.node import Node

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
                links.append((link.attrib['from'], link.attrib['to'], float(link.attrib['length'])))
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