import chess.pgn

def print_moves(game):
    print("\nMoves:")
      # Get the evaluation of the first move
    a = list()
    for move in game.mainline():
        if move.eval() is not None:
            a.append(move.eval().white())
            print("HAMELELELLELELLELE", end="\n")
            print(move.eval().white(), end="\n")
            print(move.eval().black(), end="\n")
            print(move.eval(), end="\n")
        else:
            break
    print(a)
    print("\nResult:", game.headers["Result"])
    print("\n")

def main():
    pgn_file_path = r"C:\Users\ENG128\Desktop\ChessAI\a.pgn"  # Replace with the path to your PGN file

    with open(pgn_file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # No more games in the file

            print("\nGame:", game.headers["White"], "vs", game.headers["Black"])
            print_moves(game)

if __name__ == "__main__":
    main()
