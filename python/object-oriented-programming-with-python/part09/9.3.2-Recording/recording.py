class Recording:
    def __init__(self, length):
        if length >= 0:
            self.__length = length
        else:
            raise ValueError("Amount must be above zero") 

    @property
    def length(self):
        return self.__length
    
    @length.setter
    def length(self,length):
        if length >= 0:
            self.__length = length
        else:
            raise ValueError("Amount must be above zero")
        

