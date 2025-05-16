class Book:
    def __init__(self, name: str, author: str, genre: str, year: int):
        self.name = name
        self.author = author
        self.genre = genre
        self.year = year

def older_book(book1: Book, book2: Book) -> Book:
    if book1.year < book2.year:
        return f"{book1.name} is older, it was published in {book1.year}"
    elif book1.year > book2.year:
        return f"{book2.name} is older, it was published in {book2.year}"
    else:
        return f"{book1.name} and {book2.name} were published in {book1.year}"


    


python = Book("Fluent Python", "Luciano Ramalho", "programming", 2015)
everest = Book("High Adventure", "Edmund Hillary", "autobiography", 1956)
norma = Book("Norma", "Sofi Oksanen", "crime", 2015)

print(older_book(python, everest))
print(older_book(python, norma))
