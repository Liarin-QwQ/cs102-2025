import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (x, 0),
                (x, self.height),
            )

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, y),
                (self.width, y),
            )

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                color = pygame.Color("green") if self.life.curr_generation[row][col] == 1 else pygame.Color("white")

                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.cell_size,
                        row * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        paused = False
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused

                if paused and event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // self.cell_size
                    row = y // self.cell_size

                    if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                        self.life.curr_generation[row][col] ^= 1

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()

            if not paused:
                if self.life.is_changing and not self.life.is_max_generations_exceeded:
                    self.life.step()

            clock.tick(self.speed)

        pygame.quit()
