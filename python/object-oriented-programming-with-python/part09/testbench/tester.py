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

#Needs to be added to settings.json one by one on mint.. Pretty sure that wasn't neccesary on ubuntu. Dont know why, ${workspaceFolder} doesn't work. Entirely IDE problem. Compiles fine
import fastest_car
import passing_submissions
import baby_centre
import lunchcard_and_paymentterminal
import comparing_properties
import pets 
import box_of_presents  
import shortest_person 
import car
import recording    
import weather_station  
import service_change   
import postcodes    
import list_helper  
import item_suitcase_and_cargo_hold




class MyTestCase(unittest.TestCase):
    def test_911(self):
        car1 = fastest_car.Car("Saab", 195)
        car2 = fastest_car.Car("Lada", 110)
        car3 = fastest_car.Car("Ferrari", 280)
        car4 = fastest_car.Car("Trabant", 85)

        cars = [car1, car2, car3, car4]
        fastestcar = fastest_car.fastest_car(cars)
        self.assertEqual(fastestcar.make, "Ferrari")

    def test_912(self):
        def test_passed_all_above_15():
            s1 = passing_submissions.ExamSubmission("Peter", 16)
            s2 = passing_submissions.ExamSubmission("Pippa", 19)
            s3 = passing_submissions.ExamSubmission("Paul", 15)
            s4 = passing_submissions.ExamSubmission("Phoebe", 20)
            s5 = passing_submissions.ExamSubmission("Persephone", 17)
            passes = passing_submissions.ExamSubmission.passed([s1, s2, s3, s4, s5], 15)
            self.assertEqual(len(passes), 5)

        def test_passed_some_equal_15():
            s1 = passing_submissions.ExamSubmission("Peter", 12)
            s2 = passing_submissions.ExamSubmission("Pippa", 19)
            s3 = passing_submissions.ExamSubmission("Paul", 15)
            s4 = passing_submissions.ExamSubmission("Phoebe", 9)
            s5 = passing_submissions.ExamSubmission("Persephone", 17)
            passes = passing_submissions.ExamSubmission.passed([s1, s2, s3, s4, s5], 15)
            self.assertEqual(len(passes), 3)

        def test_passed_all_below_15():
            s1 = passing_submissions.ExamSubmission("Peter", 12)
            s2 = passing_submissions.ExamSubmission("Pippa", 10)
            s3 = passing_submissions.ExamSubmission("Paul", 13)
            s4 = passing_submissions.ExamSubmission("Phoebe", 9)
            s5 = passing_submissions.ExamSubmission("Persephone", 14)
            passes = passing_submissions.ExamSubmission.passed([s1, s2, s3, s4, s5], 15)
            self.assertEqual(len(passes), 0)
        
        test_passed_all_above_15()
        test_passed_all_below_15()
        test_passed_some_equal_15()

    def test_913(self):
        def test_person_attributes():
            person = baby_centre.Person("Alice", 25, 160, 60)
            self.assertEqual(person.name, "Alice")
            self.assertEqual(person.age, 25)
            self.assertEqual(person.height, 160)
            self.assertEqual(person.weight, 60)
        
        def test_init_with_weigh_in():
            baby_centre_var = baby_centre.BabyCentre(5)
            self.assertEqual(baby_centre_var.weigh_in_count, 5)

        def test_feed():
            baby_centre_var = baby_centre.BabyCentre()
            person = baby_centre.Person("Bob", 30, 170, 70)
            baby_centre_var.feed(person)
            self.assertEqual(person.weight, 71)

        def test_weigh():
            baby_centre_var = baby_centre.BabyCentre()
            person = baby_centre.Person("Charlie", 35, 180, 80)
            initial_weight = person.weight
            weight_after_weighing = baby_centre_var.weigh(person)
            self.assertEqual(weight_after_weighing, initial_weight)
            self.assertEqual(baby_centre_var.weigh_in_count, 1)

        def test_weigh_ins():
            baby_centre_var = baby_centre.BabyCentre()
            baby_centre_var.weigh(baby_centre.Person("Dave", 40, 190, 90))
            baby_centre_var.weigh(baby_centre.Person("Eve", 45, 200, 100))
            self.assertEqual(baby_centre_var.weigh_ins(), 2)
        
        test_feed()
        test_init_with_weigh_in()
        test_person_attributes()
        test_weigh()
        test_weigh_ins()

    def test_914(self):
        def test_deposit_money():
            card = lunchcard_and_paymentterminal.LunchCard(50)
            card.deposit_money(20)
            self.assertEqual(card.balance, 70)

        def test_subtract_from_balance_enough_balance():
            card = lunchcard_and_paymentterminal.LunchCard(30)
            result = card.subtract_from_balance(20)
            self.assertTrue(result)
            self.assertEqual(card.balance, 10)

        def test_subtract_from_balance_not_enough_balance():
            card = lunchcard_and_paymentterminal.LunchCard(10)
            result = card.subtract_from_balance(20)
            self.assertFalse(result)
            self.assertEqual(card.balance, 10)
        
            def test_eat_lunch():
                terminal = lunchcard_and_paymentterminal.PaymentTerminal()
                terminal.eat_lunch(3)
                self.assertEqual(terminal.lunches, 1)
                self.assertEqual(terminal.funds, 998.5)

            def test_eat_lunch_not_enough_payment():
                terminal = lunchcard_and_paymentterminal.PaymentTerminal()
                change = terminal.eat_lunch(2)
                self.assertEqual(terminal.lunches, 0)
                self.assertEqual(change, 2)

            def test_eat_special():
                terminal = lunchcard_and_paymentterminal.PaymentTerminal()
                terminal.eat_special(5)
                self.assertEqual(terminal.specials, 1)
                self.assertEqual(terminal.funds, 995.7)

            def test_eat_special_not_enough_payment():
                terminal = lunchcard_and_paymentterminal.PaymentTerminal()
                change = terminal.eat_special(4)
                self.assertEqual(terminal.specials, 0)
                self.assertEqual(change, 4)

            def test_eat_lunch_lunchcard():
                terminal = lunchcard_and_paymentterminal.PaymentTerminal()
                card = lunchcard_and_paymentterminal.LunchCard(5)
                result = terminal.eat_lunch_lunchcard(card)
                self.assertTrue(result)
                self.assertEqual(terminal.lunches, 1)
                self.assertEqual(card.balance, 2.5)

            def test_eat_special_lunchcard():
                terminal = lunchcard_and_paymentterminal.PaymentTerminal()
                card = lunchcard_and_paymentterminal.LunchCard(7)
                result = terminal.eat_special_lunchcard(card)
                self.assertTrue(result)
                self.assertEqual(terminal.specials, 1)
                self.assertEqual(card.balance, 2.7)

            def test_deposit_money_on_card():
                terminal = lunchcard_and_paymentterminal.PaymentTerminal()
                card = lunchcard_and_paymentterminal.LunchCard(10)
                terminal.deposit_money_on_card(card, 20)
                self.assertEqual(card.balance, 30)
                self.assertEqual(terminal.funds, 1020)
            
            test_deposit_money()
            test_deposit_money_on_card()
            test_eat_lunch()
            test_subtract_from_balance_not_enough_balance()
            test_subtract_from_balance_enough_balance()
            test_eat_special()
            test_eat_lunch_lunchcard()
            test_eat_special_lunchcard()
            test_eat_lunch_not_enough_payment()
            test_eat_special_not_enough_payment()

    def test_915(self):
        def test_bigger():
            prop1 = comparing_properties.RealProperty(3, 100, 2000)
            prop2 = comparing_properties.RealProperty(4, 80, 1800)
            self.assertTrue(prop1.bigger(prop2))
            self.assertFalse(prop2.bigger(prop1))

        def test_price_difference():
            prop1 = comparing_properties.RealProperty(3, 100, 2000)
            prop2 = comparing_properties.RealProperty(4, 80, 1800)
            self.assertEqual(prop1.price_difference(prop2), 56000)
            self.assertEqual(prop2.price_difference(prop1), 56000)

        def test_more_expensive():
            prop1 = comparing_properties.RealProperty(3, 100, 2000)
            prop2 = comparing_properties.RealProperty(4, 80, 1800)
            self.assertTrue(prop1.more_expensive(prop2))
            self.assertFalse(prop2.more_expensive(prop1))

        test_bigger()
        test_price_difference()
        test_more_expensive()

    def test_921(self):
        def test_person_str():
            pet = pets.Pet("Buddy", "Dog")
            person = pets.Person("Alice", pet)
            self.assertEqual(str(person), "Alice, whose pal is Buddy, a Dog")

        test_person_str()

    def test_922(self):
        def test_add_present():
            present1 = box_of_presents.Present("Toy Car", 0.5)
            present2 = box_of_presents.Present("Doll", 0.3)
            box = box_of_presents.Box()
            box.add_present(present1)
            self.assertEqual(box.total_weight(), 0.5)
            box.add_present(present2)
            self.assertEqual(box.total_weight(), 0.8)

        test_add_present()

    def test_923(self):
        def test_is_empty():
            room = shortest_person.Room()
            self.assertTrue(room.is_empty())
            room.add(shortest_person.Person("Alice", 160))
            self.assertFalse(room.is_empty())

        def test_add():
            room = shortest_person.Room()
            person = shortest_person.Person("Bob", 170)
            room.add(person)
            self.assertEqual(len(room.persons), 1)
            self.assertIn(person, room.persons)

        def test_print_contents():
            room = shortest_person.Room([shortest_person.Person("Alice", 160), shortest_person.Person("Bob", 170)])
            with patch('sys.stdout', new_callable=io.StringIO) as captured_output:
                room.print_contents()
                output = captured_output.getvalue().strip()
                self.assertIn("There are 2 persons in the room, and their combined height is 330 cm", output)
                self.assertIn("Alice (160 cm)", output)
                self.assertIn("Bob (170 cm)", output)

        def test_shortest():
            room = shortest_person.Room([shortest_person.Person("Alice", 160), shortest_person.Person("Bob", 170), shortest_person.Person("Charlie", 150)])
            self.assertEqual(room.shortest(), "Charlie")
            empty_room = shortest_person.Room()
            self.assertIsNone(empty_room.shortest())

        def test_remove_shortest():
            room = shortest_person.Room([shortest_person.Person("Alice", 160), shortest_person.Person("Bob", 170), shortest_person.Person("Charlie", 150)])
            shortest_person_variable = room.remove_shortest()
            self.assertEqual(shortest_person_variable.name, "Charlie")
            self.assertEqual(len(room.persons), 2)

        test_is_empty()
        test_add()
        test_print_contents()
        test_shortest()
        test_remove_shortest()


    def test_931(self):
        def test_fill_up():
            car_variable = car.Car(tank=20)
            self.assertEqual(car_variable._Car__tank, 20)
            car_variable.fill_up()
            self.assertEqual(car_variable._Car__tank, 60)
            car_variable.fill_up()  # Filling up when tank is already full
            self.assertEqual(car_variable._Car__tank, 60)

        def test_drive():
            car_variable = car.Car(tank=60, odometer_reading=100)
            car_variable.drive(50)
            self.assertEqual(car_variable._Car__odometer_reading, 150)
            self.assertEqual(car_variable._Car__tank, 10)
            car_variable.drive(-10)  # Attempt to drive negative kilometers
            self.assertEqual(car_variable._Car__odometer_reading, 150)  # Odometer reading should remain unchanged
            self.assertEqual(car_variable._Car__tank, 10)  # Tank level should remain unchanged

        test_fill_up()
        test_drive()

    def test_932(self):
        def test_init():
            recording_variable = recording.Recording(10)
            self.assertEqual(recording_variable.length, 10)

            with self.assertRaises(ValueError):
                recording.Recording(-5)  # Testing negative length

        def test_setter():
            recording_variable = recording.Recording(10)
            recording_variable.length = 15
            self.assertEqual(recording_variable.length, 15)

            with self.assertRaises(ValueError):
                recording_variable.length = -5  # Testing negative length

        test_init()
        test_setter()

    def test_933(self):
        def test_add_observation():
            station = weather_station.WeatherStation("Station A")
            station.add_observation("Sunny")
            self.assertEqual(station.number_of_observations(), 1)

        def test_latest_observation():
            station = weather_station.WeatherStation("Station B")
            station.add_observation("Rainy")
            station.add_observation("Cloudy")
            self.assertEqual(station.latest_observation(), "Cloudy")

        def test_number_of_observations():
            station = weather_station.WeatherStation("Station C")
            station.add_observation("Snowy")
            station.add_observation("Foggy")
            station.add_observation("Windy")
            self.assertEqual(station.number_of_observations(), 3)

        test_add_observation()
        test_latest_observation()
        test_number_of_observations()

    def test_941(self):
        def test_deposit():
            account = service_change.BankAccount("John", "123456789", 100)
            account.deposit(50)
            #Take note, service charge is 150 * 0.01 = 1.5, so 150-1.5 = 148.5.
            #Service charge happens AFTER deposit, not before.
            self.assertEqual(account.balance, 148.5)

            with self.assertRaises(ValueError):
                account.deposit(-20)  # Testing negative deposit amount

        def test_withdraw():
            account = service_change.BankAccount("Alice", "987654321", 200)
            account.withdraw(100)
            self.assertEqual(account.balance, 99)  # Service charge applied

            with self.assertRaises(ValueError):
                account.withdraw(-50)  # Testing negative withdrawal amount

            with self.assertRaises(ValueError):
                account.withdraw(200)  # Withdrawal amount exceeds balance

        test_deposit()
        test_withdraw()

    def test_951(self):
        helsinki = postcodes.City('Helsinki')
        self.assertEqual(helsinki.name, 'Helsinki')
        self.assertEqual(postcodes.City.postcodes[helsinki.name], '00100')

    def test_952(self):
        def test_greatest_frequency():
            test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 2, 2, 2, 2, 2, 3, 3, 3, 3]
            result = list_helper.ListHelper.greatest_frequency(test_list)
            self.assertEqual(result, 2)

        def test_doubles():
            test_list = [1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5]
            result = list_helper.ListHelper.doubles(test_list)
            self.assertEqual(result, 5)

        test_greatest_frequency()
        test_doubles()

    def test_961(self):
        def test_item_getters():
            item1 = item_suitcase_and_cargo_hold.Item("Book", 15)
            self.assertEqual(item1.name, "Book")
            self.assertEqual(item1.weight, 15)
        
        def test_suitcase_methods():
            item1 = item_suitcase_and_cargo_hold.Item("Book", 5)
            item2 = item_suitcase_and_cargo_hold.Item("Phone", 35)
            item3 = item_suitcase_and_cargo_hold.Item("Brick", 65)
            suitcase1 = item_suitcase_and_cargo_hold.Suitcase(60)

            #Adding an item
            suitcase1.add_item(item1)
            self.assertEqual(suitcase1.weight,5)
            self.assertEqual(suitcase1.count_of_items, 1)
            
            #Count and weight get updated properly
            suitcase1.add_item(item2)
            self.assertEqual(suitcase1.weight,40)
            self.assertEqual(suitcase1.count_of_items, 2)

            #Heaviest item returns the heaviest object
            self.assertEqual(suitcase1.heaviest_item(), "Phone (35 kg)")

            #Suitcase maximum exceeded, adding item fails
            self.assertEqual(suitcase1.add_item(item3), "Overencumbered suitcase")
            #Make sure that nothing is added
            self.assertEqual(suitcase1.weight,40)
            self.assertEqual(suitcase1.count_of_items, 2)

        def test_suitcase_print_items():
            item1 = item_suitcase_and_cargo_hold.Item("Book", 5)
            item2 = item_suitcase_and_cargo_hold.Item("Phone", 35)
            suitcase1 = item_suitcase_and_cargo_hold.Suitcase(60)

            suitcase1.add_item(item1)
            suitcase1.add_item(item2)

            expected_output = "Book (5 kg)\nPhone (35 kg)\n"
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                suitcase1.print_items()
                self.assertEqual(fake_stdout.getvalue(), expected_output)
        
        def test_cargohold():
            item1 = item_suitcase_and_cargo_hold.Item("Book", 25)
            item2 = item_suitcase_and_cargo_hold.Item("Phone", 35)

            suitcase1 = item_suitcase_and_cargo_hold.Suitcase(60)
            suitcase2 = item_suitcase_and_cargo_hold.Suitcase(60)

            cargohold = item_suitcase_and_cargo_hold.CargoHold(100)

            suitcase1.add_item(item1)
            suitcase1.add_item(item2)

            suitcase2.add_item(item1)
            suitcase2.add_item(item2)

            cargohold.add_suitcase(suitcase1)

            #Make sure remaining space and cargo count gets updated properly
            self.assertEqual(cargohold.count, 1)
            self.assertEqual(cargohold.remaining_space, 40)

            #Test printing out contents of cargohold
            expected_output = "Book (25 kg)\nPhone (35 kg)\n"
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                cargohold.print_items()
                self.assertEqual(fake_stdout.getvalue(), expected_output)

            #Test running out of space
            self.assertEqual(cargohold.add_suitcase(suitcase2), "Not enough space for this suitcase")
            #Make sure remaining space and cargo count does not change
            self.assertEqual(cargohold.count, 1)
            self.assertEqual(cargohold.remaining_space, 40)


        test_item_getters()
        test_suitcase_methods()
        test_suitcase_print_items()
        test_cargohold()





if __name__ == '__main__':
    #print(sys.path)
    unittest.main()
