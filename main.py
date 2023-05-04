import random


class Game:
    def __init__(self):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

    def clear_board(self):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

    def print(self):
        for i in range(4):
            for j in range(4):
                print(self.board[i][j], end=" ")
            print()

    @property
    def is_board_full(self):
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return False
        return True

    def is_game_over(self):
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return False

        for row in range(4):
            for col in range(4):
                if col < 3 and self.board[row][col] == self.board[row][col + 1]:
                    return False
                if row < 3 and self.board[row][col] == self.board[row + 1][col]:
                    return False

        return True

    def put_2_or_4(self, k):
        while k > 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if self.board[row][col] == 0:
                chance = random.randint(0, 10)
                if chance <= 8:
                    self.board[row][col] = 2
                else:
                    self.board[row][col] = 4
                k -= 1
        return self.board

    def slide(self, direct):
        merged = [[False for _ in range(4)] for _ in range(4)]

        if direct == 'up':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    if i > 0:
                        for q in range(i):
                            if self.board[q][j] == 0:
                                shift += 1
                        if shift > 0:
                            self.board[i - shift][j] = self.board[i][j]
                            self.board[i][j] = 0
                        if self.board[i - shift - 1][j] == self.board[i - shift][j] and not merged[i - shift - 1][j] \
                                and not merged[i - shift][j]:
                            self.board[i - shift - 1][j] *= 2
                            self.board[i - shift][j] = 0
                            merged[i - shift - 1][j] = True

        elif direct == 'down':
            for i in range(3):
                for j in range(4):
                    shift = 0
                    for q in range(i + 1):
                        if self.board[3 - q][j] == 0:
                            shift += 1
                    if shift > 0:
                        self.board[2 - i + shift][j] = self.board[2 - i][j]
                        self.board[2 - i][j] = 0
                    if 3 - i + shift <= 3:
                        if self.board[2 - i + shift][j] == self.board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                                and not merged[2 - i + shift][j]:
                            self.board[3 - i + shift][j] *= 2
                            self.board[2 - i + shift][j] = 0
                            merged[3 - i + shift][j] = True

        elif direct == 'left':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if self.board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        self.board[i][j - shift] = self.board[i][j]
                        self.board[i][j] = 0
                    if self.board[i][j - shift] == self.board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                            and not merged[i][j - shift]:
                        self.board[i][j - shift - 1] *= 2
                        self.board[i][j - shift] = 0
                        merged[i][j - shift - 1] = True

        elif direct == 'right':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if self.board[i][3 - q] == 0:
                            shift += 1
                    if shift > 0:
                        self.board[i][3 - j + shift] = self.board[i][3 - j]
                        self.board[i][3 - j] = 0
                    if 4 - j + shift <= 3:
                        if self.board[i][4 - j + shift] == self.board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                                and not merged[i][3 - j + shift]:
                            self.board[i][4 - j + shift] *= 2
                            self.board[i][3 - j + shift] = 0
                            merged[i][4 - j + shift] = True
        if not self.is_board_full:
            self.put_2_or_4(1)
        return self


gme = Game()
gme.put_2_or_4(2)
while True:
    gme.print()
    line = input()
    gme.slide(line)
