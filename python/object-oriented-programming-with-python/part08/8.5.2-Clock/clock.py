import time

class Clock:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours

    def tick(self):
        ##print(f"{self.minutes:02d}:{self.seconds:02d}") useless line, def __str__ is doing this line in terminal.
        self.seconds += 1
        time.sleep(1)

        if self.seconds >= 60:
            self.seconds = 0
            self.minutes += 1
        
        if self.minutes >= 60:
            self.minutes = 0
            self.seconds = 0
            self.hours += 1

        if self.hours >= 24:
            self.seconds = 0
            self.minutes = 0
            self.hours = 0

    def set(self, hours=None, minutes=None, seconds=None):
        if hours is not None:
            self.hours = hours
        else:
            self.hours = 0
        if minutes is not None:
            self.minutes = minutes
        else:
            self.minutes = 0
        if seconds is not None:
            self.seconds = seconds
        else:
            self.seconds = 0

    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"



"""
clock = Clock(23, 59, 55)
print(clock)
clock.tick()
print(clock)
clock.tick()
print(clock)
clock.tick()
print(clock)
clock.set(7)
print(clock)
clock.tick()
print(clock)
clock.tick()
print(clock)

clock.set(12, 5)
print(clock)
clock.tick()
print(clock)
""" 

