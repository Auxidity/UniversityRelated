class MagicPotion:
    def __init__(self, name: str):
        self.name = name
        self.ingredients = []

    def add_ingredient(self, ingredient: str, amount: float):
        self.ingredients.append((ingredient, amount))

    def print_recipe(self):
        print(f"{self.name}:")
        for ingredient, amount in self.ingredients:
            print(f"{ingredient} {amount} grams")

class SecretMagicPotion(MagicPotion):
    def __init__(self, name: str, password:str):
        super().__init__(name)
        self.password = password

    def add_ingredient(self, ingredient: str, amount: float, password:str):
        if password == self.password:
            return super().add_ingredient(ingredient, amount)
        else:
            raise ValueError("Wrong password")
    
    def print_recipe(self, password: str):
        if password == self.password:
            return super().print_recipe()
        else:
            raise ValueError("Wrong password")
        
