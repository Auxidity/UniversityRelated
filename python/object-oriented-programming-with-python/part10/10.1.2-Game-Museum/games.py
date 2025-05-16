class ComputerGame:
    def __init__(self, name: str, publisher: str, year: int):
        self.name = name
        self.publisher = publisher
        self.year = year

class GameWarehouse:
    def __init__(self):
        self.games = []

    def add_game(self, game: ComputerGame):
        self.games.append(game)

    def list_games(self):
        return self.games

class GameMuseum(GameWarehouse):
    def __init__(self):
        super().__init__()
    
    def list_games(self):
        filtered_games = []
        for game in self.games:
            if game.year <= 1990:
                filtered_games.append(game)
        return filtered_games
            
