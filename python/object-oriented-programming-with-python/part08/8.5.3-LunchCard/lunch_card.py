import sys 


class ValueError(Exception):
    pass



class LunchCard:
    def __init__(self, balance: float, name:str):
        self.balance = balance
        self.name = name

    def eat_lunch(self):
        if self.balance - 2.6 < 0:
            raise ValueError("Insufficient balance")
        self.balance -= 2.6

    def eat_special(self):
        if self.balance - 4.6 < 0:
            raise ValueError("Insufficient balance")
        self.balance -= 4.6

    def deposit_money(self, deposit: float):
        if deposit < 0:
            raise ValueError("You cannot deposit an amount of money less than zero")
        else:
            self.balance += deposit

    def __str__(self):
        
        return f"{self.name}: The balance is {self.balance:.1f} euros"
    


"""
for i in range(1):
    try:
        peters_card = LunchCard(20, "Peter")
        graces_card = LunchCard(30, "Grace")
        peters_card.eat_special()
        graces_card.eat_lunch()
        print(peters_card)
        print(graces_card)
        peters_card.deposit_money(20)
        graces_card.eat_special()
        print(peters_card)
        print(graces_card)
        peters_card.eat_lunch()
        peters_card.eat_lunch()
        graces_card.deposit_money(50)
        print(peters_card)
        print(graces_card)
        
    except ValueError as e:
        print(f"{type(e).__name__}: {e}")
        sys.exit(1)
"""