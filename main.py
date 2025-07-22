import chess
from board import ChessBoard
from engine import Engine
from ui import UI

class ChessGame:
    def __init__(self):
        self.chessboard = ChessBoard()
        self.engine = Engine(self.chessboard.board)
        self.ui = UI(self.chessboard.board)
        self.player_is_white = self.ask_player_color()

    def ask_player_color(self):
        while True:
            print("Hi! I'm Pelikan, a chess engine created by Ayush Kumar.")
            choice = input("Do you want to play as white or black? (w/b): ").strip().lower()
            if (choice == "w"): return True
            elif (choice == "b"): return False
            else: print("Invalid input. Please enter 'w' or 'b'.")

    def play(self):
        while not self.chessboard.is_game_over():
            self.ui.display()
            if (self.chessboard.board.turn == chess.WHITE and self.player_is_white or
                self.chessboard.board.turn == chess.BLACK and not self.player_is_white):
                move_str = self.ui.get_player_move()
                while (not self.chessboard.apply_move(move_str)):
                    print("Invalid input. Please enter a move in algebraic notation.")
                    move_str = self.ui.get_player_move()
            else:
                print("Pelikan is thinking...")
                move = self.engine.select_move(depth=3)
                print(f"Pelikan plays: {self.chessboard.board.san(move)}")
                self.chessboard.board.push(move)

        self.ui.display()
        print("Game Over. Result:", self.chessboard.result())


if __name__ == "__main__":
    game = ChessGame()
    game.play()