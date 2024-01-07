import os
import pathlib

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.cell_size = cell_size
        self.life = life
        self.speed = speed

        # Параметры окна
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

        # Состояние процесса игры и паузы
        self.running = False
        self.paused = False

        # Создание нового окна
        self.screen = pygame.display.set_mode((self.width, self.height))

        super().__init__(life)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
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

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT or self.life.is_max_generations_exceeded:
                self.running = False

            if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                self.paused = not self.paused

            if event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                # Вычисление индекса клетки на основе позиции
                col = position[0] // self.cell_size
                row = position[1] // self.cell_size

                self.life.curr_generation[row][col] = 1 - self.life.curr_generation[row][col]

            if event.type == KEYDOWN and event.key == pygame.K_s:
                path_dir = os.path.dirname(__file__)
                directory = os.path.join(path_dir, "saved")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                self.life.save(pathlib.Path(os.path.join(directory, f"life_gen{self.life.generations}.txt")))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.running = True
        while self.running:
            self.handle_events()

            # Отрисовка списка клеток
            self.draw_grid()

            # Отрисовка сетки
            self.draw_lines()

            # Выполнение одного шага игры (обновление состояния ячеек)
            if not self.paused:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        self.life.curr_generation = self.life.create_grid()
        pygame.quit()


life = GameOfLife((30, 40), False)
gui = GUI(life, 20)
gui.run()
