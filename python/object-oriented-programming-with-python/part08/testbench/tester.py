import unittest, sys, os
from unittest.mock import patch, MagicMock

#Parent directory is not testbench dir but the one above it
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)



all_directories = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]

# Append each directory path to sys.path
for directory in all_directories:
    directory_path = os.path.join(parent_dir, directory)
    sys.path.append(directory_path)

#Needs to be added to settings.json one by one on mint.. Pretty sure that wasn't neccesary on ubuntu. Dont know why, ${workspaceFolder} doesn't work. Entirely IDE problem. Compiles fine
from book import Book
import three_classes
import define_class_pet
import the_older_book
import books_of_a_genre
import decreasing_counter
import first_and_last_name
import statistics_on_numbers
import stopwatch
import clock
import lunch_card
import series


class MyTestCase(unittest.TestCase):
    
    def test_831(self):
        book_instance = Book("Fluent Python", "Luciano Ramalho", "programming", 2015)

        self.assertEqual(book_instance.name, "Fluent Python")
        self.assertEqual(book_instance.author, "Luciano Ramalho")
        self.assertEqual(book_instance.genre, "programming")
        self.assertEqual(book_instance.year, 2015)
    
    def test_832(self):
        checklist_instance = three_classes.Checklist("Header", ["Entry"])
        self.assertIsInstance(checklist_instance.header, str)
        self.assertIsInstance(checklist_instance.author, list)

        customer_instance = three_classes.Customer("str", 0.2, 5)
        self.assertIsInstance(customer_instance.id, str)
        self.assertIsInstance(customer_instance.balance, float)
        self.assertIsInstance(customer_instance.discount, int)

        cable_instance = three_classes.Cable("model", 0.2, 1, False)
        self.assertIsInstance(cable_instance.model, str)
        self.assertIsInstance(cable_instance.length, float)
        self.assertIsInstance(cable_instance.max_speed, int)
        self.assertIsInstance(cable_instance.bidirectional, bool)
    
    def test_833(self):
        pet = define_class_pet.Pet("name", "species", 25)
        self.assertIsInstance(pet.name, str)
        self.assertIsInstance(pet.species, str)
        self.assertIsInstance(pet.year_of_birth, int)
    
        pet2 = define_class_pet.new_pet("Fluffy", "dog", 2017)
        self.assertIsInstance(pet2.name, str)
        self.assertIsInstance(pet2.species, str)
        self.assertIsInstance(pet2.year_of_birth, int)
    
    def test_834(self):
        book = the_older_book.Book("Norma", "Sofi Oksanen", "crime", 2015)
        book2 = the_older_book.Book("High Adventure", "Edmund Hillary", "autobiography", 1956)
        out = the_older_book.older_book(book, book2)
        self.assertTrue(out == "High Adventure is older, it was published in 1956")
    
    def test_835(self):
        python = books_of_a_genre.Book("Fluent Python", "Luciano Ramalho", "programming", 2015)
        everest = books_of_a_genre.Book("High Adventure", "Edmund Hillary", "autobiography", 1956)
        norma = books_of_a_genre.Book("Norma", "Sofi Oksanen", "crime", 2015)
        books = [python, everest, norma, books_of_a_genre.Book("The Snowman", "Jo Nesbø", "crime", 2007)]

        matches = books_of_a_genre.books_of_genre(books, "crime")
        #To prove all_books wouldn't return true
        all_books = all(book.genre == "crime" for book in books)
        self.assertTrue(matches)

    def test_841(self):
        counter = decreasing_counter.DecreasingCounter(25) #init 25
        counter.decrease()
        self.assertEqual(counter.value, 24)
        counter.set_to_zero()
        self.assertEqual(counter.value, 0)
        counter.reset_original_value()
        self.assertEqual(counter.value, 25)

    def test_842(self):
        person = first_and_last_name.Person("Minna Määttä")
        self.assertEqual(person.extract_first_name(), "Minna")
        self.assertEqual(person.extract_last_name(), "Määttä")

        self.assertTrue(first_and_last_name.validate_input("Minna Määttä"))
        self.assertTrue(first_and_last_name.validate_input("Minna-Ala Ala-Määttä"))
        #self.assertTrue(first_and_last_name.validate_input("Min-na Määttä")) #Raises error as it should

    def test_843(self):
        user_input = ["1","7", "2","3", "-1"]

        # Patch input function to simulate user input
        with patch('builtins.input', side_effect=user_input):
            count,sum,average,uneven,even = statistics_on_numbers.test()

        self.assertEqual(count, 4) 
        self.assertEqual(sum, 13)
        self.assertEqual(average, 3.25)
        self.assertEqual(uneven, 11)
        self.assertEqual(even, 2)
    
    def test_851(self):
        watch = stopwatch.Stopwatch()

        self.assertEqual(watch.minutes, 0)
        self.assertEqual(watch.seconds, 0)

        watch.tick()
        self.assertEqual(watch.minutes, 0)
        self.assertEqual(watch.seconds, 1)

        """ #To test if ticking from seconds to minutes works. It works, but takes 1 minute of run time every time if not commented out. Remove comments as neccesary.
        for _ in range (59):
            watch.tick()
        
        self.assertEqual(watch.minutes, 1)
        self.assertEqual(watch.seconds, 0)
        """

    def test_852(self):
        tclock = clock.Clock(23, 59, 55)
        self.assertEqual(tclock.hours, 23)
        self.assertEqual(tclock.minutes, 59)
        self.assertEqual(tclock.seconds, 55)

        for _ in range(6):
            tclock.tick()

        self.assertEqual(tclock.hours, 0)
        self.assertEqual(tclock.minutes, 0)
        self.assertEqual(tclock.seconds, 1)
        

        tclock.set(12, 5)

        self.assertEqual(tclock.hours, 12)
        self.assertEqual(tclock.minutes, 5)
        self.assertEqual(tclock.seconds, 0)

        

    def test_853(self):

        def test_rating():
            s = series.Series("Test", 5, ["Test"])
            s.rate(4)
            self.assertEqual(s.average_rating, 4)
        
        def test_minimum_grade():
            s1 = series.Series("Dexter", 8, ["Crime", "Drama", "Mystery", "Thriller"])
            s1.rate(5)
            s2 = series.Series("South Park", 24, ["Animation", "Comedy"])
            s2.rate(3)
            s3 = series.Series("Friends", 10, ["Romance", "Comedy"])
            s3.rate(2)
            series_list = [s1, s2, s3]
            result = series.minimum_grade(4.5, series_list)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].name, "Dexter")
        
        def test_includes_genre():
            s1 = series.Series("Dexter", 8, ["Crime", "Drama", "Mystery", "Thriller"])
            s2 = series.Series("South Park", 24, ["Animation", "Comedy"])
            s3 = series.Series("Friends", 10, ["Romance", "Comedy"])
            series_list = [s1, s2, s3]
            result = series.includes_genre("Comedy", series_list)
            self.assertEqual(len(result), 2)
            self.assertTrue(all("Comedy" in series.genres for series in result))
        
        test_rating()
        test_minimum_grade()
        test_includes_genre()


    def test_854(self):
        #Note, due to using floating point numbers, there happens something very interesting at line 206. AssertionError: 22.799999999999997 != 22.8 . I have an idea why, but since we're interested in the accuracy in 1 floating point integer, AssertAlmostEqual is good enough as solution.

        peters_card = lunch_card.LunchCard(20, "Peter")
        graces_card = lunch_card.LunchCard(30, "Grace")
        self.assertAlmostEqual(peters_card.balance, 20)
        self.assertAlmostEqual(graces_card.balance, 30)

        peters_card.eat_special()
        graces_card.eat_lunch()
        self.assertAlmostEqual(peters_card.balance, 15.4)
        self.assertAlmostEqual(graces_card.balance, 27.4)

        peters_card.deposit_money(20)
        graces_card.eat_special()
        self.assertAlmostEqual(peters_card.balance, 35.4)
        self.assertAlmostEqual(graces_card.balance, 22.8)

        peters_card.eat_lunch()
        peters_card.eat_lunch()
        graces_card.deposit_money(50)
        self.assertAlmostEqual(peters_card.balance, 30.2)
        self.assertAlmostEqual(graces_card.balance, 72.8)





if __name__ == '__main__':
    #print(sys.path)
    unittest.main()
    