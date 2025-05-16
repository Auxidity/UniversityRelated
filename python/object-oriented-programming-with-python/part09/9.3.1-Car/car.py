class Car:
    def __init__(self,tank=None,odometer_reading=None):
        if tank is not None:
            self.__tank = tank
        else:
            self.__tank = 0
        
        if odometer_reading is not None:
            self.__odometer_reading = odometer_reading 
        else:
            self.__odometer_reading = 0
    
    def fill_up(self):

        if self.__tank + 60 > 60:
            self.__tank = 60
        else:
            self.__tank += 60

    def drive(self,km:int):
        if km < 0:
            return "Can't drive negative kilometers"
        else:
            if self.__tank - km < 0:
                self.__odometer_reading += min(self.__tank, km)
                self.__tank = 0
                
            else:    
                self.__odometer_reading += km
                self.__tank -= km

    def __str__(self):
        return f"Car: odometer reading {self.__odometer_reading} km, petrol remaining {self.__tank} litres"
    

