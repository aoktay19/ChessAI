# app.py (Flask backend)
from flask import Flask, render_template, jsonify, request
import chess
import chess.engine
from chess import Board, Piece
from stockfish import Stockfish

engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\ENG128\Desktop\ChessAI\stockfish\stockfish-windows-x86-64-avx2.exe")
app = Flask(__name__, template_folder='pages')
app.static_folder = 'static'

current_board = chess.Board()



initial_piece_map = current_board.piece_map()


@app.route('/')
def index():
    return render_template('mainMenu.html')

@app.route('/playOffline')
def play_offline():
    piece_map = current_board.piece_map()
    return render_template('playOffline.html', piece_map=piece_map)

@app.route('/playWithAI')
def play_withAI():
    color = request.args.get('color', default=None)
    print("renk: ", color == "black")
    """if color == "black":
        move = getAIMove()
        print(move)
        makeMove = chess.Move.from_uci(move)
        current_board.push(makeMove)"""
    piece_map = current_board.piece_map()
    return render_template('playWithAI.html', piece_map=piece_map, color=color)


@app.route('/make_move', methods=['POST'])
def make_move():
    #TODO: check is it checkmate in AIMove
    data = request.json
    move = data['move']
    if move == "newGame":
        current_board.reset()
        return jsonify({'success': True, 'new_piece_map': current_board.piece_map(), 'is_checkmate': current_board.is_checkmate()})
    elif move == "undoMove":
        current_board.pop()
        return jsonify({'success': True, 'new_piece_map': current_board.piece_map(), 'is_checkmate': current_board.is_checkmate()})
    elif move == "AIMove":
        move = getAIMove()
        san_move = current_board.san(move)
        current_board.push(move)
        new_piece_map = current_board.piece_map()
        return jsonify({'success': True, 'new_piece_map': new_piece_map, 'is_checkmate': current_board.is_checkmate(), 'move': san_move})

    makeMove = chess.Move.from_uci(move)
    san_move = current_board.san(makeMove)
    if current_board.is_legal(makeMove):
        current_board.push(makeMove)
        new_piece_map = current_board.piece_map()
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

def getAIMove():
    result = engine.play(current_board, chess.engine.Limit(time=0.1))
    return result.move
    """move_list = [move.uci() for move in current_board.legal_moves]
    return move_list[0]"""


if __name__ == '__main__':
    app.run(debug=True)
