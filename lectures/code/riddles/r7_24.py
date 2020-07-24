class Example:
    # static data
    foo = 0

    def __init__(self):
        # non-static data
        self.bar = 0

    # TODO: decide on parameters
    def handle_move(self, p1, p2, p3):
        # TODO: update board state
        # TODO: calculate and return win
        return False


class Accumulator:
    class BoardInfo:
        def __init__(self):
            self.rows = [0, 0, 0]
            self.cols = [0, 0, 0]
            self.left_diag = 0
            self.right_diag = 0

    def __init__(self):
        self.clear()

    # Ops: 22
    # Non-static space: 17
    # Static space: 0
    def handle_move(self, row, col):
        cur_board = self.boards[self.player]  # 2

        cur_board.rows[row] += 1  # 2
        win = cur_board.rows[row] > 2  # 3

        cur_board.cols[col] += 1  # 2
        win |= cur_board.cols[col] > 2  # 3

        cur_board.left_diag += row == col  # 2
        win |= cur_board.left_diag > 2  # 2

        cur_board.right_diag += row + col == 2  # 3
        win |= cur_board.right_diag > 2  # 2

        self.player ^= 1  # 1
        return win

    def clear(self):
        self.boards = [self.BoardInfo(), self.BoardInfo()]
        self.player = 0


class Bits:
    rows = [0b000000111, 0b000111000, 0b111000000]
    cols = [0b001001001, 0b010010010, 0b100100100]
    left_diag = 0b100010001
    right_diag = 0b001010100

    def __init__(self):
        self.clear()

    # Ops: 24
    # Non-static space: 3
    # Static space: 8
    def handle_move(self, row, col):
        self.board[self.player] |= 1 << (row * 3 + col)  # 5
        cur_board = self.board[self.player]  # 2

        cur_row = self.rows[row]  # 2
        win = (cur_board & cur_row) == cur_row  # 3

        cur_col = self.cols[col]  # 2
        win |= (cur_board & cur_col) == cur_col  # 3

        win |= (cur_board & self.left_diag) == self.left_diag  # 3
        win |= (cur_board & self.right_diag) == self.right_diag  # 3

        self.player ^= 1  # 1
        return win

    def clear(self):
        self.board = [0, 0]
        self.player = 0


class BitLookup:
    win_boards = [
        0b000000111,
        0b000111000,
        0b111000000,
        0b001001001,
        0b010010010,
        0b100100100,
        0b100010001,
        0b001010100,
    ]
    table = [False] * 512

    def __init__(self):
        for i in range(0, len(self.table)):
            for win in self.win_boards:
                self.table[i] |= (i & win) == win
        self.clear()

    # Ops: 9
    # Non-static space: 3
    # Static space: 520
    def handle_move(self, row, col):
        self.board[self.player] |= 1 << (row * 3 + col)  # 5
        win = self.table[self.board[self.player]]  # 3

        self.player ^= 1  # 1
        return win

    def clear(self):
        self.board = [0, 0]
        self.player = 0


tic_tac1 = Accumulator()
tic_tac2 = Bits()
tic_tac3 = BitLookup()

moves = [(0, 0), (1, 1), (1, 2), (2, 1), (0, 1), (2, 2), (0, 2)]

for move in moves:
    print(tic_tac1.handle_move(move[0], move[1]))
    print(tic_tac2.handle_move(move[0], move[1]))
    print(tic_tac3.handle_move(move[0], move[1]))
    print()
