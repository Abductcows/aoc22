def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


from collections import deque


def get_elevation(c):
    return ord(c) - ord('a')


def get_neighbors(grid, i, j):
    result = []
    m, n = len(grid), len(grid[0])
    if i > 0 and grid[i - 1][j] <= grid[i][j] + 1:
        result.append((i - 1, j))
    if j > 0 and grid[i][j - 1] <= grid[i][j] + 1:
        result.append((i, j - 1))
    if i < m - 1 and grid[i + 1][j] <= grid[i][j] + 1:
        result.append((i + 1, j))
    if j < n - 1 and grid[i][j + 1] <= grid[i][j] + 1:
        result.append((i, j + 1))
    return result


def run(filename):
    lines = get_lines(filename)

    m, n = len(lines), len(lines[0])
    grid = [[0] * n for _ in range(m)]
    start, end = None, None

    for i in range(m):
        for j in range(n):
            c = lines[i][j]
            if ord(c) >= ord('a'):
                grid[i][j] = get_elevation(c)
            elif c == 'S':
                grid[i][j] = get_elevation('a')
            else:
                end = (i, j)

    grid[end[0]][end[1]] = get_elevation('z')

    start_list = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == get_elevation('a')]

    candidates = []
    for start in start_list:
        seen = {start}
        search = deque([start])
        length = 0
        until_next = 1

        while search:
            next = search.popleft()

            neighbors = [neighbor for neighbor in get_neighbors(grid, *next) if neighbor not in seen]
            if end in neighbors:
                candidates.append((start, length + 1))
                break

            seen.update(neighbors)
            search.extend(neighbors)

            until_next -= 1
            if until_next == 0:
                length += 1
                until_next = len(search)

    print(candidates)
    print(min(candidates, key=lambda e: e[1]))


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
