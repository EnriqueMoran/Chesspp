class Board:
    def __init__(self):
        self.boardRows = 0
        self.boardColumns = 0
        self.cells = []
        self.pieces = {}    # pieces on board {playerId : [piecesPerRowList]}

    def __repr__(self):
        return f"Board:\n\
        boardRows: {self.boardRows}\n\
        boardColumns: {self.boardColumns}\n\
        cells: {self.cells}\n\
        pieces: {self.pieces}"

    def __str__(self):
        g = lambda row : ''.join([f'  {elem},' if elem < 10 else f' {elem},' for elem in row])[:-1]
        return ''.join([g(row) + "\n" for row in self.cells[::-1]])

    def initialize(self, playerOnePieces, playerTwoPieces):    # load player pieces on board
        self.cells = [[0 for _ in range(self.boardColumns)] for _ in range(self.boardRows)]
        for index, row in enumerate(playerOnePieces):    # Player 1
            self.cells[index] = row
        for index, row in enumerate(playerTwoPieces):    # Player 2
            self.cells[(self.boardRows - 1) - index] = row

    def loadConfig(self, data):    # read config from raw data
        self.boardRows = int(data['board_rows'])
        self.boardColumns = int(data['board_columns'])

