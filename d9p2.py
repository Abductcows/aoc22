def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


def move_once_in_direction(cur_pos, direction):
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    return cur_pos[0] + directions[direction][0], cur_pos[1] + directions[direction][1]


def rope_follow(previous, current):
    def sign(x):
        return (x > 0) - (x < 0)

    hdiff, vdiff = previous[0] - current[0], previous[1] - current[1]
    if abs(hdiff) > 2 or abs(vdiff) > 2:
        raise ValueError('Impossible')

    # diagonal parent, diagonal follow
    if abs(hdiff) == abs(vdiff):
        if abs(hdiff) < 2:
            return current
        return current[0] + sign(hdiff), current[1] + sign(vdiff)

    # straight parent, follow but don't overlap
    if hdiff == 0:
        if abs(vdiff) > 1:
            return current[0], current[1] + sign(vdiff)
        return current
    if vdiff == 0:
        if abs(hdiff) > 1:
            return current[0] + sign(hdiff), current[1]
        return current

    # straight parent, but child is diagonal
    if abs(hdiff) == 1:
        return previous[0], current[1] + sign(vdiff)
    if abs(vdiff) == 1:
        return current[0] + sign(hdiff), previous[1]

    return current


def run(filename):
    lines = get_lines(filename)
    directions = [[line.split(' ')[0], int(line.split(' ')[1])] for line in lines]

    rope_part_count = 10
    part_coords = [(0, 0) for _ in range(rope_part_count)]

    visited = set()

    for direction, steps in directions:
        for _ in range(steps):
            part_coords[0] = move_once_in_direction(part_coords[0], direction)
            for i in range(1, len(part_coords)):
                part_coords[i] = rope_follow(part_coords[i - 1], part_coords[i])

            # rope_map_debug(part_coords, visited, rope_part_count)
            visited.add(part_coords[-1])

    print(len(visited))


# noinspection PyDefaultArgument
def rope_map_debug(coords, visited, rope_part_count):
    """
    cd temp
    watch -n 0.25 cat f0.txt
    """
    import string
    import time

    identifiers = ['H', *string.digits[-9:], *string.ascii_letters][:rope_part_count - 1] + ['T']

    def get_symbol(i, j):
        if (i, j) in coords:
            return identifiers[coords.index((i, j))]
        if (i, j) in visited:
            return '#'
        return '.'

    grid_side_size = 40
    rows = [''.join([get_symbol(i - grid_side_size // 2, j - grid_side_size // 2)
                     for j in range(grid_side_size)])
            for i in range(grid_side_size)]

    time.sleep(0.25)
    with open(f'temp/f0.txt', 'w') as file:
        file.write('\n'.join(rows) + '\n\f\n')
        file.flush()


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
