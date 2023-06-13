import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
import xml.etree.ElementTree as ET
import utm
import numpy as np
from quadTree import Point, QuadNode
import random

def uiGen(points, minX, minY, maxX, maxY, radius):
    newRadius = radius/111111 # convert meters to degrees
    fig, ax = plt.subplots()
    img_path = 'antena.jpg'
    for p in points:
        # Use this only with a small number of points
        # img = mpimg.imread(img_path)
        # img_size = newRadius/3
        # ax.imshow(img, extent=(x - img_size, x + img_size, y - img_size, y + img_size))
        circle = Circle((p.x, p.y), newRadius, edgecolor='b', facecolor='none')
        ax.add_patch(circle)

    plt.xlim(minX, maxX)
    plt.ylim(minY, maxY)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.savefig(f'instance.png')
    plt.show()

def pointsGen(minX, minY, maxX, maxY, radius):
    points = []
    nextPointX = minX
    nextPointY = minY
    advance = True
    step = 2*radius - 0.6*radius # intersection of 300m for radius of 500m
    while nextPointY < maxY:
        while nextPointX < maxX:
            points.append((nextPointX, nextPointY))
            nextPointX += step
        nextPointY += step
        if advance:
            nextPointX = minX + step/2
            advance = False
        else:
            nextPointX = minX
            advance = True
    return [convertUTMtoLatLong(point) for point in points]

def readNodes(inputFilePath):
    tree = ET.parse(inputFilePath)
    root = tree.getroot()
    nodes = {}
    for child in root:
        if child.tag == 'nodes':
            for node in child:
                nodes[node.attrib['id']] = ((float(node.attrib['x']), float(node.attrib['y'])))
    return nodes     

def convertUTMtoLatLong(point):
    # Sao Paulo's zone number and zone letter
    zone_number = 23
    zone_letter = 'K'
    lat_, long_ = utm.to_latlon(point[0], point[1], zone_number, zone_letter)
    return lat_, long_

def getNodesPos(nodesIds, nodes):
    nodesPos = [convertUTMtoLatLong(nodes[str(nodeId)]) for nodeId in nodesIds]
    return nodesPos

def buildQuadtree(points):
    maxX = 180
    maxY = 360
    quadtree = QuadNode(0, 0, maxX, maxY)
    for p in points:
        quadtree.insert(Point(p[0], p[1], None))
    return quadtree

def getClosePoints(quadtree, routeNodes, radius):
    closePoints = []
    for nodes in routeNodes.values():
        for n in nodes:
            closePoints.extend(quadtree.query(n[0], n[1], radius))
    return closePoints

def getRouteNodes(nodes, chosenBusTraces):
    routeNodes = {}
    for routeId, busTrace in chosenBusTraces.items():
        routeNodes[routeId] = getNodesPos(busTrace, nodes)
    return routeNodes

def getMinMax(nodes):
    maxX = max([float(node[0]) for node in nodes.values()])
    minX = min([float(node[0]) for node in nodes.values()])
    maxY = max([float(node[1]) for node in nodes.values()])
    minY = min([float(node[1]) for node in nodes.values()])
    return minX, minY, maxX, maxY

def main(chosenRoutes):
    random.seed(11)
    mapFilePath = '/home/jps/GraphGenFrw/Simulator/GraphGen/BusMovementModel/raw_data/map_20171024.xml'
    
    nodes = readNodes(mapFilePath)
    minX, minY, maxX, maxY = getMinMax(nodes)
    coverageRadius = 500
    points = pointsGen(minX, minY, maxX, maxY, coverageRadius)
    nodesQuadTree = buildQuadtree(points)
    routeNodes = getRouteNodes(nodes, chosenRoutes)

    closePoints = getClosePoints(nodesQuadTree, routeNodes, coverageRadius*1.5)
    finalResult = []
    for p in closePoints:
        convertedPoint = utm.from_latlon(p.x, p.y)
        finalResult.append((convertedPoint[0], convertedPoint[1]))
    print(len(finalResult))

    uiGen(closePoints, np.amin([float(node[0]) for node in points]), 
                   np.amin([float(node[1]) for node in points]), 
                   np.amax([float(node[0]) for node in points]), 
                   np.amax([float(node[1]) for node in points]), 
                   coverageRadius)
    return finalResult