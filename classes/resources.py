class Resources:
    def __init__(self, cpu, ram, storage):
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
    
    @property
    def description(self) -> str:
        return f"CPU: {self.cpu} \nRAM: {self.ram} \nSTORAGE: {self.storage}"