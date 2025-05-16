class PhoneBook:
    def __init__(self):
        self.__persons = {}

    def add_number(self, name: str, number: str):
        if not name in self.__persons:
            # add a new dictionary entry with an empty list for the numbers
            self.__persons[name] = []

        self.__persons[name].append(number)

    def get_numbers(self, name: str):
        if not name in self.__persons:
            return None

        return self.__persons[name]
    
    def get_name(self, number: str):
        names = []
        #Iterates over the numbers and appends matches to a seperate list. Returns the list of matches at the end
        for name, numbers in self.__persons.items(): 
            if number in numbers:
                names.append(name)
        return names

    # return all entries (in dictionary format)
    def all_entries(self):
        return self.__persons
    

class PhoneBookApplication:
    def __init__(self):
        self.__phonebook = PhoneBook()
        self.__filehandler = FileHandler("phonebook.txt")

        # add the names and numbers from the file to the phone book
        for name, numbers in self.__filehandler.load_file().items():
            for number in numbers:
                self.__phonebook.add_number(name, number)

    def help(self):
        print("commands: ")
        print("0 exit")
        print("1 add entry")
        print("2 search")
        print("3 search by number")

    def add_entry(self):
        name = input("name: ")
        number = input("number: ")
        self.__phonebook.add_number(name, number)

    def search(self):
        name = input("name: ")
        numbers = self.__phonebook.get_numbers(name)
        if numbers == None:
            print("number unknown")
            return
        
        for number in numbers:
            print(number)
    
    def searchnum(self):
        number = input("number: ")
        names = self.__phonebook.get_name(number)
        if not names:
            print("Name unknown")
            return
        for name in names:
            print(name)

    # a method which gets executed as the program exits
    def exit(self):
        self.__filehandler.save_file(self.__phonebook.all_entries())

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
                self.searchnum()
            else:
                self.help()

class FileHandler():
    def __init__(self, filename):
        self.__filename = filename

    def load_file(self):
        names = {}
        try:
            with open(self.__filename) as f:
                for line in f:
                    parts = line.strip().split(';')
                    name, *numbers = parts
                    names[name] = numbers
        except FileNotFoundError:
            pass

        return names

    def save_file(self, phonebook: dict):
        with open(self.__filename, "w") as f:
            for name, numbers in phonebook.items():
                line = [name] + numbers
                f.write(";".join(line) + "\n")



#application = PhoneBookApplication()
#application.execute()
