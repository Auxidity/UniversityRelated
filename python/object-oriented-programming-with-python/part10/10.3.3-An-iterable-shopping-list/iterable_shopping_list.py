class ShoppingList:
    def __init__(self):
        self.items = {}
        self.product_list =[]

    def add(self, item, amount):
        if item in self.items:
            self.items[item] += amount
        else:
            self.items[item] = amount
            self.product_list.append((item, amount))

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
    
    def __iter__(self):
        self.current_index = 0
        return self
    
    def __next__(self):
        if self.current_index < len(self.product_list):
            product = self.product_list[self.current_index]
            self.current_index += 1
            return product
        else:
            raise StopIteration("End of iteration")
    

    
def total_units( object:ShoppingList):
    return sum(object.items.values())


"""
shopping_list = ShoppingList()
shopping_list.add("bananas", 10)
shopping_list.add("apples", 5)
shopping_list.add("pineapple", 1)

for product in shopping_list:
    print(f"{product[0]}: {product[1]} units")
"""