# app.py (Flask backend)
from flask import Flask, render_template, jsonify, request
import chess
from chess import Board, Piece

app = Flask(__name__)
app.static_folder = 'static'

current_board = Board()

print(current_board.piece_map())
initial_piece_map = current_board.piece_map()


@app.route('/')
def index():
    return render_template('mainMenu.html')

@app.route('/playOffline')
def play_offline():
    return render_template('playOffline.html', piece_map=initial_piece_map)

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    move = data['move']
    if move == "newGame":
        current_board.reset()
        return jsonify({'success': True, 'new_piece_map': current_board.piece_map(), 'is_checkmate': current_board.is_checkmate()})
    elif move == "undoMove":
        current_board.pop()
        return jsonify({'success': True, 'new_piece_map': current_board.piece_map(), 'is_checkmate': current_board.is_checkmate()})
    makeMove = chess.Move.from_uci(move)
    san_move = current_board.san(makeMove)
    if current_board.is_legal(makeMove):
        current_board.push(makeMove)
        new_piece_map = current_board.piece_map();
        return jsonify({'success': True, 'new_piece_map': new_piece_map, 'is_checkmate': current_board.is_checkmate(), 'move': san_move})
    else:
        return jsonify({'success': False, 'message': 'Invalid move'})

@app.route('/get_possible_moves', methods=['POST'])
def get_possible_moves():
    data = request.json
    square = data['square']
    file_char, rank_char = square[0], square[1]

    file_index = ord(file_char) - ord('a')
    rank_index = int(rank_char) - 1

    square_index = file_index + rank_index * 8
    piece = current_board.piece_at(square_index)
    
    if piece:
        legal_moves = [move.uci() for move in current_board.legal_moves if move.from_square == square_index]
        return jsonify({'piece': piece.symbol(), 'moves': legal_moves})
    else:
        return jsonify({'piece': None, 'moves': []})

if __name__ == '__main__':
    app.run(debug=True)
