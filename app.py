from flask import Flask, render_template, request, jsonify
import chess
import chess.svg
import os
from board import ChessBoard
from engine import Engine

app = Flask(__name__)

class ChessGame:
    def __init__(self, player_color='white'):
        self.chessboard = ChessBoard()
        self.engine = Engine(self.chessboard.board)
        self.player_is_white = (player_color.lower() == 'white')
        self.game_active = True
        self.last_engine_move = None

    def ask_player_color(self):
        return self.player_is_white

    def get_game_ending_reason(self):
        board = self.chessboard.board
        
        if board.is_checkmate():
            return "by checkmate."
        elif board.is_stalemate():
            return "by stalemate."
        elif board.is_insufficient_material():
            return "by insufficient material."
        elif board.is_seventyfive_moves():
            return "by 75-move rule."
        elif board.is_fivefold_repetition():
            return "by fivefold repetition."
        elif board.can_claim_draw():
            if board.can_claim_fifty_moves():
                return "by 50-move rule."
            elif board.can_claim_threefold_repetition():
                return "by threefold repetition."
        else:
            return "."

    def play(self, move_str=None):
        if self.chessboard.is_game_over():
            return {
                'game_over': True,
                'result': self.chessboard.result(),
                'reason': self.get_game_ending_reason()
            }
        
        if move_str and self._is_player_turn():
            if not self.chessboard.apply_move(move_str):
                return {'error': 'Invalid move'}
            
            if self.chessboard.is_game_over():
                return {
                    'game_over': True,
                    'result': self.chessboard.result(),
                    'reason': self.get_game_ending_reason()
                }
        
        if not self._is_player_turn() and not self.chessboard.is_game_over():
            move = self.engine.select_move(depth=3)
            if move:
                self.last_engine_move = self.chessboard.board.san(move)
                self.chessboard.board.push(move)
        
        return {
            'game_over': self.chessboard.is_game_over(),
            'result': self.chessboard.result() if self.chessboard.is_game_over() else None,
            'reason': self.get_game_ending_reason() if self.chessboard.is_game_over() else None,
            'engine_move': self.last_engine_move
        }

    def start_new_game(self, player_color):
        self.__init__(player_color)
        
        if not self.player_is_white:
            result = self.play()
            return True, result
        
        return True, {'game_over': False}

    def make_player_move(self, move_str):
        if not self.game_active:
            return False, "Game is not active"
        
        if not self._is_player_turn():
            return False, "Not your turn"
        
        result = self.play(move_str)
        
        if 'error' in result:
            return False, result['error']
        
        return True, result

    def _is_player_turn(self):
        return (self.chessboard.board.turn == chess.WHITE and self.player_is_white) or \
               (self.chessboard.board.turn == chess.BLACK and not self.player_is_white)

    def get_board_svg(self):
        return chess.svg.board(board=self.chessboard.board, size=400)

    def get_current_turn(self):
        return "White" if self.chessboard.board.turn == chess.WHITE else "Black"

game = ChessGame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    try:
        data = request.get_json()
        player_color = data.get('color', 'white')
        
        global game
        game = ChessGame(player_color)
        success, result = game.start_new_game(player_color)
        
        if success:
            response_data = {
                'success': True,
                'board_svg': game.get_board_svg(),
                'turn': game.get_current_turn(),
                'is_player_turn': game._is_player_turn()
            }
            
            if result.get('engine_move'):
                response_data['engine_move'] = result['engine_move']
            
            return jsonify(response_data)
        else:
            return jsonify({'success': False, 'error': 'Failed to start game'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/make_move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        move = data.get('move', '').strip()
        
        if not move:
            return jsonify({'success': False, 'error': 'No move provided'})
        
        success, result = game.make_player_move(move)
        
        if success:
            response_data = {
                'success': True,
                'board_svg': game.get_board_svg(),
                'turn': game.get_current_turn(),
                'is_player_turn': game._is_player_turn(),
                'game_over': result.get('game_over', False)
            }
            
            if result.get('engine_move'):
                response_data['engine_move'] = result['engine_move']
                game.last_engine_move = None
            
            if result.get('game_over'):
                response_data['result'] = f"Game over. Result: {result['result']} {result['reason']}"
                
            return jsonify(response_data)
        else:
            return jsonify({'success': False, 'error': result})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/game_state')
def game_state():
    try:
        if not game.game_active:
            return jsonify({'error': 'No active game'})
        
        return jsonify({
            'board_svg': game.get_board_svg(),
            'turn': game.get_current_turn(),
            'is_player_turn': game._is_player_turn(),
            'game_over': game.chessboard.is_game_over(),
            'result': f"Game over. Result: {game.chessboard.result()} {game.get_game_ending_reason()}" if game.chessboard.is_game_over() else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
else:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)