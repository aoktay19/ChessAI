import chess.pgn
import numpy as np
from state import State

"""def print_moves(game):
      # Get the evaluation of the first move
    white_ser, black_ser = [], []
    white_cp = list()
    black_cp = list()
    board = game.board()
    for move in game.mainline():
        if move.eval() is not None:
            s = chess.Move.from_uci(move.uci())
            board.push(s)
            ser = State(board).serialize()
            
            if(move.eval().turn == chess.WHITE):

                white_cp.append(move.eval().white().score(mate_score=100000))
                white_ser.append(ser)
            else:
                black_cp.append(move.eval().black().score(mate_score=100000))
                black_ser.append(ser)
            #print("HAMELELELLELELLELE", end="\n")
            #print(move.eval().relative.score(), end="\n")
            #print(move, end="\n")
            #print(move.eval().white(), end="\n")
        else:
            break
    if len(white_cp) != 0:
        #print(white_cp)
        #print(black_cp)
        original_array = np.array(white_cp)
        original_array = np.insert(original_array, 0, 0)
        # Calculate the differences between consecutive elements
        differences_array = np.diff(original_array)
        #print(differences_array)
        #print(white_ser[0])
        return white_ser, white_cp"""
def print_moves(game):
      # Get the evaluation of the first move
    white_ser, black_ser = [], []
    white_cp = list()
    black_cp = list()
    board = game.board()
    for i, move in enumerate(game.mainline_moves()):
        board.push(move)
        if i % 2 == 0:
            ser = State(board).serialize()
            white_ser.append(ser)
        
    for move in game.mainline():
        if move.eval() is not None:
            
            if(move.eval().turn == chess.WHITE):
                white_cp.append(move.eval().white().score(mate_score=100000))

            else:
                black_cp.append(move.eval().black().score(mate_score=100000))
            #print("HAMELELELLELELLELE", end="\n")
            #print(move.eval().relative.score(), end="\n")
            #print(move, end="\n")
            #print(move.eval().white(), end="\n")
        else:
            break
    if len(white_cp) != 0:
        #print(white_cp)
        #print(black_cp)
        original_array = np.array(white_cp)
        original_array = np.insert(original_array, 0, 0)
        # Calculate the differences between consecutive elements
        differences_array = np.diff(original_array)
        #print(differences_array)
        #print(white_ser[0])
        return white_ser, white_cp
    

def main():
    pgn_file_path = r"C:\Users\nsavran19\Desktop\ChessAI\a.pgn"  # Replace with the path to your PGN file
    X,Y = [], []
    with open(pgn_file_path) as pgn_file:
        while True and len(X) < 1000:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # No more games in the file

            #print("\nGame:", game.headers["White"], "vs", game.headers["Black"])
            if print_moves(game) is not None:
                a,b = print_moves(game)
                for i in a:
                    X.append(i)
                for j in b:
                    Y.append(j)
    for i, sublist in enumerate(X):
        print(f"Size of element {i}: {len(sublist)}")
    #X_1 = np.array(X)
    #Y_1 = np.array(Y)
    np.savez("deneme.npz", X, Y)

if __name__ == "__main__":
    main()
