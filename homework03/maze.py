from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    directions = []

    if x - 2 > 0:
        directions.append((-2, 0))
    if y + 2 < cols - 1:
        directions.append((0, 2))
    if not directions:
        return grid

    dx, dy = choice(directions)

    grid[x + dx // 2][y + dy // 2] = " "
    grid[x + dx][y + dy] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    empty_cells = []

    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        if y == cols - 2:
            grid[x - 1][y] = " "
        elif x == 1:
            grid[x][y + 1] = " "
        else:
            if choice([True, False]):
                grid[x][y + 1] = " "
            else:
                grid[x - 1][y] = " "

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, 1
        x_out, y_out = rows - 2, cols - 1

    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits = []

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    rows = len(grid)
    cols = len(grid[0])

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if grid[nx][ny] == " " or grid[nx][ny] == 0:
                            grid[nx][ny] = k + 1
    return grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    x, y = exit_coord
    if not isinstance(grid[x][y], int) or grid[x][y] == 0:
        return None

    k = grid[x][y]
    assert isinstance(k, int)

    path = [(x, y)]

    while k > 1:
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if isinstance(grid[nx][ny], int) and grid[nx][ny] == k - 1:
                    path.append((nx, ny))
                    x, y = nx, ny
                    k -= 1
                    found = True
                    break
        if not found:
            return None

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])
    walls = 0

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= rows or ny < 0 or ny >= cols:
            walls += 1
        elif grid[nx][ny] == "■":
            walls += 1

    if (x == 0 or x == rows - 1) and (y == 0 or y == cols - 1):
        return walls >= 2
    if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
        return walls >= 3

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[List[Tuple[int, int]]]]:
    exits = get_exits(grid)

    if len(exits) != 2:
        return grid, None

    start, end = exits[0], exits[1]

    if encircled_exit(grid, start) or encircled_exit(grid, end):
        return grid, None

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                grid[x][y] = 0

    grid[start[0]][start[1]] = 1

    k = 1
    while grid[end[0]][end[1]] == 0:
        prev = deepcopy(grid)
        k += 1
        grid = make_step(grid, k - 1)

        if grid == prev:
            return grid, None

    path = shortest_path(grid, end)

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[List[Tuple[int, int]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "main":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
