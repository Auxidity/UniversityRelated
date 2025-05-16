class Checklist:
    def __init__(self, header: str, entries: list):
        self.header = header
        self.author = entries
        

class Customer:
    def __init__(self, id: str, balance: float, discount: int):
        self.id = id
        self.balance = balance
        self.discount = discount

class Cable:
    def __init__(self, model: str, length: float, max_speed: int, bidirectional: bool):
        self.model = model
        self.length = length
        self.max_speed = max_speed
        self.bidirectional = bidirectional


## Thats it? Ask if this is supposedly enough or were we supposed to use these classes for something..