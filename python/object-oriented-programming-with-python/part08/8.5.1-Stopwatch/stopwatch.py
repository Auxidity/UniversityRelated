import time

class Stopwatch:
    def __init__(self):
        self.seconds = 0
        self.minutes = 0

    def tick(self):
        self.seconds += 1
        time.sleep(1)

        if self.seconds >= 60:
            self.seconds = 0
            self.minutes += 1
        
        if self.minutes >= 60:
            self.minutes = 0
            self.seconds = 0
    def __str__(self):
        return f"{self.minutes:02d}:{self.seconds:02d}"


""" 
watch = Stopwatch()


for i in range (3600):
    print(watch)
    watch.tick()

"""