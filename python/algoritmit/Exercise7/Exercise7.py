from collections import deque
#Task 1
class Stack:
    def __init__(self):
        self.stack = deque()

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            print("Stack is empty")
            return None
        
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            print("Stack is empty")
            return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
#Task1 end

#Task2
    
class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        print(item)
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        else:
            print("Queue is empty")
            return None
    
    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        else:
            print("Queue is empty")
            return None
        
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
#Task2 end
    
#Task3

class Student:
    students = []

    def __init__(self, name:str, age:int, living_location:str, siblings:str,length:int, hobby:str, math:int, english:int, finnish:int, average:float):
        self.name = name
        self.age = age
        self.living_location = living_location
        self.siblings = siblings
        self.length = length
        self.hobby = hobby
        self.math = math
        self.english = english
        self.finnish = finnish
        self.average = average
        
    
    def weighted_score(self):
        score = self.english * 1.5 + self.finnish * 2 + self.math * 1.5
        return score
    
    @staticmethod
    def passing(list:list, amount:int):
        sorted_students = sorted(list, key=lambda student: (student.average, student.weighted_score()), reverse=True)

        #Append to list
        passed_students = sorted_students[:amount]

        return passed_students
    
    @classmethod
    def add_student(self, student: 'Student'): #Forward declaration of class Student
        students.append(student)
#Task3 end
    
students = [
    Student("Jack", 15,"Varissuo, Turku","Younger sister", 175, "Football", 8, 9, 6, 8.4),
    Student("Joe", 16,"Pääskyvuori, Turku","Younger brother", 181, "Football", 9, 8, 8, 8.7),
    Student("Josh", 16,"Nummi, Turku","Older sister", 177, "Basketball", 9, 7, 7, 7.4),
    Student("James", 15,"Lauste, Turku","Older brother", 178, "Basketball", 8, 8, 8, 7.4)
]

passed_students = Student.passing(students, 3)
for student in passed_students:
    print(f"{student.name}: Score: {student.weighted_score()}, Average: {student.average}")