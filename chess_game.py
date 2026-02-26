# Импортируем библиотеку pygame для создания игры
import pygame
# Импортируем sys для корректного закрытия программы
import sys

# Инициализируем все модули pygame
pygame.init()

# Константы (переменные, которые не меняются)
# Определяем размеры шахматной доски
CELL_SIZE = 80  # Размер одной клетки в пикселях
BOARD_SIZE = 8  # Размер доски (8x8 клеток)
WINDOW_WIDTH = CELL_SIZE * BOARD_SIZE  # Ширина окна: 80 * 8 = 640
WINDOW_HEIGHT = CELL_SIZE * BOARD_SIZE  # Высота окна: 80 * 8 = 640

# Цвета в формате RGB (Red, Green, Blue)
WHITE = (255, 255, 255)  # Белый цвет
BLACK = (0, 0, 0)  # Черный цвет
BROWN = (118, 150, 86)  # Светло-коричневый для светлых клеток
DARK_BROWN = (86, 118, 50)  # Темно-коричневый для темных клеток
GRAY = (128, 128, 128)  # Серый цвет для подсветки
RED = (255, 0, 0)  # Красный цвет для выделения


class ChessGame:

    # здесь вся логика игры

    def __init__(self):
        #Конструктор класса - вызывается при создании объекта
        # Создаем игровое окно с заданными размерами
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # Устанавливаем заголовок окна
        pygame.display.set_caption("Шахматы")

        # Создаем доску - список списков
        self.board = self.create_board()

        # Переменная для хранения выбранной клетки (None - ничего не выбрано)
        self.selected = None
        # Переменная для хранения текущего игрока (True - белые, False - черные)
        self.current_player = True  # True = белые ходят первыми
        # Список для хранения допустимых ходов выбранной фигуры
        self.valid_moves = []
        # Часы для контроля времени (чтобы игра работала с одинаковой скоростью)
        self.clock = pygame.time.Clock()

    def create_board(self):

    #начальная расстановка фигур
        # Создаем пустую доску 8x8, заполненную пробелами
        board = [[' ' for _ in range(8)] for _ in range(8)]

        # Расставляем черные фигуры (верхняя часть доски)
        # Черные фигуры обозначаем строчными буквами
        board[0][0] = 'r'  # Ладья (rook)
        board[0][1] = 'n'  # Конь (knight)
        board[0][2] = 'b'  # Слон (bishop)
        board[0][3] = 'q'  # Ферзь (queen)
        board[0][4] = 'k'  # Король (king)
        board[0][5] = 'b'  # Слон
        board[0][6] = 'n'  # Конь
        board[0][7] = 'r'  # Ладья

        # Черные пешки
        for i in range(8):
            board[1][i] = 'p'

        # Расставляем белые фигуры (нижняя часть доски)
        # Белые фигуры обозначаем заглавными буквами
        board[7][0] = 'R'  # Ладья
        board[7][1] = 'N'  # Конь
        board[7][2] = 'B'  # Слон
        board[7][3] = 'Q'  # Ферзь
        board[7][4] = 'K'  # Король
        board[7][5] = 'B'  # Слон
        board[7][6] = 'N'  # Конь
        board[7][7] = 'R'  # Ладья

        # Белые пешки
        for i in range(8):
            board[6][i] = 'P'

        return board

    def draw_board(self):

    # создание шахматной доски

        # Проходим по всем клеткам доски
        for row in range(8):
            for col in range(8):
                # Определяем координаты клетки
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                # Определяем цвет клетки (шахматный порядок)
                if (row + col) % 2 == 0:
                    color = BROWN  # Светлая клетка
                else:
                    color = DARK_BROWN  # Темная клетка

                # Рисуем прямоугольник (клетку)
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))

                # Если клетка выбрана, рисуем подсветку
                if self.selected and self.selected == (row, col):
                    # Рисуем полупрозрачную подсветку
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    s.set_alpha(128)  # Полупрозрачность
                    s.fill(RED)
                    self.screen.blit(s, (x, y))

                # Если клетка является допустимым ходом, рисуем подсветку
                if (row, col) in self.valid_moves:
                    # Рисуем кружок для обозначения возможного хода
                    center_x = x + CELL_SIZE // 2
                    center_y = y + CELL_SIZE // 2
                    pygame.draw.circle(self.screen, GRAY, (center_x, center_y), 10)

    def draw_pieces(self):

    # создание фигур

        # Создаем шрифт для отрисовки фигур
        font = pygame.font.Font(None, CELL_SIZE - 10)

        # Проходим по всем клеткам доски
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ' ':  # Если в клетке есть фигура
                    # Определяем координаты для текста
                    x = col * CELL_SIZE + CELL_SIZE // 2 - 20
                    y = row * CELL_SIZE + CELL_SIZE // 2 - 30

                    # Словарь для преобразования букв в символы фигур
                    piece_symbols = {
                        'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
                        'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
                    }

                    # Получаем символ фигуры
                    symbol = piece_symbols.get(piece, piece)

                    # Определяем цвет фигуры
                    if piece.isupper():  # Заглавные буквы - белые фигуры
                        color = WHITE
                    else:  # Строчные буквы - черные фигуры
                        color = BLACK

                    # Создаем текст с фигурой
                    text = font.render(symbol, True, color)
                    # Рисуем текст на экране
                    self.screen.blit(text, (x, y))

    def get_valid_moves(self, row, col):

    # определение допустимых кодов
        piece = self.board[row][col]
        if piece == ' ':  # Если клетка пустая, нет ходов
            return []

        moves = []

        # Определяем ходы для каждой фигуры
        if piece.lower() == 'p':  # Пешка
            direction = -1 if piece.isupper() else 1  # Белые ходят вверх (-1), черные вниз (+1)
            start_row = 6 if piece.isupper() else 1  # Начальная позиция пешки

            # Ход на одну клетку вперед
            new_row = row + direction
            if 0 <= new_row < 8 and self.board[new_row][col] == ' ':
                moves.append((new_row, col))

                # Ход на две клетки с начальной позиции
                if row == start_row:
                    new_row = row + 2 * direction
                    if self.board[new_row][col] == ' ':
                        moves.append((new_row, col))

            # Взятие фигур по диагонали
            for dcol in [-1, 1]:
                new_col = col + dcol
                new_row = row + direction
                if 0 <= new_col < 8 and 0 <= new_row < 8:
                    target = self.board[new_row][new_col]
                    if target != ' ' and target.isupper() != piece.isupper():
                        moves.append((new_row, new_col))

        elif piece.lower() == 'r':  # Ладья
            # Ходы по горизонтали и вертикали
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                for i in range(1, 8):
                    new_row = row + dr * i
                    new_col = col + dc * i
                    if not (0 <= new_row < 8 and 0 <= new_col < 8):
                        break
                    if self.board[new_row][new_col] == ' ':
                        moves.append((new_row, new_col))
                    elif self.board[new_row][new_col].isupper() != piece.isupper():
                        moves.append((new_row, new_col))
                        break
                    else:
                        break

        elif piece.lower() == 'n':  # Конь
            # Все возможные ходы коня
            knight_moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for dr, dc in knight_moves:
                new_row = row + dr
                new_col = col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target == ' ' or target.isupper() != piece.isupper():
                        moves.append((new_row, new_col))

        elif piece.lower() == 'b':  # Слон
            # Ходы по диагоналям
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                for i in range(1, 8):
                    new_row = row + dr * i
                    new_col = col + dc * i
                    if not (0 <= new_row < 8 and 0 <= new_col < 8):
                        break
                    if self.board[new_row][new_col] == ' ':
                        moves.append((new_row, new_col))
                    elif self.board[new_row][new_col].isupper() != piece.isupper():
                        moves.append((new_row, new_col))
                        break
                    else:
                        break

        elif piece.lower() == 'q':  # Ферзь (комбинация ладьи и слона)
            # Все направления
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                for i in range(1, 8):
                    new_row = row + dr * i
                    new_col = col + dc * i
                    if not (0 <= new_row < 8 and 0 <= new_col < 8):
                        break
                    if self.board[new_row][new_col] == ' ':
                        moves.append((new_row, new_col))
                    elif self.board[new_row][new_col].isupper() != piece.isupper():
                        moves.append((new_row, new_col))
                        break
                    else:
                        break

        elif piece.lower() == 'k':  # Король
            # Ходы на одну клетку во все стороны
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row = row + dr
                    new_col = col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = self.board[new_row][new_col]
                        if target == ' ' or target.isupper() != piece.isupper():
                            moves.append((new_row, new_col))

        return moves

    def move_piece(self, from_pos, to_pos):
        """
        Перемещает фигуру с позиции from_pos на позицию to_pos.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Перемещаем фигуру
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ' '

        # Меняем игрока
        self.current_player = not self.current_player

    def handle_click(self, pos):
        """
        Обрабатывает клик мыши.
        pos - координаты клика (x, y)
        """
        # Определяем клетку, в которую кликнули
        col = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE

        # Проверяем, что клик в пределах доски
        if 0 <= row < 8 and 0 <= col < 8:
            # Если ничего не выбрано
            if self.selected is None:
                # Проверяем, что в клетке есть фигура и она принадлежит текущему игроку
                piece = self.board[row][col]
                if piece != ' ':
                    # Белые фигуры - заглавные, черные - строчные
                    if (self.current_player and piece.isupper()) or (not self.current_player and piece.islower()):
                        self.selected = (row, col)
                        self.valid_moves = self.get_valid_moves(row, col)
            else:
                # Если что-то выбрано, пробуем сделать ход
                if (row, col) in self.valid_moves:
                    self.move_piece(self.selected, (row, col))

                # Сбрасываем выбор
                self.selected = None
                self.valid_moves = []

    def run(self):

    # игровой цикл

        running = True

        while running:
            # Обрабатываем события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Нажатие на крестик
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Клик мыши
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Клавиша ESC для выхода
                        running = False

            # Отрисовываем все элементы
            self.draw_board()  # Сначала доску
            self.draw_pieces()  # Потом фигуры поверх доски

            # Обновляем экран
            pygame.display.flip()

            # Ограничиваем частоту кадров (60 FPS)
            self.clock.tick(60)

        # Завершаем игру
        pygame.quit()
        sys.exit()


# Создаем и запускаем игру, если файл запущен напрямую
if __name__ == "__main__":
    game = ChessGame()  # Создаем объект игры
    game.run()  # Запускаем игру