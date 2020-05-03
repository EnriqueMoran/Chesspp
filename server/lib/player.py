import logging
from math import ceil

class Player:

    def __init__(self, ip, nick, playerId):
        self.ip = ip
        self.nick = nick
        self.pieces = []    # player pieces per board row
        self.nPieces = 0
        self.id = playerId
        self.wins = 0
        self.defeats = 0
        logging.info(f"Player created: {self.nick} - {self.id}, ip: {self.ip}.")

    def __repr__(self):
        return f"Player ({self.id}) - Nick: {self.nick}, Ip: {self.ip}, \
        Wins: {self.wins} Defeats: {self.defeats}, nPieces: {self.nPieces}, \\nPieces: {self.pieces}"

    def __str__(self):
        return(f"Player ({self.id}) - Name: {self.nick}, Wins: {self.wins} Defeats: {self.defeats}")

    def loadConfig(self, playerData, boardData):
        self.nPieces = int(playerData["player_pieces"])
        boardColumns = int(boardData["board_columns"])
        playerRows = ceil(self.nPieces / boardColumns)
        self.pieces = [[0 for i in range(boardColumns)] for _ in range(playerRows)]

    def addPiece(self, piece, row, column):
        self.pieces[row][column] = piece

    def movePiece(self, oldRow, oldColumn, newRow, newColumn):
        if True:    # check if movement is possible (in piece's movement list and rules set)
            return (oldRow, oldColumn, newRow, newColumn)
        else:
            return None