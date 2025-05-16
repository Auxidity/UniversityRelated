class SimpleDate:
    def __init__(self, day, month, year) -> None:
        self.day = day
        self.month = month
        self.year = year

    def __str__(self) -> str:
        return f"{self.day}.{self.month}.{self.year}"

    def __eq__(self, another):
        if isinstance(another, SimpleDate):
            return (self.day == another.day) and \
            (self.month == another.month) and \
            (self.year == another.year)
        return False
    
    def __gt__(self, another):
        if isinstance(another, SimpleDate):
            if self.year > another.year:
                return True
            elif self.year == another.year:
                if self.month > another.month:
                    return True
                elif self.month == another.month:
                    return self.day > another.day
        return False
        
    def __add__(self, another):
        if isinstance(another, int):
            new_date = SimpleDate(self.day, self.month, self.year)
            days_to_add = another
            days_in_a_month = 30

            while days_to_add > 0:
                #Overflow from days to months
                if new_date.day + days_to_add > days_in_a_month:
                    days_to_add -= (days_in_a_month - new_date.day + 1) #+1 because we start counting days from 1 instead of 0
                    new_date.day = 1
                    new_date.month += 1

                    #Overflow from months to years
                    if new_date.month > 12:
                        new_date.month = 1
                        new_date.year += 1
                
                #No overflow from days to months, simply add days.
                else:
                    new_date.day += days_to_add
                    days_to_add = 0
            
            return new_date

    def __sub__(self, another):
        if isinstance(another, SimpleDate):
            new_date = SimpleDate(self.day, self.month, self.year)
            new_date_daytotal = new_date.day + new_date.month * 30 + new_date.year * 360
            compared_to_daytotal = another.day + another.month * 30 + another.year * 360

            if new_date_daytotal > compared_to_daytotal:
                return new_date_daytotal - compared_to_daytotal
            elif new_date_daytotal < compared_to_daytotal:
                return compared_to_daytotal - new_date_daytotal
            else:
                return 0

