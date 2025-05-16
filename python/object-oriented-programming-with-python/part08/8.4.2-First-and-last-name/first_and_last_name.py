import re
import sys


class InvalidInputError(Exception):
    pass

def is_valid_name_part(part):
    capital_letter_count = 0
    hyphen_count = 0

    for char in part:
        if char.isupper():
            capital_letter_count += 1

        if char == '-':
            hyphen_count += 1

    if hyphen_count >= 2 or hyphen_count < 0:
        raise InvalidInputError("Too many hyphens")
    elif hyphen_count == 1 and capital_letter_count != 2:
        raise InvalidInputError("Too many or too few capital letters present")
    elif hyphen_count == 0 and capital_letter_count != 1:
        raise InvalidInputError("Too many or too few capital letters present")

    if not part[0].isupper():
        #This error only raises if theres enough capital letters to pass first check but it isn't the first one.
        raise InvalidInputError("Invalid name, does not begin with a capital letter")

    hyphen_idx = part.find('-')
    # Checks if there is a hyphen
    if hyphen_idx != -1:
        # Checks if the letter after hyphen is capital
        if hyphen_idx + 1 < len(part) and not part[hyphen_idx + 1].isupper():
            raise InvalidInputError("Letters after hyphen must be capital")
        
        # Checks if the name ends with a hyphen
        if hyphen_idx == len(part) -1:
            raise InvalidInputError("Name cannot end with a hyphen")

    return bool(re.match(r'^[A-ZÄÖÅa-zäöå-]{1,}(-[A-ZÄÖÅa-zäöå-]+)*$', part))
   

def validate_input(input_string):
    parts = input_string.split(' ')

    if len(parts) == 2:
        first_name, last_name = parts

        # Validate the first name
        if not is_valid_name_part(first_name):
            raise InvalidInputError("Invalid first name. Must start with a capital letter and not contain numbers or special characters outside of hyphens.")

        # Validate the last name
        if not is_valid_name_part(last_name):
            raise InvalidInputError("Invalid last name. Must start with a capital letter and not contain numbers or special characters outside of hyphens.")

        return input_string
    else:
        raise InvalidInputError("Invalid name format. Both names must start with a capital letter and not contain numbers or special characters outside of hyphens.")

    
class Person:
    def __init__(self, name: str):
        try:
            self.name = validate_input(name)
        except InvalidInputError as e:
            print(f"{e}")
            sys.exit(1)

    def extract_first_name(self):
        parts = self.name.split(' ')
        return parts[0] if parts else None
    
    def extract_last_name(self):
        parts = self.name.split(' ')
        return ' '.join(parts[1:]) if len(parts) > 1 else None


"""
user_input = input("Enter a full name: ")

try:
    person = Person(user_input)
    print(person.extract_first_name())
    print(person.extract_last_name())

except InvalidInputError as e:
    print(f"{e}")
    

except Exception as e:
    print(f"{e}")
"""  
