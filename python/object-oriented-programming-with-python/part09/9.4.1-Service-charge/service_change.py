class BankAccount:
    def __init__(self, owner:str, acc_number:str, balance:float):
        self.owner = owner
        self.acc_number = acc_number
        self.balance = balance
        
    
    def __service_charge(self):
        self.balance -= 0.01*self.balance

    def deposit(self, amount:float):
        if amount > 0:
            self.balance += amount
            self.__service_charge()
        else:
            raise ValueError("The deposited amount must be positive.")
        
    def withdraw(self, amount:float):
        if amount < 0:
            raise ValueError("Deposited amount must be positive")
        elif self.balance - amount < 0:
            raise ValueError("Cannot withdraw more than accounts balance")
        else:
            self.balance -= amount
            self.__service_charge()

    def __str__(self):
        return f"Owner: {self.name}, Account number: {self.acc_number}, Balance: {self.balance}"
    
