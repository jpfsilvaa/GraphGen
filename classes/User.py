class UserVM:
    def __init__(self, uId, vmType, bid, avgSpeed, initTime, route, reqs):
        self.uId = uId
        self.vmType = vmType
        self.bid = bid
        self.avgSpeed = avgSpeed
        self.initTime = initTime
        self.route = route
        self.maxReq = 0
        self.reqs = reqs
        self.reqsSum = 0
        # self.connectedCloudlet
        self.allocatedCloudlet = None
        self.currLatency = 0
        self.currNode = None
