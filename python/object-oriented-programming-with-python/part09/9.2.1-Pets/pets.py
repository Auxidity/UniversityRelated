class Pet:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def __str__(self):
        return f"{self.name}"

class Person:
    def __init__(self, name: str, pet: Pet):
        self.name = name
        self.pet = pet

    def __str__(self):
        return f"{self.name}, whose pal is {self.pet}, a {self.pet.species}"

