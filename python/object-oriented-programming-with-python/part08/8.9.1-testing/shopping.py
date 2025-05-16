class ShoppingList:
    def __init__(self):
        self.items = {}

    def add(self, item, amount):
        if item in self.items:
            self.items[item] += amount
        else:
            self.items[item] = amount
        return self.items

    def number_of_items(self):
        return len(self.items)

    def item(self, index):
        if 1 <= index <= len(self.items):
            return list(self.items.keys())[index - 1]
        else:
            raise IndexError("Item index out of range")

    def amount(self, index):
        if 1 <= index <= len(self.items):
            return list(self.items.values())[index - 1]
        else:
            raise IndexError("Item index out of range")
