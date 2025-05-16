class SuperHero:
    def __init__(self, name: str, superpowers: str):
        self.name = name
        # Split the superpowers string into a list, using a comma as the separator
        self.superpowers = superpowers.split(',') if superpowers else []

    def __str__(self):
        if not self.superpowers:  # Check if the list of superpowers is empty
            superpowers_str = "No superpowers"
        else:
            superpowers_str = ", ".join(self.superpowers).strip()
        return f"{self.name}, superpowers: {superpowers_str}"

class SuperGroup():
    def __init__(self, name: str, location:str):
        self._name = name
        self._location = location
        self._members = []

    @property
    def get_name(self) -> str:
        return self._name
    
    @property
    def get_location(self) -> str:
        return self._location

    def add_member(self, hero: SuperHero):
        self._members.append(hero)

    def print_group(self):
        print (f"{self.get_name}, {self.get_location}")
        print("Members:")
        for member in self._members:
            print(member)


