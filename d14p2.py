def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


import re
from utils import sign

coord_matcher = re.compile(r'(\d+),(\d+)')
SOURCE, ROCK, AIR, SAND = '+', '#', '.', 'o'
blocked = f'{ROCK}{SAND}'
allowed = f'{AIR}'


def drop_sand(grid, sand_row, sand_col):
    m = len(grid)
    i, j = sand_row, sand_col

    while True:
        if i + 1 >= m:
            return i + 1, j  ## out of bounds

        if grid[i + 1][j] in blocked:
            if grid[i + 1][j - 1] in allowed:
                j -= 1
            elif grid[i + 1][j + 1] in allowed:
                j += 1
            else:
                return i, j
        i += 1


def populate_rocks(grid, coords):
    if not coords:
        return

    grid[coords[0][0]][coords[0][1]] = ROCK

    i, n = 1, len(coords)

    while i < n:
        cur, stop = coords[i - 1], coords[i]
        step = (sign(stop[0] - cur[0]), sign(stop[1] - cur[1]))

        while cur != stop:
            cur = (cur[0] + step[0], cur[1] + step[1])
            grid[cur[0]][cur[1]] = ROCK

        i += 1


def run(filename):
    lines = get_lines(filename)

    m, n = 202, 700
    board = [[AIR] * n for _ in range(m)]

    max_row = -1
    for line in lines:
        coords = coord_matcher.findall(line)
        for _, row in coords:
            max_row = max(max_row, int(row))
        coord_line = [(int(row), int(col)) for col, row in coords]
        populate_rocks(board, coord_line)
    board[max_row + 2] = [ROCK] * n

    drops_settled = 0
    sand_source = (0, 500)

    board[sand_source[0]][sand_source[1]] = SOURCE
    while board[sand_source[0]][sand_source[1]] == SOURCE:
        destination = drop_sand(board, *sand_source)

        board[destination[0]][destination[1]] = SAND
        drops_settled += 1

    for line in board:
        print(''.join(line[:]))

    print(drops_settled)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
