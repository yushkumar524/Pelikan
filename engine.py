import chess
import chess.polyglot

pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]

class Engine:
    def __init__(self, board):
        self.board = board
        self.move_history = []
        self.transposition_table = {}

    def evaluate(self):
        board = self.board
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100*(wp - bp) + 320*(wn - bn) + 330*(wb - bb) + \
                   500*(wr - br) + 900*(wq - bq)

        pawnsq = 0
        for square in board.pieces(chess.PAWN, chess.WHITE):
            pawnsq += pawntable[square]
        for square in board.pieces(chess.PAWN, chess.BLACK):
            pawnsq -= pawntable[chess.square_mirror(square)]
        
        knightsq = 0
        for square in board.pieces(chess.KNIGHT, chess.WHITE):
            knightsq += knightstable[square]
        for square in board.pieces(chess.KNIGHT, chess.BLACK):
            knightsq -= knightstable[chess.square_mirror(square)]
        
        bishopsq = 0
        for square in board.pieces(chess.BISHOP, chess.WHITE):
            bishopsq += bishopstable[square]
        for square in board.pieces(chess.BISHOP, chess.BLACK):
            bishopsq -= bishopstable[chess.square_mirror(square)]
        
        rooksq = 0
        for square in board.pieces(chess.ROOK, chess.WHITE):
            rooksq += rookstable[square]
        for square in board.pieces(chess.ROOK, chess.BLACK):
            rooksq -= rookstable[chess.square_mirror(square)]
        
        queensq = 0
        for square in board.pieces(chess.QUEEN, chess.WHITE):
            queensq += queenstable[square]
        for square in board.pieces(chess.QUEEN, chess.BLACK):
            queensq -= queenstable[chess.square_mirror(square)]
        
        kingsq = 0
        for square in board.pieces(chess.KING, chess.WHITE):
            kingsq += kingstable[square]
        for square in board.pieces(chess.KING, chess.BLACK):
            kingsq -= kingstable[chess.square_mirror(square)]

        eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        return eval if board.turn else -eval

    def quiesce(self, alpha, beta):
        static_eval = self.evaluate()
        if static_eval >= beta:
            return beta
        alpha = max(alpha, static_eval)

        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -self.quiesce(-beta, -alpha)
                self.board.pop()
                if score >= beta:
                    return beta
                alpha = max(alpha, score)
        return alpha

    def order_moves(self, moves):
        captures = []
        others = []
        
        for move in moves:
            if self.board.is_capture(move):
                captures.append(move)
            else:
                others.append(move)
    
        return captures + others

    def alphabeta(self, alpha, beta, depth):
        key = chess.polyglot.zobrist_hash(self.board)
        if key in self.transposition_table:
            cached_score, cached_depth = self.transposition_table[key]
            if cached_depth >= depth: return cached_score
        
        bestscore = -9999
        if depth == 0:
            score = self.quiesce(alpha, beta)
            self.transposition_table[key] = (score, depth)
            return score

        ordered_moves = self.order_moves(self.board.legal_moves)

        for move in ordered_moves:
            self.board.push(move)
            score = -self.alphabeta(-beta, -alpha, depth - 1)
            self.board.pop()

            if score >= beta:
                self.transposition_table[key] = beta, depth
                return beta
            bestscore = max(bestscore, score)
            alpha = max(alpha, score)
        
        self.transposition_table[key] = (bestscore, depth)
        return bestscore

    def select_move(self, depth=3):
        try:
            with chess.polyglot.MemoryMappedReader("baron30.bin") as reader:
                move = reader.weighted_choice(self.board).move
                self.move_history.append(move)
                return move
        except:
            best_move = None
            best_value = -9999
            alpha = -10000
            beta = 10000
            for move in self.board.legal_moves:
                self.board.push(move)
                value = -self.alphabeta(-beta, -alpha, depth - 1)
                self.board.pop()
                if value > best_value:
                    best_value = value
                    best_move = move
                if value > alpha:
                    alpha = value
            if best_move:
                self.move_history.append(best_move)
            return best_move