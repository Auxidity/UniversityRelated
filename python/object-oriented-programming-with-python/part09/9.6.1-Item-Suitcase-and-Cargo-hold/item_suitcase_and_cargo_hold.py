class Item:
    def __init__(self, name:str, weight:int):
        self.name_var = name
        self.weight_var = weight
    
    @property
    def name(self):
        return self.name_var

    @property
    def weight(self):
        return self.weight_var
    
    def __str__(self):
        return f"{self.name_var} ({self.weight_var} kg)"

class Suitcase:
    def __init__(self, max_weight:int):
        self.max_weight = max_weight
        self.weight_var = 0
        self.count_of_items = 0
        self.contents = []
    
    def add_item(self, item:Item):
        if self.weight_var + item.weight_var > self.max_weight:
            return "Overencumbered suitcase"
        else:
            self.weight_var += item.weight_var
            self.count_of_items += 1
            self.contents.append(f"{item.name_var} ({item.weight_var} kg)")
    
    def print_items(self):
        for content in self.contents:
            print(content) 

    @property
    def weight(self):
        return self.weight_var
    
    def heaviest_item(self):
        if not self.contents:
            return "No items in the suitcase"

        heaviest_item = max(self.contents, key=lambda x: int(x.split('(')[1].split(' ')[0])) #Finds the string part (x kg), turns the string value of x (which is between '(' and space ) to int, then finds max among all items

        return heaviest_item
    
    def __str__(self):
        if self.count_of_items != 1:
            return f"{self.count_of_items} items ({self.weight_var} kg)"
        else:
            return f"{self.count_of_items} item ({self.weight_var} kg)"
    


class CargoHold:
    def __init__(self, max_weight:int):
        self.max_weight = max_weight
        self.count = 0
        self.remaining_space = self.max_weight
        self.suitcases = []
    
    def add_suitcase(self,suitcase:Suitcase):
        if self.remaining_space - suitcase.weight_var < 0:
            return "Not enough space for this suitcase"
        else:
            self.remaining_space -= suitcase.weight_var
            self.count += 1
            self.suitcases.append(suitcase)

    def print_items(self):
        for suitcase in self.suitcases:
            suitcase.print_items()

    def __str__(self):
        return f"{self.count} suitcases, space for {self.remaining_space} kg"
    
    

"""
book = Item("ABC Book", 2)
phone = Item("Nokia 3210", 1)
brick = Item("Brick", 4)

adas_suitcase = Suitcase(10)
adas_suitcase.add_item(book)
adas_suitcase.add_item(phone)

peters_suitcase = Suitcase(10)
peters_suitcase.add_item(brick)

cargo_hold = CargoHold(1000)
cargo_hold.add_suitcase(adas_suitcase)
cargo_hold.add_suitcase(peters_suitcase)

print("The suitcases in the cargo hold contain the following items:")
cargo_hold.print_items()
"""