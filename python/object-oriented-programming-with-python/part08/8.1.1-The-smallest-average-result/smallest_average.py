def calculate_average(person: dict):
        result_sum = sum(value for key, value in person.items() if key != 'name')
        num_results = len(person) -1
        average = result_sum / num_results if num_results > 0 else 0
        return average




def smallest_average(*people: dict):
        averages = {}


        for person in people:
                name = person.get('name', '')
                avg = calculate_average(person)
                averages[name] = avg



        min_average_name = min(averages, key=averages.get)
        smallest_avg = min(averages.values())

        return smallest_avg, min_average_name
        
    
#Test 
person1 = {"name": "Mary", "result1": 2, "result2": 3, "result3": 3}
person2 = {"name": "Gary", "result1": 5, "result2": 1, "result3": 8}
person3 = {"name": "Harry", "result1": 3, "result2": 1, "result3": 19}

result, name = smallest_average(person1, person2, person3)

for person in (person1, person2, person3):
        if person['name'] == name:
                print(person)
                break

#print(f"result for smallest average is {result} and is {name}'s")
