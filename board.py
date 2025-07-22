import chess

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()

    def apply_move(self, move_str):
        try:
            move = self.board.parse_san(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            return False
        except:
            return False

    def is_game_over(self):
        return self.board.is_game_over()

    def result(self):
        return self.board.result()

    def get_legal_moves(self):
        return list(self.board.legal_moves)