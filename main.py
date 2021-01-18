import pygame
from pygame.locals import *
import random


class Cell:

    def __init__(self):
        self._status = 0

    def set_dead(self):
        self._status = 0

    def set_alive(self):
        self._status = 1

    def is_alive(self):
        if self._status == 1:
            return True
        return False

    def get(self):
        return int(self._status)


class Board:

    def __init__(self, width: int = 500, height: int = 500, cell_size: int = 50, speed: int = 1.5, randomed=True):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size  # rows
        self.cell_height = self.height // self.cell_size  # columns

        self.cells = [[Cell() for i in range(self.cell_height)] for j in range(self.cell_width)]
        self.PAUSED = False

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость протекания игры
        self.speed = speed

        self.generate_board(randomed)

    def draw_lines(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def generate_board(self, randomed):
        if randomed:
            for row in self.cells:
                for column in row:
                    chance_number = random.randint(0, 2)
                    if chance_number == 1:
                        column.set_alive()
        else:
            pass

    def draw_by_mouse(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x = event.pos[0] // 50
                y = event.pos[1] // 50
                self.cells[y][x].set_alive()
                pygame.draw.rect(self.screen, pygame.Color('green'), (x * 50 + 1, y * 50 + 1, 49, 49))
            elif event.button == 3:
                x = event.pos[0] // 50
                y = event.pos[1] // 50
                self.cells[y][x].set_dead()
                pygame.draw.rect(self.screen, pygame.Color('white'), (x * 50 + 1, y * 50 + 1, 49, 49))
        pygame.display.flip()

    def draw_grid(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                if self.cells[j][i].is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'), (i * 50 + 1, j * 50 + 1, 49, 49))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (i * 50 + 1, j * 50 + 1, 49, 49))

    def update_board(self):
        new_cells = [[Cell() for i in range(self.cell_height)] for j in range(self.cell_width)]
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                if self.cells[i][j].is_alive():
                    new_cells[i][j].set_alive()

        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                neighbours = (self.cells[i][(j - 1) % 10].get() + self.cells[i][(j + 1) % 10].get() +
                              self.cells[(i - 1) % 10][j].get() + self.cells[(i + 1) % 10][j].get() +
                              self.cells[(i - 1) % 10][(j - 1) % 10].get() +
                              self.cells[(i - 1) % 10][(j + 1) % 10].get() +
                              self.cells[(i + 1) % 10][(j - 1) % 10].get() +
                              self.cells[(i + 1) % 10][(j + 1) % 10].get())

                if self.cells[i][j].is_alive():
                    if (neighbours < 2) or (neighbours > 3):
                        new_cells[i][j].set_dead()
                else:
                    if neighbours == 3:
                        new_cells[i][j].set_alive()

        self.cells = new_cells

    def run(self):
        caption = 'Game of Life'
        start = True
        game = True
        title = True
        add = False
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption(caption)
        pygame.display.flip()
        while game:
            while title:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        start = False
                        game = False
                        running = False
                        title = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_o:
                            title = False

                image = pygame.image.load('logo.jpg')
                self.screen.blit(image, [0, 0])
                pygame.display.flip()
            if not add:
                self.screen.fill(pygame.Color('white'))
            while start:
                self.draw_lines()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        start = False
                        game = False
                        title = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_s:
                            start = False
                            running = True
                self.draw_by_mouse(event)
                pygame.display.flip()

            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        game = False
                        title = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_SPACE:
                            self.PAUSED = not self.PAUSED
                            if self.PAUSED:
                                pygame.display.set_caption(caption+'(Paused)')
                            else:
                                pygame.display.set_caption(caption)
                        if event.key == K_a:
                            running = False
                            start = True
                            add = True
                        if event.key == K_r:
                            running = False
                            start = True
                            for i in range(len(self.cells)):
                                for j in range(len(self.cells)):
                                    self.cells[i][j].set_dead()
                if not self.PAUSED:
                    self.draw_grid()
                    self.update_board()
                pygame.display.flip()
                clock.tick(self.speed)

        pygame.quit()


if __name__ == '__main__':
    game = Board(randomed=False)
    game.run()
