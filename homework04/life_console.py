import abc
import curses
import time

from life import GameOfLife
from ui import UI


class UI(abc.ABC):
    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        pass


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        max_y, max_x = screen.getmaxyx()
        for y, row in enumerate(self.life.curr_generation):
            if y + 1 >= max_y:
                break
            for x, cell in enumerate(row):
                if x + 1 >= max_x:
                    break
                try:
                    screen.addch(y + 1, x + 1, "O" if cell else " ")
                except curses.error:
                    pass

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.timeout(0)
        running = True
        try:
            while running:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()
                time.sleep(0.1)

                # Обновление поколения
                if self.life.is_changing and not self.life.is_max_generations_exceeded:
                    self.life.step()
                else:
                    running = False
        finally:
            curses.endwin()


life = GameOfLife((24, 80), max_generations=100)
ui = Console(life)
ui.run()
