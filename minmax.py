
from __future__ import annotations
from board import Piece, Board, Move


def minimax(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8) -> float:
    # Abbruchbedingung – Endposition oder maximale Tiefe erreicht
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # Rekursionsbedingung – eigene Gewinne maximieren oder die des Gegners minimieren
    if maximizing:
        best_eval: float = float("-inf") # Beliebig niedriger Startwert
        for move in board.legal_moves:
            result: float = minimax(board.move(move), False, original_player, max_depth - 1)
            best_eval = max(result, best_eval) # Wir wollen den Zug mit der höchsten Bewertung
        return best_eval
    else: # Minimieren
        worst_eval: float = float("inf")
        for move in board.legal_moves:
            result = minimax( board.move(move), True, original_player, max_depth - 1)
            worst_eval = min(result, worst_eval) # Wir wollen den Zug mit der niedrigsten Bewertung
        return worst_eval


def alphabeta(board: Board, maximizing: bool, original_player: Piece, max_depth: int = 8, alpha: float = float("-inf"), beta: float = float("inf")) -> float:
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)

    # Rekursionsbedingung – eigene Gewinne maximieren oder die des Gegners minimieren
    if maximizing:
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move), False, original_player, max_depth - 1, alpha, beta)
            alpha = max(result, alpha)
            if beta <= alpha:
                break
        return alpha
    else:  # Minimieren
        for move in board.legal_moves:
            result = alphabeta(board.move(move), True, original_player, max_depth - 1, alpha, beta)
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta


# Den besten möglichen Zug an der aktuellen Position finden
# und bis zu max_depth vorausschauen
def find_best_move(board: Board, max_depth: int = 2) -> Move:
    best_eval: float = float("-inf")
    best_move: Move = Move(-1)
    for move in board.legal_moves:
        result: float = alphabeta(board.move(move), False, board.turn, max_depth)
        print ("result: {0}, best_eval: {1}]".format(result, best_eval))
        if result > best_eval:
            best_eval = result
            best_move = move
    return best_move
