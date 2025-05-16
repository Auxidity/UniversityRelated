class Person:
    def __init__(self, name: str,age:int, height: int, weight: int):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class BabyCentre:
    def __init__(self, weigh_in=None):
        if weigh_in is not None:
            self.weigh_in_count = weigh_in
        else:
            self.weigh_in_count = 0
        
    def feed(self, person:Person):
        person.weight += 1


    def weigh(self, person:Person):
        self.weigh_in_count += 1
        return person.weight

    def weigh_ins(self):
        return self.weigh_in_count

"""
baby_centre = BabyCentre()

eric = Person("Eric", 1, 110, 7)
peter = Person("Peter", 33, 176, 85)

print(f"Total number of weigh-ins is {baby_centre.weigh_ins()}")

baby_centre.weigh(eric)
baby_centre.weigh(eric)

print(f"Total number of weigh-ins is {baby_centre.weigh_ins()}")

baby_centre.weigh(eric)
baby_centre.weigh(eric)
baby_centre.weigh(eric)
baby_centre.weigh(eric)

print(f"Total number of weigh-ins is {baby_centre.weigh_ins()}")
"""