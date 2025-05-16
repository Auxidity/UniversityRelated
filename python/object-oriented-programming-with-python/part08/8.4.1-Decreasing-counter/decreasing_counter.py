
class DecreasingCounter:
    def __init__(self,initial_value: int):
        if initial_value >= 0:
            self.value  = initial_value
            self.initial_value = initial_value
        
        else:
            raise ValueError("Initial value must be greater than or equal to 0")

    def print_value(self):
        print("Value:", self.value)

    def decrease(self):
        if self.value > 0:
            self.value = self.value - 1
        
        else: ##Prevents the numbers from going to negative. 
            self.value = self.value
    
    def set_to_zero(self):
        self.value = 0
    
    def reset_original_value(self):
        self.value = self.initial_value
            
##Test case trying to showcase every part, first just decreasing the value and printing it, then setting to zero, then showing it doesn't go below zero and finally resetting to original value
counter = DecreasingCounter(100) 
counter.print_value()
counter.decrease()
counter.print_value()
counter.set_to_zero()
counter.print_value()
counter.decrease()
counter.print_value()
counter.reset_original_value()
counter.print_value()