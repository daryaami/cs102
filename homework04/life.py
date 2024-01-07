import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:

        if randomize == False:
            grid: Grid = [[0 for j in range(self.cols)]
                          for i in range(self.rows)]
            return grid

        grid = [[random.randint(0, 1) for _ in range(self.cols)]
                for _ in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell

        neighbours_list = [
            (i, j)
            for i in range(max(0, row - 1), min(self.rows, row + 2))
            for j in range(max(0, col - 1), min(self.cols, col + 2))
            if (i, j) != (row, col)
        ]

        neighbours = [self.curr_generation[n[0]][n[1]]
                      for n in neighbours_list]

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = self.get_neighbours((row, col))
                n_alive = sum(neighbours)
                if self.curr_generation[row][col] == 1 and n_alive in [2, 3]:
                    new_grid[row][col] = 1
                elif self.curr_generation[row][col] == 0 and n_alive == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        new_generation = self.get_next_generation()
        self.curr_generation = copy.deepcopy(new_generation)
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()
        # Исключаем пустые строки и строки только с пробелами или символами новой строки
        state: Grid = [
            [int(char) for char in line.rstrip()]
            for line in lines
            if line.strip()
        ]
        size = (len(state), len(state[0]))
        game = GameOfLife(size)
        game.curr_generation = state
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as file:
            for row in self.curr_generation:
                row_str = ''.join(str(cell) for cell in row)
                file.write(row_str + '\n')
