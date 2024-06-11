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
        color = {0: (0, 0, 0), 1: 'PINK'}
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
        if not(cell is None):
            x, y = cell
            self.board[y][x] = int(self.board[y][x] == 0)

    def get_click(self, mouse_pos):
        cell = self.cell(mouse_pos)
        self.on_click(cell)
        print(cell)



if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 1000
    sc = pg.display.set_mode(size)
    board = Board(10, 10)
    board.set_view(100, 100, 50)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pg.QUIT:
                running = False
        sc.fill((0, 0, 0))
        board.render(sc)
        pg.display.flip()
    pg.quit()

