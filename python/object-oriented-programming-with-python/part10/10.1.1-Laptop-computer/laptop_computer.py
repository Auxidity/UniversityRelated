class Computer:
    def __init__(self, model: str, speed: int):
        self.model = model
        self.speed = speed

class LaptopComputer(Computer):
    def __init__(self, model: str, speed: int, weight:int):
        super().__init__(model, speed)
        self.weight = weight

    def __str__(self):
        return f"{self.model}, {self.speed} MHz, {self.weight} kg"


