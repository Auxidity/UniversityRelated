class LunchCard:
    def __init__(self, balance: float):
        self.balance = balance

    def deposit_money(self, amount: float):
        self.balance += amount

    def subtract_from_balance(self, amount: float):
        if (self.balance > amount):            
            self.balance -= amount
            return f"Payment succesful: True"
        else:
            return f"Payment succesful: False"

class PaymentTerminal:
    def __init__(self):
        # Initially there is 1000 euros in cash available at the terminal
        self.funds = 1000
        self.lunches = 0
        self.specials = 0

    def eat_lunch(self, payment: float):
        self.funds += payment

        if payment < 2.5:
            self.funds -= payment
            return payment #Potentially should say that transaction was unsuccesful but it wasn't specified if that should be mentioned, only that entire payment should be returned.
        else:
            self.lunches += 1
            self.funds -= payment
            self.funds += 2.5
            payment = payment -2.5
            return payment

    def eat_special(self, payment: float):
        self.funds += payment

        if payment < 4.3:
            self.funds -= payment
            return payment #Potentially should say that transaction was unsuccesful but it wasn't specified if that should be mentioned, only that entire payment should be returned.
        else:
            self.specials += 1
            self.funds -= payment
            self.funds += 4.3
            payment = payment -4.3
            return payment
        
    def eat_lunch_lunchcard(self, card: LunchCard):
        if card.subtract_from_balance(2.5) == "Payment succesful: True":
            self.lunches += 1
            return True
        else:
            return False

    def eat_special_lunchcard(self, card: LunchCard):
        if card.subtract_from_balance(4.3) == "Payment succesful: True":
            self.specials += 1
            return True
        else:
            return False
        
    def deposit_money_on_card(self, card: LunchCard, amount: float):
        self.funds += amount
        card.deposit_money(amount)


"""
if __name__ == "__main__":
    exactum = PaymentTerminal()

    card = LunchCard(2)
    print(f"Card balance is {card.balance} euros")

    result = exactum.eat_special_lunchcard(card)
    print("Payment successful:", result)

    exactum.deposit_money_on_card(card, 100)
    print(f"Card balance is {card.balance} euros")

    result = exactum.eat_special_lunchcard(card)
    print("Payment successful:", result)
    print(f"Card balance is {card.balance} euros")

    print("Funds available at the terminal:", exactum.funds)
    print("Regular lunches sold:", exactum.lunches)
    print("Special lunches sold:", exactum.specials)

"""