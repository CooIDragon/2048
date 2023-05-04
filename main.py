import random

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QMessageBox, QPushButton
import sys


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

    @staticmethod
    def on_player_state_changed(state):
        if state == QMediaPlayer.StoppedState:
            player.play()


play = QMediaPlayer()
play.setMedia(QMediaContent(QUrl.fromLocalFile('sound.mp3')))

meow = QMediaPlayer()
meow.setMedia(QMediaContent(QUrl.fromLocalFile('meow.mp3')))

kefteme = QMediaPlayer()
kefteme.setMedia(QMediaContent(QUrl.fromLocalFile('kefteme.mp3')))

player = QMediaPlayer()
player.setMedia(QMediaContent(QUrl.fromLocalFile('audio.mp3')))
player.setVolume(5)
player.stateChanged.connect(Game.on_player_state_changed)


class MatrixTable(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)
        self.fill_table(game.board)

    def show_rules(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Правила")
        msg_box.setText("Конечная цель игры 2048 - получить плитку с числом 2048 на игровом поле. \nНачальный набор игры состоит из двух плиток с числами 2 или 4.\nПравила игры:\nИгровое поле состоит из 4x4 квадратов.\nИгрок может сделать ход, передвигая плитки на поле в одном из четырех направлений: вверх, вниз, влево или вправо.\nЕсли две плитки с одинаковыми числами встречаются в процессе передвижения, они объединяются в одну плитку, сумма чисел на которой равна сумме чисел на двух объединяемых плитках.\nПосле каждого хода на случайном месте на игровом поле появляется новая плитка со значением 2 или 4.\nИгрок проигрывает, если на игровом поле не осталось свободных квадратов, в которые можно поместить новую плитку, либо если он не может сделать ход, который приведет к объединению плиток.Подсказка: старайтесь объединять плитки с более высокими значениями, чтобы освобождать место для новых плиток и продолжать игру. Удачи!")
        msg_box.exec()

    def end_of_the_game(self):
        kefteme.play()

        msg = QMessageBox()
        msg.setWindowTitle("Конец игры")
        msg.setText("Игра окончена")
        msg.setIcon(QMessageBox.Information)

        msg.addButton(QMessageBox.Ok)
        msg.addButton(QMessageBox.Reset)

        result = msg.exec_()
        if result == QMessageBox.Ok:
            QApplication.quit()
        else:
            self.game.clear_board()
            self.update_table(self.game.put_2_or_4(2))

    def first_nums(self):
        self.update_table(self.game.put_2_or_4(2))

    def fill_table(self, matrix):
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                if matrix[row][col] == 0:
                    label = QLabel('')
                else:
                    label = QLabel(str(matrix[row][col]))
                label.setMinimumSize(75, 75)
                label.setStyleSheet(
                    'QLabel { background-color: #eee; border: 1px solid #ccc; font-size: 24px; font-weight: bold; text-align: center; }')
                self.grid.addWidget(label, row, col)

    def update_table(self, new_matrix):
        if self.game.is_game_over():
            MatrixTable.end_of_the_game(self)
        self.fill_table(new_matrix)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left:
            self.game.slide('left')
            play.play()
        elif event.key() == Qt.Key_Right:
            self.game.slide('right')
            play.play()
        elif event.key() == Qt.Key_Up:
            self.game.slide('up')
            play.play()
        elif event.key() == Qt.Key_Down:
            self.game.slide('down')
            play.play()
        elif event.key() == Qt.Key_H:
            meow.play()
            self.show_rules()
        elif event.key() == Qt.Key_R:
            kefteme.play()
            self.game.clear_board()
            self.update_table(self.game.put_2_or_4(2))
            return
        self.update_table(self.game.board)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gme = Game()
    table = MatrixTable(gme)
    MatrixTable.first_nums(table)
    table.show()
    player.play()
    sys.exit(app.exec_())
