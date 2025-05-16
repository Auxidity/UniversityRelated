class Course:
    def __init__(self, name=None, grade=None, credits=None):
        self.namev = name if name is not None else []
        self.gradev = [grade] if grade is not None else []
        self.creditsv = [credits] if credits is not None else []
    
    def name(self):
        return self.namev if self.namev else ""
    
    def grade(self):
        return self.gradev[0] if self.gradev else None
        
    def credits(self):
        return self.creditsv[0] if self.creditsv else None
    
    def add_name(self, name):
        self.namev.append(name)

    def add_grade(self, grade):
        if self.gradev:
            if grade > self.gradev[0]:
                self.gradev[0] = grade
        else:
            self.gradev.append(grade)
    
    def add_credits(self, credit):
        if not self.creditsv:
            self.creditsv.append(credit)



class CourseList:
    def __init__(self):
        self.__courses = {}

    def add_course(self, name: str, grade: str, credits: str):
        if name not in self.__courses:
            course = Course(name)

            self.__courses[name] = course
        else:
            course = self.__courses[name]    

        course.add_grade(grade)
        
        
        course.add_credits(credits)

    
    def get_course(self, name: str):
        if not name in self.__courses:
            return None
        
        return self.__courses[name].grade(), self.__courses[name].credits()
    
    def mean_grades(self):
        all_grades = []
        for course in self.__courses.values():
            if isinstance(course.grade(), list):
                all_grades.extend(map(float, course.grade()))
            else:
                all_grades.append(float(course.grade()))  # Convert single grade to float

        if not all_grades:
            return None

        mean = sum(all_grades) / len(all_grades)
        return mean
    
    def sum_credits(self):
        sum_cred = 0

        for course in self.__courses.values():
            if isinstance(course.credits(), list):
                sum_cred += sum(map(int, course.credits()))
            else:
                sum_cred += int(course.credits())  # Convert single credit to int

        return sum_cred



class App:
    def __init__(self):
        self.__courselist = CourseList()
    
    def help(self):
        print("commands: ")
        print("0 exit")
        print("1 add course")
        print("2 get course data")
        print("3 statistics")
    
    def exit(self):
        exit()

    def add_course(self):
        name = input("Name of the course: ")


        if name in self.__courselist._CourseList__courses:
            grade_valid = False
            credits = 2 #Doesn't matter what is used here, it won't be used due to how add_course works in CourseList. Only provided so that last line won't give an error.
            while not grade_valid:
                try:
                    grade = int(input("grade: "))
                    if 0 <= grade <= 5:
                        grade_valid = True
                    else:
                        print("Invalid input. Grade must be between 0 & 5")
                except ValueError:
                    print("Invalid input, please enter a number between 0 & 5")


        else:    
            grade_valid = False
            while not grade_valid:
                try:
                    grade = int(input("grade: "))
                    if 0 <= grade <= 5:
                        grade_valid = True
                    else:
                        print("Invalid input. Grade must be between 0 & 5")
                except ValueError:
                    print("Invalid input, please enter a number between 0 & 5")

            cred_valid = False    
            while not cred_valid:
                try:
                    credits = int(input("credits: "))
                    if credits >= 0:
                        cred_valid = True
                    else:
                        print("Invalid input, credits must be above 0")
                except ValueError:
                    print("Invalid input, please enter an integer above 0")

        self.__courselist.add_course(name,grade,credits)
    
    def search(self):
        name = input("course: ")
        course_name = self.__courselist.get_course(name)

        if course_name is None:
            print("no entry for this course")
            return
        
        grades, credits = self.__courselist.get_course(name)
        print(f"{name} ({credits} cr) grade {grades}")
    
    def statistics(self):
        mean_grade = self.__courselist.mean_grades()
        credit_sum = self.__courselist.sum_credits()
        num_courses = len(self.__courselist._CourseList__courses)

        if mean_grade is not None:
            print("Mean: {:.2f}".format(mean_grade))
        else:
            print("No grades available")
        print(f"{format(num_courses)} completed courses, a total of {format(credit_sum)} credits")

        #Grade matrix
        print("\nGrade distribution:")
        for grade in range(5,0, -1):
            grade_count = sum(1 for course in self.__courselist._CourseList__courses.values() if grade == course.grade())
            print(f"{grade}:{'x' * grade_count}")

    def execute(self):
        self.help()
        while True:
            print("")
            command = input("command: ")
            if command == "0":
                self.exit()
                break
            elif command == "1":
                print("\n")
                self.add_course()
            elif command == "2":
                print("\n")
                self.search()
            elif command == "3":
                print("\n")
                self.statistics()
            else:
                print("\n")
                self.help()


alt = App()
#alt.execute()
