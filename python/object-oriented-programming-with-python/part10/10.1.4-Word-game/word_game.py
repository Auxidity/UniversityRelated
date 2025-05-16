import random

class WordGame():
    def __init__(self, rounds: int):
        self.wins1 = 0
        self.wins2 = 0
        self.rounds = rounds

    def round_winner(self, player1_word: str, player2_word: str):
        # determine a random winner
        return random.randint(1, 2)

    def play(self):
        print("Word game:")
        for i in range(1, self.rounds+1):
            print(f"round {i}")
            answer1 = input("player1: ")
            answer2 = input("player2: ")

            if self.round_winner(answer1, answer2) == 1:
                self.wins1 += 1
                print("player 1 won")
            elif self.round_winner(answer1, answer2) == 2:
                self.wins2 += 1
                print("player 2 won")
            else:
                pass # it's a tie

        print("game over, wins:")
        print(f"player 1: {self.wins1}")
        print(f"player 2: {self.wins2}")

class LongestWord(WordGame):
    def __init__(self, rounds: int):
        super().__init__(rounds)
    def round_winner(self, answer1:str, answer2: str):
        if len(answer1)>len(answer2):
            return 1
        elif len(answer2)>len(answer1):
            return 2
        else:
            return 0

class MostVowels(WordGame):
    def __init__(self, rounds: int):
        super().__init__(rounds)
    
    def count_vowels(self, input_string):
        vowels = "aeiouAEIOU"
        count = 0

        for char in input_string:
            if char in vowels:
                count += 1

        return count

    def round_winner(self, answer1:str, answer2: str):
        if self.count_vowels(answer1)>self.count_vowels(answer2):
            return 1
        elif self.count_vowels(answer2)>self.count_vowels(answer1):
            return 2
        else:
            return 0

class RockPaperScissors(WordGame):
    def __init__(self, rounds: int):
        super().__init__(rounds)
    
    def round_winner(self, answer1:str, answer2:str):
        valid_choices = {'rock', 'paper', 'scissor'}

        if answer1 not in valid_choices and answer2 not in valid_choices:
            return 0 #Tie, neither is valid answer
        elif answer1 not in valid_choices:
            return 2
        elif answer2 not in valid_choices:
            return 1
        else:
            if answer1 == 'rock':
                if answer2 == 'rock':
                    return 0
                elif answer2 == 'paper':
                    return 2
                else:
                    return 1
            elif answer1 == 'paper':
                if answer2 == 'rock':
                    return 1
                elif answer2 == 'paper':
                    return 0
                else:
                    return 2
            else:
                if answer2 == 'rock':
                    return 2
                elif answer2 == 'scissor':
                    return 0
                else:
                    return 1


