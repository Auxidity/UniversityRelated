class Person:
    def __init__(self, name: str, height: int):
        self.name = name
        self.height = height
        

class Room:
    def __init__(self, persons=None):
        if persons is not None:
            self.persons = persons
        else:
            self.persons = []
        

    def is_empty(self):
        if len(self.persons) == 0:
            return True
        else:
            return False
        
    def add(self, person:Person):
        self.persons.append(person)

    def print_contents(self):
        sum_of_height = 0
        for person in self.persons:
            sum_of_height += person.height

        print(f"There are {len(self.persons)} persons in the room, and their combined height is {sum_of_height} cm")

        for person in self.persons:
            print(person.name, f"({person.height} cm)")

    def shortest(self):
        if  self.persons:
            shortest_person_height = min(person.height for person in self.persons)

            shortest_person_name = None

            for person in self.persons:
                if person.height == shortest_person_height:
                    shortest_person_name = person.name
                    break
            return shortest_person_name

        else:
            return None
    
    def remove_shortest(self):
        
        shortest_person = self.shortest()
        
        
        if shortest_person:
            for person in self.persons:
                if person.name == shortest_person:
                    self.persons.remove(person)
                    return person

            



"""
room = Room()

room.add(Person("Lea", 183))
room.add(Person("Kenya", 172))
room.add(Person("Nina", 162))
room.add(Person("Ally", 166))
room.print_contents()

print()

removed = room.remove_shortest()
print(f"Removed from room: {removed.name}")

print()

room.print_contents()
"""