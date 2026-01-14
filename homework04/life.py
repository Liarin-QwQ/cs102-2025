import pathlib
import random
import typing as tp

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
        grid: Grid = []
        for _ in range(self.rows):
            row: Cells = []
            for _ in range(self.cols):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours: Cells = []
        y, x = cell

        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue

                ny = y + dy
                nx = x + dx

                if 0 <= ny < self.rows and 0 <= nx < self.cols:
                    neighbours.append(self.curr_generation[ny][nx])

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid: Grid = []

        for y in range(self.rows):
            new_row: Cells = []
            for x in range(self.cols):
                alive_neighbours = sum(self.get_neighbours((y, x)))

                if self.curr_generation[y][x] == 1:
                    if alive_neighbours in (2, 3):
                        new_row.append(1)
                    else:
                        new_row.append(0)
                else:
                    if alive_neighbours == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)

            new_grid.append(new_row)

        return new_grid

    def step(self) -> None:
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        rows = len(lines)
        cols = len(lines[0])

        life = GameOfLife((rows, cols), randomize=False)

        grid: Grid = []
        for line in lines:
            row: Cells = [int(ch) for ch in line]
            grid.append(row)

        life.curr_generation = grid
        life.prev_generation = life.create_grid()

        return life

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as file:
            for row in self.curr_generation:
                file.write("".join(str(cell) for cell in row) + "\n")
