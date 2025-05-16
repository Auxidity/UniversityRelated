class Money:
    def __init__(self, euros: int, cents: int):
        # Check if both euros and cents are integers and positive
        if not isinstance(euros, int) or not isinstance(cents, int):
            raise ValueError("Both euros and cents must be integers.")
        if euros < 0 or cents < 0:
            raise ValueError("Both euros and cents must be positive.")
        # Check if cents is between 0 and 99
        if cents > 99:
            raise ValueError("Cents must be between 0 and 99.")
        
        self.__euros = euros
        self.__cents = cents

    def __str__(self):
        return f"{self.__euros}.{self.__cents:02d}"
    
    def __eq__(self, another):
        if isinstance(another, Money):
            return (self.__euros == another.__euros) and (self.__cents == another.__cents)
        return False

    def __gt__(self, another):
        if isinstance(another, Money):
            if self.__euros > another.__euros:
                return True
            elif self.__euros == another.__euros:
                return self.__cents > another.__cents
        return False
    
    def __add__(self, another):
        if isinstance(another, Money):
            new_money = Money(self.__euros, self.__cents)

            new_money.__euros += another.__euros
            new_money.__cents += another.__cents
            if new_money.__cents >= 100:
                new_money.__euros += 1
                new_money.__cents -= 100
            return new_money

    def __sub__(self, another):
        if isinstance(another, Money):
            new_money = Money(self.__euros, self.__cents)
            total_cents_self = self.__euros * 100 + self.__cents    #Converting everything to cents to ensure that cases like 0.5 - 0.9 dont return -0.4, and raise the error properly.
            total_cents_another = another.__euros * 100 + another.__cents
            if total_cents_self - total_cents_another < 0:
                raise ValueError("a negative result is not allowed")
            else:
                new_money.__euros -= another.__euros
                new_money.__cents -= another.__cents
                if new_money.__cents < 0:
                    new_money.__euros -= 1
                    new_money.__cents += 100
                return new_money

