import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
import xml.etree.ElementTree as ET
import utm
import numpy as np
from quadTree import Point, QuadNode
import random

def generate_random_hex_colors(num_colors):
    rgb_values = np.random.randint(0, 256, size=(num_colors, 3))
    hex_colors = []
    for rgb in rgb_values:
        hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        hex_colors.append(hex_color)

    return hex_colors

def uiGenAll(points, minX, minY, maxX, maxY, radius, seed):
    newRadius = radius/111111 # convert meters to degrees
    fig, ax = plt.subplots()
    for p in points:
        circle = Circle((p[0], p[1]), newRadius, edgecolor='gray', facecolor='none')
        ax.add_patch(circle)

    plt.xlim(minX, maxX)
    plt.ylim(minY, maxY)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.savefig(f'all_cls_s{seed}_cls.png')
    plt.show()

def uiGen(points, minX, minY, maxX, maxY, radius, seed):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 
              'yellow', 'black', 'magenta', 'lime', 'teal', 'aqua', 'maroon', 'navy', 'silver', 'limegreen',
              'darkgreen', 'darkblue', 'darkred', 'darkorange', 'darkcyan', 'darkmagenta', 'darkgray', 'darkkhaki', 'darkolivegreen', 'darkorchid',
              'darkslateblue', 'darkslategray', 'darkturquoise', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen']
    newRadius = radius/111111 # convert meters to degrees
    fig, ax = plt.subplots()
    img_path = 'antena.jpg'
    colorsIndex = 0
    drawnPoints = []
    usedColors = []
    for k in points.keys():
        # Use this only with a small number of points
        # img = mpimg.imread(img_path)
        # img_size = newRadius/3
        # ax.imshow(img, extent=(x - img_size, x + img_size, y - img_size, y + img_size))
        for p in points[k]:
            if p not in drawnPoints and p != points[k][-1]:
                drawnPoints.append(p)
                circle = Circle((p[0], p[1]), newRadius, edgecolor=colors[colorsIndex], facecolor='none')
                ax.add_patch(circle)
        usedColors.append(points[k][-1])
        colorsIndex += 1

    plt.xlim(minX, maxX)
    plt.ylim(minY, maxY)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.savefig(f'instance{len(points.keys())}routes_s{seed}_cls.png')
    plt.show()
    return usedColors

def uiBusLinesGen(points, minX, minY, maxX, maxY, seed, isLine, usedColors):
    r = 0.0005
    fig, ax = plt.subplots()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'yellow']
    colorsIndex = 0
    drawnPoints = []
    colorsIndex = 0
    for k in points.keys():
        if isLine:
            ax.plot([p[0] for p in points[k]], [p[1] for p in points[k]], color=usedColors[colorsIndex])
        else:
            for p in points[k]:
                if p not in drawnPoints and p != points[k][-1]:
                    drawnPoints.append(p)
                    circle = Circle((p[0], p[1]), r, edgecolor=usedColors[colorsIndex], facecolor=usedColors[colorsIndex])
                    ax.add_patch(circle)
        colorsIndex += 1

    plt.xlim(minX, maxX)
    plt.ylim(minY, maxY)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    text = 'lines' if isLine else 'points'
    plt.savefig(f'instance{len(points.keys())}routes_s{seed}_{text}.png')
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
    closePointsDict = {}
    for rId, nodes in routeNodes.items():
        closePointsDict[rId] = []
        for n in nodes:
            nodesList = [(p.x, p.y) for p in quadtree.query(n[0], n[1], radius)]
            closePointsDict[rId].extend(nodesList)
            closePoints.extend(nodesList)
    return closePointsDict, list(set(closePoints))

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

def findPointInDict(pointsDict, point):
    for k, v in pointsDict.items():
        if point in v:
            return k,v
    return None

def main(chosenRoutes, seed):
    random.seed(seed)
    mapFilePath = '/home/jps/GraphGenFrw/Simulator/GraphGen/BusMovementModel/raw_data/map_20171024.xml'
    
    nodes = readNodes(mapFilePath)
    minX, minY, maxX, maxY = getMinMax(nodes)
    coverageRadius = 500
    points = pointsGen(minX, minY, maxX, maxY, coverageRadius)
    nodesQuadTree = buildQuadtree(points)
    routeNodes = getRouteNodes(nodes, chosenRoutes)

    closePointsDict, closePoints = getClosePoints(nodesQuadTree, routeNodes, coverageRadius)
    finalResult = []

    colors = generate_random_hex_colors(len(closePointsDict.keys()))
    colorIdx = 0
    for k in closePointsDict.keys():
        closePointsDict[k].extend([colors[colorIdx]])
        colorIdx += 1

    for p in closePoints:
        convertedPoint = utm.from_latlon(p[0], p[1])
        key, val = findPointInDict(closePointsDict, p)
        color = val[-1]
        finalResult.append((convertedPoint[0], convertedPoint[1], (key, color)))
    print(len(finalResult), 'cloudlets generated')

    newMinX = min([float(p[0]) for node in routeNodes.values() for p in node]) - 0.05
    newMinY = min([float(p[1]) for node in routeNodes.values() for p in node]) - 0.05
    newMaxX = max([float(p[0]) for node in routeNodes.values() for p in node]) + 0.05
    newMaxY = max([float(p[1]) for node in routeNodes.values() for p in node]) + 0.05

    # uiGenAll(points, newMinX, newMinY, newMaxX, newMaxY, coverageRadius, seed)

    usedColors = uiGen(closePointsDict, newMinX, newMinY, newMaxX, newMaxY, 
                   coverageRadius, seed)

    uiBusLinesGen(routeNodes, newMinX, newMinY, newMaxX, newMaxY, 
                  seed, isLine=True, usedColors=usedColors)

    # uiBusLinesGen(routeNodes, newMinX, newMinY, newMaxX, newMaxY, 
    #               seed, isLine=True, usedColors=usedColors)
    return finalResult