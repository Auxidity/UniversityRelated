class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __str__(self):
        return f"rectangle {self.length}x{self.width}"

    def area(self):
        return self.length * self.width

class Square(Rectangle):
    def __init__(self, length: int):
        super().__init__(length, length)

