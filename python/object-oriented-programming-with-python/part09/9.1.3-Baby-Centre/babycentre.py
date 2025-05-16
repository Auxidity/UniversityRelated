class Person:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

class BabyCentre:
    def weigh(self, person: Person):
        # Return the weight of the person passed as an argument
        return person.weight
