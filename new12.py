import random
import sys
import pygame

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0] * width for _ in range(height)]
        self.revead = [[False] * width for _ in range(height)]
        self.flagged = [[False] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.__place_mines()

    def __place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1
                self.__update_numbers_around_mine(x, y)

    def __update_numbers_around_mine(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < self.width and 0 <= y + j < self.height and self.board[y + j][x + i]!= -1:
                    self.board[y + j][x + i] += 1

    def reveal(self, x, y):
        if self.is_flagged(x, y) or self.is_revealed(x, y) or self.is_mine(x, y):
            return
        self.revead[y][x] = True
        if self.board[y][x] == 0:
            for i in range(max(0, y - 1), min(y + 2, self.height)):
                for j in range(max(0, x - 1), min(x + 2, self.width)):
                    self.reveal(j, i)
        return True

    def flag(self, x, y):
        if not (self.is_revealed(x, y)):
            self.flagged[y][x] = not (self.flagged[y][x])

    def is_mine(self, x, y):
        return self.board[y][x] == -1

    def is_revealed(self, x, y):
        return self.revead[y][x]

    def is_flagged(self, x, y):
        return self.flagged[y][x]

    def get_cell_value(self, x, y):
        return self.board[y][x]

    def all_cells_revealed(self):
        for x in range(self.width):
            for y in range(self.height):
                if not (self.is_mine(x, y)):
                    if not (self.is_revealed(x, y)):
                        return False
        return True




NAME = 'PKO'
CELL_SIZE = 25
HEADER_HEIGHT = 100
BUTTON_HEIGHT = 50
FONT_SIZE = 24

# Цветовые константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
DARK_GREY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
font = pygame.font.SysFont(None, FONT_SIZE)

def draw_board(screen, board, game_over):
    for x in range(board.width):
        for y in range(board.height):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + HEADER_HEIGHT, CELL_SIZE, CELL_SIZE)
            color = GREY if board.is_revealed(x, y) else WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            if board.is_revealed(x, y):
                value = board.get_cell_value(x, y)
                if value == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
                elif value > 0:
                    text = font.render(str(value), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)

                    screen.blit(text, text_rect)

            elif board.is_flagged(x, y):
                pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 2)

            if game_over and board.is_mine(x, y):
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)

def draw_text(sc, text, width):
    text_render = font.render(text, True, BLACK)
    text_rect = text_render.get_rect(center=(width * CELL_SIZE / 2, BUTTON_HEIGHT + FONT_SIZE // 2 + 10))
    sc.blit(text_render, text_rect)

def draw_button(sc, text, x, y, width, height, color):
    pygame.draw.rect(sc, color, (x, y, width, height))
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(x + width / 2, y + height / 2))
    sc.blit(text_render, text_rect)

def main():
    levels = [(10, 10, 10), (16, 16, 40), (30, 30, 99)]
    width, height, num_mines = levels[0]
    screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE + HEADER_HEIGHT))
    pygame.display.set_caption('САПЁР')
    board = Board(width, height, num_mines)
    game_over = False
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 0 <= mouse_x <= width * CELL_SIZE and 0 <= mouse_y <= BUTTON_HEIGHT:
                    board = Board(width, height, num_mines)
                    game_over = False
                    win = False

                elif not game_over:
                    x, y = mouse_x // CELL_SIZE, (mouse_y - HEADER_HEIGHT) // CELL_SIZE
                    if 0 <= x < width and 0 <= y < height:
                        if event.button == 1:
                            if not (board.is_flagged(x, y)) and board.is_mine(x, y):
                                game_over = True
                            else:
                                board.reveal(x, y)
                                if board.all_cells_revealed():
                                    win = True
                                    game_over = True

                        elif event.button == 3:
                            board.flag(x, y)

        screen.fill(WHITE)
        draw_board(screen, board, game_over)
        draw_button(screen, "НОВАЯ ИГРА", 0, 0, width * CELL_SIZE, BUTTON_HEIGHT, BLUE)
        if game_over:
            result_text = "ВЫ ПОБЕДИТЕЛЬ!" if win else "ИГРА ОКОНЧЕНА!"
            draw_text(screen, result_text, width)

        else:
            draw_text(screen, "САПЁР by " + NAME, width)
        pygame.display.flip()


if __name__ == '__main__':
    main()




