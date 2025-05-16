class Series:
    def __init__(self,name:str, seasons:int,genres:str,rating=None):
        self.name = name
        self.seasons = seasons
        self.genres = genres
        self.rating = []
        self.average_rating = 0

        if rating is not None:
            self.add_rating(rating)

    def rate(self, rating: int):
        self.rating.append(rating)
        self.update_rating()
        
    def update_rating(self):
        if len(self.rating) > 0:
            self.average_rating = sum(self.rating) / len(self.rating)
        else:
            self.average_rating = 0



    def __str__(self):
        if self.rating == 0:
            return f"{self.name} ({self.seasons} seasons)\ngenres: {self.genres}\nno ratings "
        else:
            return f"{self.name} ({self.seasons} seasons)\ngenres: {self.genres}\nrating: {self.average_rating} "
        
    
def minimum_grade(rating, series_list):
    return [series for series in series_list if series.average_rating >= rating]

    
def includes_genre(genre, series_list):
        return [series for series in series_list if genre in series.genres]




"""
s1 = Series("Dexter", 8, ["Crime", "Drama", "Mystery", "Thriller"])
s1.rate(5)

s2 = Series("South Park", 24, ["Animation", "Comedy"])
s2.rate(3)

s3 = Series("Friends", 10, ["Romance", "Comedy"])
s3.rate(2)

series_list = [s1, s2, s3]

print("Minimum grade of 4.5:")
for series in minimum_grade(4.5, series_list):
    print(series.name)

print("Genre Comedy:")
for series in includes_genre("Comedy", series_list):
    print(series.name)




genre_list = ["Crime", "Drama", "Mystery", "Thriller"]
genre_string = ", ".join(genre_list)

dexter = Series("Dexter", 8, genre_string)
dexter.rate(4)
dexter.rate(5)
dexter.rate(5)
dexter.rate(3)
dexter.rate(0)
print(dexter)
"""