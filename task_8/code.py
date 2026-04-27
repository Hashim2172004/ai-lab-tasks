def minimax(depth, is_maximizing):
    # Example terminal condition
    if depth == 0:
        return evaluate()

    if is_maximizing:
        best = -float('inf')

        for move in get_possible_moves():
            make_move(move)
            score = minimax(depth - 1, False)
            undo_move(move)
            best = max(best, score)

        return best

    else:
        best = float('inf')

        for move in get_possible_moves():
            make_move(move)
            score = minimax(depth - 1, True)
            undo_move(move)
            best = min(best, score)

        return best