def get_line_score(connected_pieces, m):
    return m ** (connected_pieces - 1)


def max_score_if_not_ending(n, m):
    return m ** (n - 1) - 1


# if circle wins, this function return a possitive number of circle's max score; if X wins, this function return a negative number of X's min score; otherwise,
# this function returns (circle score,cross score) with circle score in positive and cross score in negative; the positive/negative may be changed according to pieces this AI gets, in main module
def calculate_board_value(board_str, m, myself):
    board = board_str.strip().split()
    size = len(board)
    circle_in_line = set()
    all_circle = set()
    cross_in_line = set()
    all_cross = set()
    circle_score = 0
    cross_score = 0

    for each_row in range(size):  # scan rows line by line,from top to left
        previous_piece = "-"
        continue_piece = 1
        score = 0
        for each_column in range(size):
            if (board[each_row][each_column] == 'O'):  # all_circle stores all circles' positions
                all_circle.add((each_row, each_column))
            if (board[each_row][each_column] == 'X'):  # all_cross stores all crosses' positions
                all_cross.add((each_row, each_column))
            if (board[each_row][
                each_column] == previous_piece and previous_piece != "-"):  # if current piece is same to left piece
                continue_piece = continue_piece + 1
                if (continue_piece == m):  # game over
                    if (board[each_row][each_column] == myself):
                        return get_line_score(continue_piece, m)
                    else:
                        return -get_line_score(continue_piece, m)
                if (each_column == size - 1):  # if current piece is at the most right position of the board
                    if (
                            each_column - continue_piece == 0):  # if left piece of this line is at the most left position of the board
                        score = continue_piece
                    elif (board[each_row][each_column - continue_piece] != previous_piece and board[each_row][
                        each_column - continue_piece] != "-"):  # if the left side of this line is blocked by opponent
                        score = continue_piece
                    else:
                        score = get_line_score(continue_piece, m) / 2

                    if (previous_piece == 'O'):
                        circle_score = circle_score + score
                        col = each_column
                        for i in range(
                                continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                            circle_in_line.add((each_row, col))
                            col = col - 1

                    else:
                        cross_score = cross_score - score
                        col = each_column
                        for i in range(continue_piece):
                            cross_in_line.add((each_row, col))
                            col = col - 1

            else:  # if the current piece different from left piece
                if (continue_piece != 1 and previous_piece != "-"):
                    score = get_line_score(continue_piece, m)
                    if (board[each_row][
                        each_column] != "-" and each_column - continue_piece - 1 < 0):  # if the left piece of this line is at the most left position of the board, and the right side is also blocked
                        score = continue_piece
                    elif (board[each_row][
                              each_column] == "-" and each_column - continue_piece - 1 < 0):  # if the left piece of this line is at the most left position of the board, and the right side is not blocked
                        score = score / 2
                    elif (board[each_row][each_column] != "-" and board[each_row][
                        each_column - continue_piece - 1] != "-"):  # if both sides of the line are blocked
                        score = continue_piece
                    elif (board[each_row][each_column] != board[each_row][
                        each_column - continue_piece - 1]):  # if just one side of the line are blocked
                        score = score / 2
                    if (previous_piece == 'O'):
                        circle_score = circle_score + score
                        col = each_column - 1
                        for i in range(
                                continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                            circle_in_line.add((each_row, col))
                            col = col - 1

                    else:
                        cross_score = cross_score - score
                        col = each_column - 1
                        for i in range(continue_piece):
                            cross_in_line.add((each_row, col))
                            col = col - 1
                    continue_piece = 1
                    score = 0
            previous_piece = board[each_row][each_column]

    for each_column in range(size):  # scan columns line by line,from left to right
        previous_piece = "-"
        continue_piece = 1
        score = 0
        for each_row in range(size):
            if (board[each_row][each_column] == 'O'):  # all_circle stores all circles' positions
                all_circle.add((each_row, each_column))
            if (board[each_row][each_column] == 'X'):  # all_cross stores all crosses' positions
                all_cross.add((each_row, each_column))
            if (board[each_row][
                each_column] == previous_piece and previous_piece != "-"):  # if current piece is same to upper piece
                continue_piece = continue_piece + 1
                if (continue_piece == m):  # the game is over
                    if (board[each_row][each_column] == myself):
                        return get_line_score(continue_piece, m)
                    else:
                        return -get_line_score(continue_piece, m)
                if (each_row == size - 1):  # if current piece is at the bottom position of the board
                    if (each_row - continue_piece < 0):  # if top piece of this line is at the top position of the board
                        score = continue_piece
                    elif (board[each_row - continue_piece][each_column] != previous_piece and
                          board[each_row - continue_piece][
                              each_column] != "-"):  # if the top side of this line is blocked by opponent
                        score = continue_piece
                    else:
                        score = get_line_score(continue_piece, m) / 2

                    if (previous_piece == 'O'):
                        circle_score = circle_score + score
                        row = each_row
                        for i in range(
                                continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                            circle_in_line.add((row, each_column))
                            row = row - 1

                    else:
                        cross_score = cross_score - score
                        row = each_row
                        for i in range(continue_piece):
                            cross_in_line.add((row, each_column))
                            row = row - 1

            else:
                if (continue_piece != 1 and previous_piece != "-"):  # if the current piece different from top piece
                    score = get_line_score(continue_piece, m)
                    if (board[each_row][
                        each_column] != "-" and each_row - continue_piece - 1 < 0):  # if the top piece of this line is at the top position of the board, and the bottom side is also blocked
                        score = continue_piece
                    elif (board[each_row][
                              each_column] == "-" and each_row - continue_piece - 1 < 0):  # if the left piece of this line is al the most left position of the board, and the bottom side is not blocked
                        score = score / 2
                    elif (board[each_row][each_column] != "-" and board[each_row - continue_piece - 1][
                        each_column] != "-"):  # if both sides of the line are blocked
                        score = continue_piece
                    elif (board[each_row][each_column] != board[each_row - continue_piece - 1][
                        each_column]):  # if just one side of the line are blocked
                        score = score / 2
                    if (previous_piece == 'O'):
                        circle_score = circle_score + score
                        row = each_row - 1
                        for i in range(
                                continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                            circle_in_line.add((row, each_column))
                            row = row - 1

                    else:
                        cross_score = cross_score - score
                        row = each_row - 1
                        for i in range(continue_piece):
                            cross_in_line.add((row, each_column))
                            row = row - 1
                    continue_piece = 1
                    score = 0
            previous_piece = board[each_row][each_column]

    for each_scan_start in range(2 * size - 1):  # scan all diagonal lines from bottom to top, from left to right
        if (each_scan_start < size):  # this is the left_top part
            each_row = each_scan_start
            each_column = 0
            previous_piece = "-"
            continue_piece = 1
            score = 0
            while (each_row >= 0):
                if (board[each_row][each_column] == 'O'):  # all_circle stores all circles' positions
                    all_circle.add((each_row, each_column))
                if (board[each_row][each_column] == 'X'):  # all_cross stores all crosses' positions
                    all_cross.add((each_row, each_column))
                if (board[each_row][
                    each_column] == previous_piece and previous_piece != "-"):  # if current piece is same to previous piece
                    continue_piece = continue_piece + 1
                    if (continue_piece == m):  # the game is over
                        if (board[each_row][each_column] == myself):
                            return get_line_score(continue_piece, m)
                        else:
                            return -get_line_score(continue_piece, m)
                    if (each_row == 0):  # if current piece is at the top edge of the board
                        if (
                                each_row + continue_piece - 1 == each_scan_start):  # if left piece of this line is at the left position of the board
                            score = continue_piece
                        elif (board[each_row + continue_piece][each_column - continue_piece] != previous_piece and
                              board[each_row + continue_piece][
                                  each_column - continue_piece] != "-"):  # if the left side of this line is blocked by opponent
                            score = continue_piece
                        else:
                            score = get_line_score(continue_piece, m) / 2

                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row
                            col = each_column
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row + 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row
                            col = each_column
                            for i in range(continue_piece):
                                circle_in_line.add((row, col))
                                row = row + 1
                                col = col - 1

                else:
                    if (continue_piece != 1 and previous_piece != "-"):  # if the current piece different from top piece
                        score = get_line_score(continue_piece, m)
                        if (board[each_row][
                            each_column] != "-" and each_row + continue_piece == each_scan_start):  # if the left piece of this line is at the boundary of the board, and the right side is also blocked
                            score = continue_piece
                        elif (board[each_row][
                                  each_column] == "-" and each_row + continue_piece == each_scan_start):  # if the left piece of this line is al the most left position of the board, and the right side is not blocked
                            score = score / 2
                        elif (board[each_row][each_column] != "-" and board[each_row + continue_piece + 1][
                            each_column - continue_piece - 1] != "-"):  # if both sides of the line are blocked
                            score = continue_piece
                        elif (board[each_row][each_column] != board[each_row + continue_piece + 1][
                            each_column - continue_piece - 1]):  # if just one side of the line are blocked
                            score = score / 2
                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row + 1
                            col = each_column - 1
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row + 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row + 1
                            col = each_column - 1
                            for i in range(continue_piece):
                                cross_in_line.add((row, col))
                                row = row + 1
                                col = col - 1
                        continue_piece = 1
                        score = 0
                previous_piece = board[each_row][each_column]
                each_row = each_row - 1
                each_column = each_column + 1
        else:  # this is the right_bottom part

            start_row = size - 1
            start_column = each_scan_start - size + 1
            each_row = start_row
            each_column = start_column
            previous_piece = "-"
            continue_piece = 1
            score = 0
            while (each_column <= size - 1):
                if (board[each_row][each_column] == 'O'):  # all_circle stores all circles' positions
                    all_circle.add((each_row, each_column))
                if (board[each_row][each_column] == 'X'):  # all_cross stores all crosses' positions
                    all_cross.add((each_row, each_column))
                if (board[each_row][
                    each_column] == previous_piece and previous_piece != "-"):  # if current piece is same to previous piece
                    continue_piece = continue_piece + 1
                    if (continue_piece == m):  # the game is over
                        if (board[each_row][each_column] == myself):
                            return get_line_score(continue_piece, m)
                        else:
                            return -get_line_score(continue_piece, m)
                    if (each_column == size - 1):  # if current piece is at the right boundary of the board
                        if (
                                each_row + continue_piece - 1 == size - 1):  # if left piece of this line is at the left position of the board
                            score = continue_piece
                        elif (board[each_row + continue_piece][each_column - continue_piece] != previous_piece and
                              board[each_row + continue_piece][
                                  each_column - continue_piece] != "-"):  # if the left side of this line is blocked by opponent
                            score = continue_piece
                        else:
                            score = get_line_score(continue_piece, m) / 2

                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row
                            col = each_column
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row + 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row
                            col = each_column
                            for i in range(continue_piece):
                                circle_in_line.add((row, col))
                                row = row + 1
                                col = col - 1

                else:
                    if (
                            continue_piece != 1 and previous_piece != "-"):  # if the current piece is different from previous piece
                        score = get_line_score(continue_piece, m)
                        if (board[each_row][
                            each_column] != "-" and each_row + continue_piece == start_row):  # if the left piece of this line is at the boundary of the board, and the right side is also blocked
                            score = continue_piece
                        elif (board[each_row][
                                  each_column] == "-" and each_row + continue_piece == start_row):  # if the left piece of this line is at the most left position of the board, and the right side is not blocked
                            score = score / 2
                        elif (board[each_row][each_column] != "-" and board[each_row + continue_piece + 1][
                            each_column - continue_piece - 1] != "-"):  # if both sides of the line are blocked
                            score = continue_piece
                        elif (board[each_row][each_column] != board[each_row + continue_piece + 1][
                            each_column - continue_piece - 1]):  # if just one side of the line are blocked
                            score = score / 2
                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row + 1
                            col = each_column - 1
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row + 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row + 1
                            col = each_column - 1
                            for i in range(continue_piece):
                                cross_in_line.add((row, col))
                                row = row + 1
                                col = col - 1
                        continue_piece = 1
                        score = 0
                previous_piece = board[each_row][each_column]
                each_row = each_row - 1
                each_column = each_column + 1

    for each_scan_start in range(2 * size - 2, -1,
                                 -1):  # scan all diagonal lines from top to bottom, from left to right
        if (each_scan_start <= size - 1):  # this is the left_bottom part
            each_row = each_scan_start
            each_column = 0
            previous_piece = "-"
            continue_piece = 1
            score = 0
            while (each_row <= size - 1):
                if (board[each_row][each_column] == 'O'):  # all_circle stores all circles' positions
                    all_circle.add((each_row, each_column))
                if (board[each_row][each_column] == 'X'):  # all_cross stores all crosses' positions
                    all_cross.add((each_row, each_column))
                if (board[each_row][
                    each_column] == previous_piece and previous_piece != "-"):  # if current piece is same to previous piece
                    continue_piece = continue_piece + 1
                    if (continue_piece == m):  # the game is over
                        if (board[each_row][each_column] == myself):
                            return get_line_score(continue_piece, m)
                        else:
                            return -get_line_score(continue_piece, m)
                    if (each_row == 0):  # if current piece is at the bottom of the board
                        if (
                                each_row - continue_piece + 1 == each_scan_start):  # if left piece of this line is at the left position of the board
                            score = continue_piece
                        elif (board[each_row - continue_piece][each_column - continue_piece] != previous_piece and
                              board[each_row - continue_piece][
                                  each_column - continue_piece] != "-"):  # if the left side of this line is blocked by opponent
                            score = continue_piece
                        else:
                            score = get_line_score(continue_piece, m) / 2

                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row
                            col = each_column
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row - 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row
                            col = each_column
                            for i in range(continue_piece):
                                circle_in_line.add((row, col))
                                row = row - 1
                                col = col - 1

                else:
                    if (continue_piece != 1 and previous_piece != "-"):  # if the current piece different from top piece
                        score = get_line_score(continue_piece, m)
                        if (board[each_row][
                            each_column] != "-" and each_row - continue_piece == each_scan_start):  # if the left piece of this line is at the boundary of the board, and the right side is also blocked
                            score = continue_piece
                        elif (board[each_row][
                                  each_column] == "-" and each_row - continue_piece == each_scan_start):  # if the left piece of this line is al the most left position of the board, and the right side is not blocked
                            score = score / 2
                        elif (board[each_row][each_column] != "-" and board[each_row - continue_piece - 1][
                            each_column - continue_piece - 1] != "-"):  # if both sides of the line are blocked
                            score = continue_piece
                        elif (board[each_row][each_column] != board[each_row - continue_piece - 1][
                            each_column - continue_piece - 1]):  # if just one side of the line are blocked
                            score = score / 2
                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row - 1
                            col = each_column - 1
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row - 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row - 1
                            col = each_column - 1
                            for i in range(continue_piece):
                                cross_in_line.add((row, col))
                                row = row - 1
                                col = col - 1
                        continue_piece = 1
                        score = 0
                previous_piece = board[each_row][each_column]
                each_row = each_row + 1
                each_column = each_column + 1
        else:  # this is the right_top part

            start_row = 0
            start_column = each_scan_start - size + 1
            each_row = start_row
            each_column = start_column
            previous_piece = "-"
            continue_piece = 1
            score = 0
            while (each_column <= size - 1):
                if (board[each_row][each_column] == 'O'):  # all_circle stores all circles' positions
                    all_circle.add((each_row, each_column))
                if (board[each_row][each_column] == 'X'):  # all_cross stores all crosses' positions
                    all_cross.add((each_row, each_column))
                if (board[each_row][
                    each_column] == previous_piece and previous_piece != "-"):  # if current piece is same to previous piece
                    continue_piece = continue_piece + 1
                    if (continue_piece == m):  # the game is over
                        if (board[each_row][each_column] == myself):
                            return get_line_score(continue_piece, m)
                        else:
                            return -get_line_score(continue_piece, m)
                    if (each_column == size - 1):  # if current piece is at the right boundary of the board
                        if (
                                each_row - continue_piece + 1 == 0):  # if left piece of this line is at the top boundary of the board
                            score = continue_piece
                        elif (board[each_row - continue_piece][each_column - continue_piece] != previous_piece and
                              board[each_row - continue_piece][
                                  each_column - continue_piece] != "-"):  # if the left side of this line is blocked by opponent
                            score = continue_piece
                        else:
                            score = get_line_score(continue_piece, m) / 2

                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row
                            col = each_column
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row - 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row
                            col = each_column
                            for i in range(continue_piece):
                                circle_in_line.add((row, col))
                                row = row - 1
                                col = col - 1

                else:
                    if (
                            continue_piece != 1 and previous_piece != "-"):  # if the current piece is different from previous piece
                        score = get_line_score(continue_piece, m)
                        if (board[each_row][
                            each_column] != "-" and each_row - continue_piece == 0):  # if the left piece of this line is at the boundary of the board, and the right side is also blocked
                            score = continue_piece
                        elif (board[each_row][
                                  each_column] == "-" and each_row - continue_piece == 0):  # if the left piece of this line is at the most left position of the board, and the right side is not blocked
                            score = score / 2
                        elif (board[each_row][each_column] != "-" and board[each_row - continue_piece - 1][
                            each_column - continue_piece - 1] != "-"):  # if both sides of the line are blocked
                            score = continue_piece
                        elif (board[each_row][each_column] != board[each_row - continue_piece - 1][
                            each_column - continue_piece - 1]):  # if just one side of the line are blocked
                            score = score / 2
                        if (previous_piece == 'O'):
                            circle_score = circle_score + score
                            row = each_row - 1
                            col = each_column - 1
                            for i in range(
                                    continue_piece):  # store all pieces' position which forms a line (>2 continuous pieces) in the corresponding set
                                circle_in_line.add((row, col))
                                row = row - 1
                                col = col - 1

                        else:
                            cross_score = cross_score - score
                            row = each_row - 1
                            col = each_column - 1
                            for i in range(continue_piece):
                                cross_in_line.add((row, col))
                                row = row - 1
                                col = col - 1
                        continue_piece = 1
                        score = 0
                previous_piece = board[each_row][each_column]
                each_row = each_row + 1
                each_column = each_column + 1

    circle_score = circle_score + len(all_circle - circle_in_line)
    cross_score = cross_score - len(all_cross - cross_in_line)
    if (myself == "O"):
        return max(min(circle_score + cross_score, max_score_if_not_ending(size, m)), -max_score_if_not_ending(size, m))
    else:
        return max(min(-circle_score - cross_score, max_score_if_not_ending(size, m)),
                   -max_score_if_not_ending(size, m))


if __name__ == "__main__":
    game_str = '-OOOO---\n---X----\n---X----\n---X----\n---X----\n---X----\n--------\n--------\n'
    print(calculate_board_value(game_str, 5, "O"))
