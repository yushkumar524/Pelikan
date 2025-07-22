import chess.svg
import os
import webbrowser

class UI:
    def __init__(self, board):
        self.board = board
        self.page_opened = False

    def display(self):
        svg = chess.svg.board(board=self.board, size=400)
        filepath = os.path.abspath("chess_board.svg")
        with open(filepath, "w") as f:
            f.write(svg)
        
        if not self.page_opened:
            webbrowser.open("file://" + filepath, new=0)
            self.page_opened = True

    def get_player_move(self):
        return input("Your move: ")