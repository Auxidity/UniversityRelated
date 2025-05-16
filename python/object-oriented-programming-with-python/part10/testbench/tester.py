import unittest, sys, os, io
from unittest.mock import patch, MagicMock

#Parent directory is not testbench dir but the one above it
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



all_directories = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]

# Append each directory path to sys.path
for directory in all_directories:
    directory_path = os.path.join(parent_dir, directory)
    sys.path.append(directory_path)


#Imports for testing
import laptop_computer
import games
import rectangle
import word_game
import supergroup
import magicpotion
import money
import simple_date
import iterable_shopping_list
import phone_book_v1
import phone_book_v2
import course_records


class MyTestCase(unittest.TestCase):
    def test_1011(self):
        laptop = laptop_computer.LaptopComputer("Laptop", 25, 5)
        self.assertEqual(laptop.model, "Laptop")
        self.assertEqual(laptop.speed, 25)
        self.assertEqual(laptop.weight, 5)

    def test_1012(self):
        def test_add_game():
            warehouse = games.GameWarehouse()
            game = games.ComputerGame("Game1", "Publisher1", 2000)
            warehouse.add_game(game)
            self.assertEqual(len(warehouse.list_games()), 1)

        def test_list_games():
            warehouse = games.GameWarehouse()
            game1 = games.ComputerGame("Game1", "Publisher1", 2000)
            game2 = games.ComputerGame("Game2", "Publisher2", 1995)
            warehouse.add_game(game1)
            warehouse.add_game(game2)
            games_variable = warehouse.list_games()
            self.assertEqual(len(games_variable), 2)
            self.assertTrue(all(isinstance(game, games.ComputerGame) for game in games_variable))

        def test_add_games_museum():
            museum = games.GameMuseum()
            game1 = games.ComputerGame("Game1", "Publisher1", 2000)
            game2 = games.ComputerGame("Game2", "Publisher2", 1985)
            game3 = games.ComputerGame("Game3", "Publisher3", 1995)
            museum.add_game(game1)
            museum.add_game(game2)
            museum.add_game(game3)
            filtered_games = museum.list_games()
            self.assertEqual(len(filtered_games), 1)
            self.assertEqual(filtered_games[0].name, "Game2")

        # Call the nested test functions
        test_add_game()
        test_list_games()
        test_add_games_museum()

    def test_1013(self):
        def test_rectangle_area():
            rectangle_variable = rectangle.Rectangle(4, 5)
            assert rectangle_variable.area() == 20

        def test_square_area():
            square = rectangle.Square(4)
            assert square.area() == 16

        # Call the nested test functions
        test_rectangle_area()
        test_square_area()

    def test_1014(self):
        def test_round_winner_word_game():
            game = word_game.WordGame(1)
            winner = game.round_winner("hello", "world")
            self.assertIn(winner, [1, 2])

        def test_round_winner_longest_word_tie():
            game = word_game.LongestWord(1)
            winner = game.round_winner("hello", "world")
            self.assertIn(winner, [0])
        
        def test_round_winner_longest_word():
            game = word_game.LongestWord(1)
            winner = game.round_winner("mokoko", "world")
            self.assertIn(winner, [1])

        def test_round_winner_most_vowels():
            game = word_game.MostVowels(1)
            winner = game.round_winner("hello", "world")
            self.assertIn(winner, [1])

        def test_round_winner_rock_paper_scissors():
            game = word_game.RockPaperScissors(1)
            winner = game.round_winner("rock", "paper")
            self.assertIn(winner, [2])
            winner2 = game.round_winner("rock", "scissor")
            self.assertIn(winner2, [1])
            winner3 = game.round_winner("paper", "scissor")
            self.assertIn(winner3, [2])
            
            #Tie cases
            winner4 = game.round_winner("scissor", "scissor")
            self.assertIn(winner4, [0])
            winner5 = game.round_winner("rock", "rock")
            self.assertIn(winner5, [0])
            winner6 = game.round_winner("paper", "paper")
            self.assertIn(winner6, [0])

        def test_mocked_inputs():
            with patch('builtins.input', side_effect=['rock', 'rock', 'scissor', 'rock','paper','rock']), \
                io.StringIO() as mock_stdout:
                sys.stdout = mock_stdout #Redirect stdout for the game to keep terminal clean
                game = word_game.RockPaperScissors(3)
                game.play()
                sys.stdout = sys.__stdout__ #Restore stdout

                self.assertEqual(game.wins1, 1)
                self.assertEqual(game.wins2, 1)

        # Call the nested test functions
        test_round_winner_word_game()
        test_round_winner_longest_word_tie()
        test_round_winner_longest_word()
        test_round_winner_most_vowels()
        test_round_winner_rock_paper_scissors()
        test_mocked_inputs()

    def test_1021(self):
        def test_superhero_str():
            hero = supergroup.SuperHero("Spiderman", "Wall crawling, Web-slinging")
            
            self.assertEqual(hero.__str__(), "Spiderman, superpowers: Wall crawling,  Web-slinging")

        def test_supergroup_print(): #Printing the supergroup also tests both getters
            group = supergroup.SuperGroup("Avengers", "New York")
            hero1 = supergroup.SuperHero("Iron Man", "Armor suit")
            hero2 = supergroup.SuperHero("Thor", "God of Thunder")
            group.add_member(hero1)
            group.add_member(hero2)

            with self.subTest():
                expected_output = "Avengers, New York\nMembers:\nIron Man, superpowers: Armor suit\nThor, superpowers: God of Thunder\n"
                with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                    group.print_group()
                    self.assertEqual(mock_stdout.getvalue(), expected_output)

        # Call the nested test functions
        test_superhero_str()
        test_supergroup_print()

    def test_1022(self):
        def test_magic_potion_recipe():
            potion = magicpotion.MagicPotion("Healing Potion")
            potion.add_ingredient("Herb", 10)
            potion.add_ingredient("Water", 20)
            expected_output = "Healing Potion:\nHerb 10 grams\nWater 20 grams\n"
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                potion.print_recipe()
                self.assertEqual(mock_stdout.getvalue(), expected_output)

        def test_secret_magic_potion_recipe():
            secret_potion = magicpotion.SecretMagicPotion("Invisibility Potion", "secret")
            secret_potion.add_ingredient("Moon Dust", 5, "secret")
            with self.assertRaises(ValueError):
                secret_potion.add_ingredient("Sun Essence", 10, "wrong_password")  # Attempt with wrong password

            expected_output = "Invisibility Potion:\nMoon Dust 5 grams\n"
            with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
                secret_potion.print_recipe("secret")
                self.assertEqual(mock_stdout.getvalue(), expected_output)

                with self.assertRaises(ValueError):
                    secret_potion.print_recipe("wrong_password")  # Attempt with wrong password


        # Call the nested test functions
        test_magic_potion_recipe()
        test_secret_magic_potion_recipe()

    def test_1031(self):
        def test_money_str():
            money1 = money.Money(10, 50)
            self.assertEqual(str(money1), "10.50")

        def test_money_equality():
            money1 = money.Money(10, 50)
            money2 = money.Money(10, 50)
            money3 = money.Money(10, 60)
            self.assertEqual(money1, money2)
            self.assertNotEqual(money1, money3)

        def test_money_comparison():
            money1 = money.Money(10, 50)
            money2 = money.Money(11, 40)
            money3 = money.Money(10, 60)
            self.assertTrue(money2 > money1)
            self.assertFalse(money1 > money2)
            self.assertTrue(money1 < money2)
            self.assertFalse(money2 < money1)
            self.assertTrue(money1 == money1)
            self.assertFalse(money1 == money3)

        def test_money_addition():
            money1 = money.Money(10, 50)
            money2 = money.Money(11, 40)
            money3 = money.Money(0, 50)
            money_sum = money1 + money2
            money_sum2 = money_sum + money3

            money_sum_str = str(money_sum)
            euros, cents = map(int, money_sum_str.split('.'))

            money_sum_str2 = str(money_sum2)
            euros2, cents2 = map(int, money_sum_str2.split('.'))

            self.assertEqual(euros, 21)
            self.assertEqual(cents, 90)

            self.assertEqual(euros2, 22)
            self.assertEqual(cents2, 40)

        def test_money_subtraction():
            money1 = money.Money(10, 50)
            money2 = money.Money(11, 40)
            money3 = money.Money(0, 50)
            money_sub = money2 - money1
            self.assertEqual(money_sub, money.Money(0, 90))
            with self.assertRaises(ValueError):
                money1 - money2
            self.assertEqual(money2 - money3, money.Money(10, 90))

        # Call the nested test functions
        test_money_str()
        test_money_equality()
        test_money_comparison()
        test_money_addition()
        test_money_subtraction()

    def test_1032(self):
        def test_simple_date_str():
            date = simple_date.SimpleDate(15, 3, 2022)
            self.assertEqual(str(date), "15.3.2022")

        def test_simple_date_equality():
            date1 = simple_date.SimpleDate(15, 3, 2022)
            date2 = simple_date.SimpleDate(15, 3, 2022)
            date3 = simple_date.SimpleDate(16, 3, 2022)
            self.assertEqual(date1, date2)
            self.assertNotEqual(date1, date3)

        def test_simple_date_comparison():
            date1 = simple_date.SimpleDate(15, 3, 2022)
            date2 = simple_date.SimpleDate(16, 3, 2022)
            date3 = simple_date.SimpleDate(15, 4, 2022)
            self.assertTrue(date2 > date1)
            self.assertFalse(date1 > date2)
            self.assertTrue(date3 > date1)
            self.assertFalse(date1 > date3)
            self.assertFalse(date1 > date1)

        def test_simple_date_addition():
            date = simple_date.SimpleDate(15, 3, 2022)
            new_date = date + 10
            self.assertEqual(new_date, simple_date.SimpleDate(25, 3, 2022))

        def test_simple_date_subtraction():
            date1 = simple_date.SimpleDate(15, 3, 2022)
            date2 = simple_date.SimpleDate(10, 3, 2022)
            date3 = simple_date.SimpleDate(20, 3, 2022)
            self.assertEqual(date1 - date2, 5)
            self.assertEqual(date2 - date1, 5)
            self.assertEqual(date3 - date1, 5)

        # Call the nested test functions
        test_simple_date_str()
        test_simple_date_equality()
        test_simple_date_comparison()
        test_simple_date_addition()
        test_simple_date_subtraction()

    def test_1033(self):
        def test_shopping_list_add():
            shopping_list = iterable_shopping_list.ShoppingList()
            shopping_list.add("bananas", 10)
            shopping_list.add("apples", 5)
            shopping_list.add("pineapple", 1)
            self.assertEqual(shopping_list.number_of_items(), 3)

        def test_shopping_list_item_amount():
            shopping_list = iterable_shopping_list.ShoppingList()
            shopping_list.add("bananas", 10)
            shopping_list.add("apples", 5)
            shopping_list.add("pineapple", 1)
            self.assertEqual(shopping_list.amount(1), 10)
            self.assertEqual(shopping_list.amount(2), 5)
            self.assertEqual(shopping_list.amount(3), 1)

        def test_shopping_list_item_index_out_of_range():
            shopping_list = iterable_shopping_list.ShoppingList()
            shopping_list.add("bananas", 10)
            shopping_list.add("apples", 5)
            shopping_list.add("pineapple", 1)
            with self.assertRaises(IndexError):
                shopping_list.item(0)
            with self.assertRaises(IndexError):
                shopping_list.amount(0)
            with self.assertRaises(IndexError):
                shopping_list.item(4)
            with self.assertRaises(IndexError):
                shopping_list.amount(4)

        def test_total_units():
            shopping_list = iterable_shopping_list.ShoppingList()
            shopping_list.add("bananas", 10)
            shopping_list.add("apples", 5)
            shopping_list.add("pineapple", 1)
            
            total = iterable_shopping_list.total_units(shopping_list)
            expected_total = 16  # 10 + 5 + 1
            self.assertEqual(total, expected_total)

        def test_shopping_list_stop_iteration():
            shopping_list = iterable_shopping_list.ShoppingList()
            shopping_list.add("bananas", 10)
            shopping_list.add("apples", 5)
            shopping_list.add("pineapple", 1)
            
            iterator = iter(shopping_list)

            keep_iterating = True
            while keep_iterating:
                try:
                    next(iterator)
                except StopIteration as e:
                    self.assertEqual(str(e), "End of iteration")
                    keep_iterating = False

        # Call the nested test functions
        test_shopping_list_add()
        test_shopping_list_item_amount()
        test_shopping_list_item_index_out_of_range()
        test_shopping_list_stop_iteration()
        test_total_units()
    
    def test_1041(self):
        def test_phone_book_add_number():
            phone_book = phone_book_v1.PhoneBook()
            phone_book.add_number("John", "12345")
            phone_book.add_number("John", "67890")
            phone_book.add_number("Alice", "54321")
            self.assertEqual(phone_book.get_numbers("John"), ["12345", "67890"])
            self.assertEqual(phone_book.get_numbers("Alice"), ["54321"])
            self.assertEqual(phone_book.get_numbers("Bob"), None)

        def test_phone_book_get_name():
            phone_book = phone_book_v1.PhoneBook()
            phone_book.add_number("John", "12345")
            phone_book.add_number("Alice", "54321")
            phone_book.add_number("Alice", "98765")
            self.assertEqual(phone_book.get_name("12345"), ["John"])
            self.assertEqual(phone_book.get_name("54321"), ["Alice"])
            self.assertEqual(phone_book.get_name("98765"), ["Alice"])
            self.assertEqual(phone_book.get_name("99999"), [])

        def test_phone_book_application_navigation():
            # Create a PhoneBook object and a PhoneBookApplication object
            phone_book = phone_book_v1.PhoneBook()
            app = phone_book_v1.PhoneBookApplication()
            app.__phonebook = phone_book

            #Add entry commands
            commands = [
                "Alice",
                "12345"
            ]

            #Test adding an entry
            with patch('builtins.input', side_effect=commands):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.add_entry()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "")

            #Test searching existing entry using name
            with patch('builtins.input', side_effect=["Alice"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "12345\n")

            #Test searching non-existing entry using name
            with patch('builtins.input', side_effect=["Bob"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "number unknown\n")   

            #Test searching existing entry using number
            with patch('builtins.input', side_effect=["12345"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.searchnum()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "Alice\n")

            #Test searching non-existing entry using number
            with patch('builtins.input', side_effect=["99999"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.searchnum()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "Name unknown\n") 


        def setUp():
            self.test_file = "test_phonebook.txt"
            self.file_handler = phone_book_v1.FileHandler(self.test_file)
            
            #If you want to inspect the test file, this line removes the file on consequent runs so that tests work
            if os.path.exists(self.test_file):
                os.remove(self.test_file)
            
        #For cleaning up so that there are no ghost files. Comment out if you want to inspect test file and play around with FileHandler functions
        def tearDown():
            if os.path.exists(self.test_file):
                os.remove(self.test_file)

        def test_load_file():
            # Test loading from a non-existent file
            self.assertEqual(self.file_handler.load_file(), {})

            # Create a test file
            with open(self.test_file, "w") as f:
                f.write("Alice;123\nBob;456")

            # Test loading from the created file
            expected_output = {"Alice": ["123"], "Bob": ["456"]}
            self.assertEqual(self.file_handler.load_file(), expected_output)

        def test_save_file():
            # Prepare data for testing
            phonebook_data = {"Alice": ["123"], "Bob": ["456"]}

            # Save the data to a file
            self.file_handler.save_file(phonebook_data)

            # Read the saved file
            with open(self.test_file, "r") as f:
                saved_data = f.read()

            # Test if the saved data matches the expected format
            expected_output = "Alice;123\nBob;456\n"
            self.assertEqual(saved_data, expected_output)

        # Run nested filehandler functions
        setUp()
        test_load_file()
        test_save_file()
        tearDown()

        #Run nested App functions
        test_phone_book_add_number()
        test_phone_book_get_name()
        test_phone_book_application_navigation()
        

    def test_1042(self):
        def test_add_number():
            # Test adding a number to a new person
            phonebook = phone_book_v2.PhoneBook()
            phonebook.add_number("Alice", "12345")
            self.assertEqual(phonebook.get_entry("Alice"), '12345')

            # Test adding a number to an existing person
            phonebook.add_number("Alice", "67890")
            self.assertEqual(phonebook.get_entry("Alice"), '12345, 67890')

        def test_add_person():
            # Test adding a person with address
            phonebook = phone_book_v2.PhoneBook()
            phonebook.add_person("Bob", "123 Main St")
            self.assertEqual(phonebook.get_person("Bob").address(), "123 Main St")

            # Test adding a person without address
            phonebook.add_person("Charlie")
            self.assertEqual(phonebook.get_person("Charlie").address(), "address unknown")

        def test_search():
            # Test searching for an existing person
            phonebook = phone_book_v2.PhoneBook()
            phonebook.add_number("Alice", "12345")
            self.assertEqual(phonebook.get_person("Alice").numbers(), '12345')

            # Test searching for a non-existing person
            self.assertIsNone(phonebook.get_person("Bob"))

        def test_phone_book_application_navigation():
            # Create a PhoneBook object and a PhoneBookApplication object
            phone_book = phone_book_v2.PhoneBook()
            app = phone_book_v2.PhoneBookApplication()
            app.__phonebook = phone_book

            #Add entry commands
            commands = [
                "Alice",
                "12345"
            ]

            #Add entry commands for 2nd number
            commands2 = [
                "Alice",
                "54321"
            ]

            #add address commands
            commands_address = [
                "Alice",
                "address"
            ]

            #add address commands for 2nd address
            commands_address2 = [
                "Alice",
                "address2"
            ]

            #Test adding an entry
            with patch('builtins.input', side_effect=commands):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.add_entry()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "")

            #Test searching existing entry using name that doesn't have an address
            with patch('builtins.input', side_effect=["Alice"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "Numbers: 12345\nAddress: address unknown\n")

            #Test searching non-existing entry using name
            with patch('builtins.input', side_effect=["Bob"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "number unknown\naddress unknown\n")   

            #Test adding an address
            with patch('builtins.input', side_effect=commands_address):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.add_address()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "")   
            
            #Test searching existing entry using name that has an address
            with patch('builtins.input', side_effect=["Alice"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "Numbers: 12345\nAddress: address\n")
            
            #Adding additional number
            with patch('builtins.input', side_effect=commands2):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.add_entry()
            #Adding additional address
            with patch('builtins.input', side_effect=commands_address2):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.add_address()


            #Test searching existing entry using name that has multiple numbers and addresses.
            with patch('builtins.input', side_effect=["Alice"]):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "Numbers: 12345, 54321\nAddress: address, address2\n")

        test_add_number()
        test_add_person()
        test_search()
        test_phone_book_application_navigation()

    def test_1043(self):
        def test_course_init():
            # Test initialization of Course object with default values
            course = course_records.Course()
            self.assertEqual(course.name(), "")
            self.assertIsNone(course.grade())
            self.assertIsNone(course.credits())

            # Test initialization of Course object with specific values
            course = course_records.Course("Math", 4, 3)
            self.assertEqual(course.name(), "Math")
            self.assertEqual(course.grade(), 4)
            self.assertEqual(course.credits(), 3)

        def test_course_methods():
            course = course_records.Course()

            # Test adding name, grade, and credits
            course.add_name("Physics")
            self.assertEqual(course.name(), ['Physics'])

            course.add_grade(3)
            self.assertEqual(course.grade(), 3)

            course.add_credits(4)
            self.assertEqual(course.credits(), 4)

            # Test adding grade higher than existing grade
            course.add_grade(5)
            self.assertEqual(course.grade(), 5)

            # Test adding credits when already present
            course.add_credits(2)
            self.assertEqual(course.credits(), 4)  # Should remain unchanged

        def test_courselist_init():
            # Test initialization of CourseList object
            course_list = course_records.CourseList()
            self.assertEqual(course_list._CourseList__courses, {})  # Accessing private attribute


        def test_courselist_methods():
            course_list = course_records.CourseList()

            # Test adding courses
            course_list.add_course("Math", 4, 3)
            course_list.add_course("Physics", 3, 4)

            self.assertEqual(course_list.get_course("Math"), (4, 3))
            self.assertEqual(course_list.get_course("Physics"), (3, 4))
            self.assertIsNone(course_list.get_course("Chemistry"))  # Non-existent course

            # Test mean grades and sum credits
            self.assertAlmostEqual(course_list.mean_grades(), 3.5)
            self.assertEqual(course_list.sum_credits(), 7)

        def test_courselist_app_navigation():
            # Create a PhoneBook object and a PhoneBookApplication object
            course_list = course_records.CourseList()
            app = course_records.App()
            app.__courselist = course_list

            #Commands for adding a course
            commands = [
                "test_course",
                "5",
                "2"
            ]

            #Test adding an entry
            with patch('builtins.input', side_effect=commands):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.add_course()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "")

            #Search the course
            commands2 = [
                "test_course"
            ]

            #Test searching an existing course
            with patch('builtins.input', side_effect=commands2):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "test_course (2 cr) grade 5\n")

            #Search a course that doesn't exist
            commands3 = [
                "test_course2"
            ]

            #Test searching an existing course
            with patch('builtins.input', side_effect=commands3):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "no entry for this course\n")

            #Commands for adding a course with invalid inputs (Due to the eternal loop, we do give at end valid outputs)
            commands4 = [
                "test_course2",
                "6",    #Not valid grade
                "testing",  #Not valid grade
                "4",    #Valid grade
                "-3",   #Not valid credits
                "testing again",    #Not valid credits
                "3"     #Valid credits
            ]

            #Test adding above course and get the correct error messages
            with patch('builtins.input', side_effect=commands4):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.add_course()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "Invalid input. Grade must be between 0 & 5\nInvalid input, please enter a number between 0 & 5\nInvalid input, credits must be above 0\nInvalid input, please enter an integer above 0\n")

            #Verify that when searched for it is found
            with patch('builtins.input', side_effect=['test_course2']):
                with patch('sys.stdout', new=io.StringIO()) as fake_out:
                    app.search()
                    output = fake_out.getvalue()
                    self.assertEqual(output, "test_course2 (3 cr) grade 4\n")

            expected_output = "Mean: 4.50\n2 completed courses, a total of 5 credits\n\nGrade distribution:\n5:x\n4:x\n3:\n2:\n1:\n"

            #Test the statistics function
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                app.statistics()
                output = fake_out.getvalue()
                self.assertEqual(output, expected_output)

        # Execute the nested test functions
        test_course_init()
        test_course_methods()
        test_courselist_init()
        test_courselist_methods()
        test_courselist_app_navigation()




if __name__ == '__main__':
    #print(sys.path)
    unittest.main()