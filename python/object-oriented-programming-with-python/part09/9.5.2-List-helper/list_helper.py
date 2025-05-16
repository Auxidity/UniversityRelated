class ListHelper:
    def __init__(self):
        pass

    @staticmethod
    def greatest_frequency(my_list:list):
        freq_dict = {}

        for num in my_list:
            if num in freq_dict:
                freq_dict[num] += 1
            else:
                freq_dict[num] = 1
        
        most_frequent_element = max(freq_dict, key=freq_dict.get)
        return most_frequent_element

    @staticmethod
    def doubles(my_list:list):
        doubles_dict = {}
        

        for num in my_list:
            if num  in doubles_dict:
                doubles_dict[num] += 1
                
            else:
                doubles_dict[num] = 1

        unique_doubles_count = sum(1 for value in doubles_dict.values() if value >= 2)

        return unique_doubles_count



