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
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.fill(pygame.Color("white"))

            self.draw_grid()
            self.draw_lines()

            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        """
        grid: Grid = []
        for _ in range(self.cell_height):
            row: Cells = []
            for _ in range(self.cell_width):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующие цвета.
        """
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                color = pygame.Color("green") if self.grid[y][x] == 1 else pygame.Color("white")
                rect = (
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки cell.
        """
        neighbours: Cells = []
        y, x = cell

        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue

                ny = y + dy
                nx = x + dx
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        new_grid: Grid = []

        for y in range(self.cell_height):
            new_row: Cells = []
            for x in range(self.cell_width):
                neighbours = self.get_neighbours((y, x))
                alive = sum(neighbours)
                if self.grid[y][x] == 1:
                    if alive == 2 or alive == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)
                else:
                    if alive == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)

            new_grid.append(new_row)

        return new_grid
