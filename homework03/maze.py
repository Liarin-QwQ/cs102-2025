from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    """
    Создаёт сетку лабиринта
    """
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    Удаляет стену
    """
    x, y = coord
    cols = len(grid[0])
    direction = choice(("up", "right"))

    if direction == "up":
        if x > 1:
            grid[x - 1][y] = " "
        elif y < cols - 2:
            grid[x][y + 1] = " "
    else:
        if y < cols - 2:
            grid[x][y + 1] = " "
        elif x > 1:
            grid[x - 1][y] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    Генерирует лабиринт
    """
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    grid = create_grid(rows, cols)
    empty_cells = []

    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    for cell in empty_cells:
        remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in {0, rows - 1} else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in {0, rows - 1} else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    Находит выходы
    """
    """
    :param grid:
    :return:
    """

    exits = []

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    Выполняет шаг для поиска пути
    """
    """
    :param grid:
    :param k:
    :return:
    """

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


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    Находит кратчайший путь
    """
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord

    cell = grid[x][y]
    if not isinstance(cell, int) or cell == 0:
        return None

    k = cell
    path: List[Tuple[int, int]] = [(x, y)]

    while k > 1:
        found = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbor = grid[nx][ny]
                if isinstance(neighbor, int) and neighbor == k - 1:
                    path.append((nx, ny))
                    x, y = nx, ny
                    k -= 1
                    found = True
                    break
        if not found:
            return None

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    Проверяет доступностть выхода
    """
    """
    :param grid:
    :param coord:
    :return:
    """
    rows, cols = len(grid), len(grid[0])
    x, y = coord

    if (x == 0 or x == rows - 1) and (y == 0 or y == cols - 1):
        return True

    if x == 0 and grid[x + 1][y] != " ":
        return True

    if x == rows - 1 and grid[x - 1][y] != " ":
        return True

    if y == 0 and grid[x][y + 1] != " ":
        return True

    if y == cols - 1 and grid[x][y - 1] != " ":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    Решает лабиринт
    """
    """
    :param grid:
    :return:
    """
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
    while True:
        end_cell = grid[end[0]][end[1]]

        if isinstance(end_cell, int) and end_cell > 0:
            break

        prev = deepcopy(grid)
        k += 1
        grid = make_step(grid, k - 1)

        if grid == prev:
            return grid, None

    path = shortest_path(grid, end)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    Рисует найденный путь
    """
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
