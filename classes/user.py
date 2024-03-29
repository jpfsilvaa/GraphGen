class UserVM:
    def __init__(self, uId, vmType, bid, avgSpeed, initTime, route, reqs):
        self.uId = uId
        self.vmType = vmType
        self.bid = bid
        self.avgSpeed = avgSpeed
        self.initTime = initTime
        self.route = route
        self.busId = 0
        self.maxReq = 0
        self.reqs = reqs
        self.reqsSum = 0
        # self.connectedCloudlet
        self.allocatedCloudlet = None
        self.pastCloudlets = list()
        self.currLatency = 0
        self.currNodeId = route[0]
        self.price = 0

    @property
    def description(self) -> str:
        return f"ID: {self.uId} \nROUTE: {self.route} \nALLOCATED CLOUDLET: {self.allocatedCloudlet} \nCURRENTE NODE POS: {self.currNodeId}"