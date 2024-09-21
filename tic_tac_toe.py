import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_size = 20
        self.x_score = 0
        self.o_score = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('4 Chặn 5 - Tic-Tac-Toe 50x50')

        self.main_layout = QVBoxLayout()

        self.turn_label = QLabel('Đến lượt: X')
        self.turn_label.setStyleSheet("font-size: 20px; color: blue;")
        self.main_layout.addWidget(self.turn_label, alignment=Qt.AlignCenter)

        self.score_label = QLabel(f'Điểm số: X - {self.x_score} | O - {self.o_score}')
        self.score_label.setStyleSheet("font-size: 18px;")
        self.main_layout.addWidget(self.score_label, alignment=Qt.AlignCenter)

        self.reset_button = QPushButton('Reset trò chơi')
        self.reset_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.reset_button.clicked.connect(self.reset_scores)
        self.main_layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)

        self.grid = QGridLayout()
        self.main_layout.addLayout(self.grid)

        self.buttons = [[QPushButton('') for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].setFixedSize(40, 40)
                self.buttons[i][j].clicked.connect(self.make_move)
                self.grid.addWidget(self.buttons[i][j], i, j)
        self.grid.setSpacing(0)

        self.current_player = 'X'
        self.board = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.game_over = False

        self.setLayout(self.main_layout)

    def make_move(self):
        button = self.sender()
        if button.text() == '' and not self.game_over:
            button.setText(self.current_player)
            row, col = self.get_button_pos(button)
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                QMessageBox.information(self, 'Kết thúc', f'Người chơi {self.current_player} thắng!')
                self.game_over = True
                self.turn_label.setText(f'Người chơi {self.current_player} thắng!')
                if self.current_player == 'X':
                    self.x_score += 1
                else:
                    self.o_score += 1
                self.update_score()
                QTimer.singleShot(2000, self.reset_game)
            elif all(all(cell != '' for cell in row) for row in self.board):
                QMessageBox.information(self, 'Kết thúc', 'Trò chơi hòa!')
                self.game_over = True
                self.turn_label.setText('Trò chơi hòa!')
                QTimer.singleShot(2000, self.reset_game)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.turn_label.setText(f'Đến lượt: {self.current_player}')
                self.turn_label.setStyleSheet(f"font-size: 20px; color: {'blue' if self.current_player == 'X' else 'red'}")

    def get_button_pos(self, button):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.buttons[i][j] == button:
                    return i, j
        return -1, -1

    def check_winner(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        return any(self.check_line(row, col, dr, dc) for dr, dc in directions)

    def check_line(self, row, col, delta_row, delta_col):
        count = 0
        blocked_ends = 0

        r, c = row, col
        while 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.board[r][c] == self.current_player:
            count += 1
            r += delta_row
            c += delta_col

        if 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.board[r][c] != '':
            blocked_ends += 1

        r, c = row - delta_row, col - delta_col
        while 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.board[r][c] == self.current_player:
            count += 1
            r -= delta_row
            c -= delta_col

        if 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.board[r][c] != '':
            blocked_ends += 1

        return (blocked_ends == 0 and count >= 4) or (blocked_ends == 1 and count >= 5)

    def reset_game(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].setText('')
        self.board = [['' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.current_player = 'X'
        self.turn_label.setText('Đến lượt: X')
        self.turn_label.setStyleSheet("font-size: 20px; color: blue;")
        self.game_over = False

    def reset_scores(self):
        self.x_score = 0
        self.o_score = 0
        self.update_score()

    def update_score(self):
        self.score_label.setText(f'Điểm số: X - {self.x_score} | O - {self.o_score}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tictactoe = TicTacToe()
    tictactoe.show()
    sys.exit(app.exec())
