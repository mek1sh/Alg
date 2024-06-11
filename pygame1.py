import pygame as pg

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sc):
        PINK = (222, 49, 99)
        color = {0: (0, 0, 0), 1: PINK}
        for x in range(self.width):
            for y in range(self.height):
                pg.draw.rect(sc, color[self.board[y][x]], (self.left + x * self.cell_size,
                                        self.left + y * self.cell_size,
                                        self.cell_size, self.cell_size), 0)
                pg.draw.rect(sc, PINK, (self.left + x * self.cell_size,
                                        self.left + y * self.cell_size,
                                        self.cell_size, self.cell_size), 1)

    def cell(self, mouse_pos):
        mx, my = mouse_pos
        if self.left <= mx <= self.left + self.width * self.cell_size and \
            self.top <= my <= self.top + self.height * self.cell_size:
            mx -= self.left
            my -= self.top
            return (mx // self.cell_size,
                    my // self.cell_size)
        return None

    def on_click(self, cell):
        x, y = cell
        self.board[y][x] = int(self.board[y][x] == 0)
        for i in range(self.width):
            self.board[y][i] = 1 - self.board[y][i]
        for i in range(self.height):
            self.board[i][x] = 1 - self.board[i][x]

if __name__ == '__main__':
    pg.init()
    sc = pg.display.set_mode((1000, 1000))
    board = Board(10, 10)
    board.set_view(10, 10, 30)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                cell = board.cell(event.pos)
                if cell:
                    board.on_click(cell)
        sc.fill((0, 0, 0))
        board.render(sc)
        pg.display.flip()
    pg.quit()




