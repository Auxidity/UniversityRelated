import datetime

def list_years(dates: list) -> list:
    years = []
    for date in dates:
        try:
            date = datetime.date(*date)
        except ValueError:
            raise ValueError(f"{date} is not a valid date object.")
        
        years.append(date.year)

    years.sort()
    return years





date1 = (2019, 2, 3)
date2 = (2006, 10, 10)
date3 = (1993, 5, 9)
date4 = (1990, 2, 1)

dates = [date1, date2, date3, date4]
years = list_years(dates)
print(years)