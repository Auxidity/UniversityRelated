class Person:
    def __init__(self, name=None, number=None, address=None):
        self.name_v = name if name is not None else []
        self.numbers_v = [number] if number is not None else []
        self.address_v = [address] if address is not None else []

    def add_number(self, number):
        self.numbers_v.append(number)

    def add_address(self, address):
        self.address_v.append(address)

    def add_name(self,name):
        if name not in self.name_v:
            self.name_v.append(name)

    def name(self):
        return self.name_v if self.name_v else "name unknown"

    def numbers(self):
        return ', '.join(self.numbers_v) if self.numbers_v else "number unknown"

    def address(self):
        return ', ' .join(self.address_v) if self.address_v else "address unknown"

class PhoneBook:
    def __init__(self):
        self.__persons = {}

    def add_number(self, name: str, number: str):
        if name not in self.__persons:
            # add a new dictionary entry with an empty list for the numbers
            person = Person(name)

            self.__persons[name] = person

        self.__persons[name].add_number(number)

    def get_entry(self, name: str):
        if not name in self.__persons:
            return None

        return self.__persons[name].numbers()
    
    def get_person(self, name: str):
        return self.__persons.get(name)
    
    def add_person(self, name, address=None):
        if name in self.__persons:
            # Update existing person's address
            self.__persons[name].add_address(address)
        else:
            # Create a new person with the provided name and address
            person = Person(name, address=address)
            self.__persons[name] = person

    # return all entries (in dictionary format)
    def all_entries(self):
        result = {}
        for name, person in self.__persons.items():
            result[name] = person.numbers()
        return result
    

class PhoneBookApplication:
    def __init__(self):
        self.__phonebook = PhoneBook()
       

    def help(self):
        print("commands: ")
        print("0 exit")
        print("1 add entry")
        print("2 search")
        print("3 add address")

    def add_entry(self):
        name = input("name: ")
        number = input("number: ")
        self.__phonebook.add_number(name, number)

    def search(self):
        name = input("name: ")
        person = self.__phonebook.get_person(name)
        
        if person is None:
            print("number unknown")
            print("address unknown")
            return

        print("Numbers:", person.numbers())
        address = person.address()
        print("Address:", address if address else "Not available")
    
    def add_address(self):
        name = input("name: ")
        address = input("address: ")
        self.__phonebook.add_person(name, address)


    # a method which gets executed as the program exits
    def exit(self):
        exit()

    def execute(self):
        self.help()
        while True:
            print("")
            command = input("command: ")
            if command == "0":

                self.exit()
                break
            elif command == "1":
                self.add_entry()
            elif command == "2":
                self.search()
            elif command =="3":
                self.add_address()
            else:
                self.help()


application = PhoneBookApplication()
#application.execute()
