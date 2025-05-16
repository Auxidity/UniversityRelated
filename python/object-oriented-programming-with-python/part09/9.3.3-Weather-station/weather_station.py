class WeatherStation:
    def __init__(self,name:str):
        self.name = name #Based on how I understood the task, this was supposed to be left as public.
        self.__observations = []
        self.__count_of_obs = 0
    
    def add_observation(self,observation:str):
        self.__observations.append(observation)
        self.__count_of_obs += 1
    
    def latest_observation(self):
        if not self.__observations:
            return None
        else:
            return self.__observations[-1]
        
    def number_of_observations(self):
        return self.__count_of_obs
    
    def __str__(self):
        return f"{self.name}, {self.__count_of_obs} observations"
    

