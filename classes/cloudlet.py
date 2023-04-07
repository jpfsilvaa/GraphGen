import copy

class Cloudlet:
    def __init__(self, cId: str , position: str, coverageArea: int, resources):
        self.cId = cId
        self.position = position
        self.coverageArea = coverageArea
        self.resources = resources
        self.resourcesFullValues = copy.deepcopy(resources)
        self.currUsersAllocated = []

    @property
    def description(self) -> str:
        return f"ID: {self.cId} \nPOS: {self.position} \nCURRENT USERS: {self.currUsersAllocated}"