from collections import defaultdict

from sortedcontainers import SortedList


def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


X, Y, Z = range(3)


def get_point_beam(point, axis):
    if axis == X:
        return 64 * point[Y] + point[Z]
    if axis == Y:
        return 64 * point[X] + point[Z]
    if axis == Z:
        return 64 * point[X] + point[Y]


def run(filename):
    lines = get_lines(filename)
    xbeams, ybeams, zbeams = [defaultdict(lambda sort_index=i: SortedList(key=lambda e: e[sort_index]))
                              for i in range(3)]

    for line in lines:
        point = tuple(int(e) for e in line.split(','))
        xbeams[get_point_beam(point, X)].add(point)
        ybeams[get_point_beam(point, Y)].add(point)
        zbeams[get_point_beam(point, Z)].add(point)

    total = 0
    for beams, get_index in (xbeams, X), (ybeams, Y), (zbeams, Z):
        for beam in beams.values():
            total += 2

            for i in range(len(beam) - 1):
                if beam[i][get_index] + 1 != beam[i + 1][get_index]:
                    total += 2

    print(total)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
