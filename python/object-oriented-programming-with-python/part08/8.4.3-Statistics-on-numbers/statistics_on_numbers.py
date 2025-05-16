import sys

class InvalidInputError(Exception):
    pass

class  NumberStats:
    def __init__(self):
        try:
            self.number_list = []
        except InvalidInputError as e:
            print(f"{e}")
            sys.exit(1)

    def add_number(self, number:int):
        if not isinstance(number, (int)) or number < -1:
            raise InvalidInputError("Invalid input, please provide a positive integer")
    
        self.number_list.append(number)
            
    def count_numbers(self):
        return len(self.number_list)
    
    def get_sum(self):
        return sum(self.number_list)

    def average(self):
        if not self.number_list:
            raise InvalidInputError("No numbers have been added yet, are you trying to divide with 0?")
            
            
        return sum(self.number_list)/len(self.number_list)




def test():
    stats = NumberStats()
    uneven_number = 0
    even_number = 0
    while True:
        try:
            
            user_input = input("Enter an integer or -1 to stop: ")
            number = int(user_input)

            if number == -1:
                break

            if number % 2 == 1:
                uneven_number += number
            
            if number % 2 == 0:
                even_number += number

            stats.add_number(number)
            
        except InvalidInputError as e:
            print(f"{e}")
    return stats.count_numbers(), stats.get_sum(), stats.average(), uneven_number, even_number

"""
print("Numbers added:", stats.count_numbers())
print("Sum of numbers:", stats.get_sum())
print("Mean of numbers:", stats.average())
print(f"Sum of uneven numbers: {uneven_number}")
print(f"Sum of even numbers: {even_number}")
"""