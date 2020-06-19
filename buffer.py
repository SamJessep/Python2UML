class ChessPiece:
    def __init__(self, type):
        self.type = type


from abc import ABC

from demoCode.projects.basicOOP.chessPiece import ChessPiece


class Game(ABC):
    def __init__(self):
        pass

    def Start(self):
        pass

    def Finish(self):
        pass


class Chess_game(Game):
    def __init__(self):
        self.pieces = []

    def Start(self):
        pieces = self.get_pieces()
        self.pieces = pieces
        for piece in pieces:
            print(piece.type)

    def get_pieces(self):
        pieces = []
        typeCount = {"king": 2, "queen": 2, "bishop": 4,
                     "knight": 4, "rook": 4, "pawn": 16}
        for type in typeCount:
            for count in range(typeCount[type]):
                pieces.append(ChessPiece(type))
        return pieces


Chess_game().Start()
