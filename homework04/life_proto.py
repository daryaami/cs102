import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Настоящее поколение
        self.grid = self.create_grid(True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            self.draw_grid()

            self.draw_lines()

            # Выполнение одного шага игры (обновление состояния ячеек)
            next_generation = self.get_next_generation()
            self.grid = next_generation

            pygame.display.flip()
            clock.tick(self.speed)
        self.grid = self.create_grid()
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize == False:
            grid: Grid = [[0 for j in range(self.cell_width)] for i in range(self.cell_height)]
            return grid

        grid = [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if self.grid[row][col] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        neighbours_list = [
            (i, j)
            for i in range(max(0, row - 1), min(self.cell_height, row + 2))
            for j in range(max(0, col - 1), min(self.cell_width, col + 2))
            if (i, j) != (row, col)
        ]
        neighbours = [self.grid[n[0]][n[1]] for n in neighbours_list]

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid: Grid = [[0 for j in range(self.cell_width)] for i in range(self.cell_height)]

        for row in range(self.cell_height):
            for col in range(self.cell_width):
                neighbours = self.get_neighbours((row, col))
                n_alive = sum(neighbours)
                if self.grid[row][col] == 1 and n_alive in [2, 3]:
                    new_grid[row][col] = 1
                elif self.grid[row][col] == 0 and n_alive == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0

        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 10)
    game.run()
