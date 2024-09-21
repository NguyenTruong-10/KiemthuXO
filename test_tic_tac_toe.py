import pytest
from PyQt5.QtWidgets import QApplication
from tic_tac_toe import TicTacToe
from PyQt5.QtCore import Qt

@pytest.fixture
def app(qtbot):
    test_app = TicTacToe()
    qtbot.addWidget(test_app)
    return test_app

# TC001: Kiểm tra giao diện khởi động trò chơi
def test_initial_game_state(app):
    assert app.current_player == 'X'
    assert app.turn_label.text() == 'Đến lượt: X'
    for row in app.board:
        assert all(cell == '' for cell in row)

# TC002: Kiểm tra di chuyển của người chơi X đầu tiên
def test_make_move(app, qtbot):
    button = app.buttons[0][0]
    qtbot.mouseClick(button, Qt.LeftButton)
    assert button.text() == 'X'
    assert app.board[0][0] == 'X'
    assert app.current_player == 'O'

# TC003: Kiểm tra di chuyển của người chơi O sau người chơi X
def test_alternate_moves(app, qtbot):
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    assert app.current_player == 'O'
    qtbot.mouseClick(app.buttons[0][1], Qt.LeftButton)
    assert app.current_player == 'X'

# TC004: Kiểm tra thắng lợi khi người chơi X có 4 dấu X liên tiếp không bị chặn ở cả hai đầu
def test_winner_detection_X(app, qtbot):
    for i in range(4):
        qtbot.mouseClick(app.buttons[0][i], Qt.LeftButton)
        if i < 3:
            qtbot.mouseClick(app.buttons[1][i], Qt.LeftButton)
    assert app.game_over is True
    assert app.turn_label.text() == 'Người chơi X thắng!'

# TC005: Kiểm tra thắng lợi khi người chơi X có 5 dấu liên tiếp bị chặn ở một đầu
def test_blocked_win_condition_X(app, qtbot):
    qtbot.mouseClick(app.buttons[0][1], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][2], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[1][2], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][3], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[1][3], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][4], Qt.LeftButton)
    assert app.game_over is False
    qtbot.mouseClick(app.buttons[0][5], Qt.LeftButton)
    assert app.game_over is True
    assert app.turn_label.text() == 'Người chơi X thắng!'

# TC006: Kiểm tra thắng lợi của người chơi O khi có 4 dấu O liên tiếp không bị chặn
def test_winner_detection_O(app, qtbot):
    for i in range(4):
        qtbot.mouseClick(app.buttons[i][0], Qt.LeftButton)
        if i < 3:
            qtbot.mouseClick(app.buttons[i][1], Qt.LeftButton)
    assert app.game_over is True
    assert app.turn_label.text() == 'Người chơi O thắng!'

# TC007: Kiểm tra trạng thái hòa khi lưới đầy nhưng không có người thắng
def test_draw_condition(app, qtbot):
    for i in range(app.grid_size):
        for j in range(app.grid_size):
            if (i + j) % 2 == 0:
                qtbot.mouseClick(app.buttons[i][j], Qt.LeftButton)
            else:
                qtbot.mouseClick(app.buttons[i][j], Qt.LeftButton)
    assert app.game_over is True
    assert app.turn_label.text() == 'Trò chơi hòa!'

# TC008: Kiểm tra chức năng reset trò chơi
def test_reset_game(app, qtbot):
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    qtbot.mouseClick(app.reset_button, Qt.LeftButton)
    assert app.current_player == 'X'
    assert app.turn_label.text() == 'Đến lượt: X'
    for row in app.board:
        assert all(cell == '' for cell in row)
    assert app.game_over is False

# TC009: Kiểm tra di chuyển vào ô đã được đánh dấu trước đó
def test_move_on_marked_cell(app, qtbot):
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    assert app.buttons[0][0].text() == 'X'
    assert app.current_player == 'O'

# TC010: Kiểm tra thay đổi màu chữ hiển thị lượt khi chuyển lượt
def test_turn_color_change(app, qtbot):
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    assert 'color: blue;' in app.turn_label.styleSheet()  # Assuming blue color for X
    qtbot.mouseClick(app.buttons[0][1], Qt.LeftButton)
    assert 'color: red;' in app.turn_label.styleSheet()  # Assuming red color for O

# TC011: Kiểm tra thông báo khi người chơi O có 5 dấu O liên tiếp bị chặn một đầu
def test_winner_detection_blocked_O(app, qtbot):
    qtbot.mouseClick(app.buttons[0][1], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][2], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[1][2], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][3], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[1][3], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][4], Qt.LeftButton)
    assert app.game_over is False
    qtbot.mouseClick(app.buttons[0][5], Qt.LeftButton)
    assert app.game_over is True
    assert app.turn_label.text() == 'Người chơi O thắng!'

# TC012: Kiểm tra không hiển thị thông báo khi chưa có chuỗi 4 hoặc 5 liên tiếp
def test_no_win_message_without_consecutive_marks(app, qtbot):
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[1][1], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[2][2], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[3][3], Qt.LeftButton)
    qtbot.mouseClick(app.buttons[4][4], Qt.LeftButton)
    assert app.game_over is False
    assert 'Người chơi X thắng!' not in app.turn_label.text()
    assert 'Người chơi O thắng!' not in app.turn_label.text()

# TC013: Kiểm tra lưới trò chơi với kích thước 20x20
def test_grid_size_20x20(app, qtbot):
    assert len(app.buttons) == 20
    assert len(app.buttons[0]) == 20
    assert app.grid_size == 20

# TC014: Kiểm tra tỷ số khi người chơi X thắng
def test_score_update_on_win_X(app, qtbot):
    for i in range(4):
        qtbot.mouseClick(app.buttons[0][i], Qt.LeftButton)
        if i < 3:
            qtbot.mouseClick(app.buttons[1][i], Qt.LeftButton)
    assert app.score_x == 1
    assert app.score_o == 0

# TC015: Kiểm tra tỷ số khi người chơi O thắng
def test_score_update_on_win_O(app, qtbot):
    for i in range(4):
        qtbot.mouseClick(app.buttons[i][0], Qt.LeftButton)
        if i < 3:
            qtbot.mouseClick(app.buttons[i][1], Qt.LeftButton)
    assert app.score_x == 0
    assert app.score_o == 1

# TC016: Kiểm tra tỷ số sau khi reset trò chơi
def test_score_reset_on_game_reset(app, qtbot):
    for i in range(4):
        qtbot.mouseClick(app.buttons[0][i], Qt.LeftButton)
        if i < 3:
            qtbot.mouseClick(app.buttons[1][i], Qt.LeftButton)
    qtbot.mouseClick(app.reset_button, Qt.LeftButton)
    assert app.score_x == 0
    assert app.score_o == 0

# TC017: Kiểm tra không thay đổi tỷ số khi chỉ reset lưới mà không phải tỷ số
def test_score_not_reset_on_grid_reset(app, qtbot):
    for i in range(4):
        qtbot.mouseClick(app.buttons[0][i], Qt.LeftButton)
        if i < 3:
            qtbot.mouseClick(app.buttons[1][i], Qt.LeftButton)
    qtbot.mouseClick(app.reset_button, Qt.LeftButton)
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    assert app.score_x == 1
    assert app.score_o == 0

# TC018: Kiểm tra tỷ số sau khi một người thắng và reset lưới nhưng không reset tỷ số
def test_score_not_reset_after_win(app, qtbot):
    for i in range(4):
        qtbot.mouseClick(app.buttons[0][i], Qt.LeftButton)
        if i < 3:
            qtbot.mouseClick(app.buttons[1][i], Qt.LeftButton)
    qtbot.mouseClick(app.reset_button, Qt.LeftButton)
    assert app.score_x == 1
    assert app.score_o == 0

# TC019: Kiểm tra màu sắc chữ khi lượt chuyển tiếp giữa các người chơi
def test_turn_color_change_alternating(app, qtbot):
    qtbot.mouseClick(app.buttons[0][0], Qt.LeftButton)
    assert 'color: blue;' in app.turn_label.styleSheet()  # Assuming blue color for X
    qtbot.mouseClick(app.buttons[0][1], Qt.LeftButton)
    assert 'color: red;' in app.turn_label.styleSheet()  # Assuming red color for O
    qtbot.mouseClick(app.buttons[0][2], Qt.LeftButton)
    assert 'color: blue;' in app.turn_label.styleSheet()  # Assuming blue color for X

# TC020: Kiểm tra số lần di chuyển của người chơi trước khi thắng hoặc hòa
def test_move_count_before_end(app, qtbot):
    move_count = 0
    for i in range(app.grid_size):
        for j in range(app.grid_size):
            if not app.game_over:
                qtbot.mouseClick(app.buttons[i][j], Qt.LeftButton)
                move_count += 1
            if app.game_over:
                break
        if app.game_over:
            break
    assert move_count > 0
