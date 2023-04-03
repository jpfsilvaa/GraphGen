class Cloudlet:
    def __init__(self, cId: str , nodeId: str, coverageArea: int, resources):
        self.cId = cId
        self.position = position
        self.coverageArea = coverageArea
        self.resources = resources
        self.currUsersAllocated = []

    @property
    def description(self) -> str:
        return f"ID: {self.cId} \nNODE POS: {self.nodeId} \nCURRENT USERS: {self.currUsersAllocated}"