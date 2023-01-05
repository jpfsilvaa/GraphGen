class Cloudlet:
    def __init__(self, cId: str , nodeId: str, coverageArea: int, resources):
        self.cId = cId
        self.nodeId = nodeId
        self.coverageArea = coverageArea
        self.resources = resources