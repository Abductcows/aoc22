from collections import defaultdict
from functools import partial

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


def get_non_diagonal_neighbors(x, y, z):
    neighbors = [(x + dx, y + dy, z + dz)
                 for dx in (-1, 0, 1)
                 for dy in (-1, 0, 1)
                 for dz in (-1, 0, 1)
                 if abs(dx) + abs(dy) + abs(dz) == 1]

    return neighbors


def run(filename):
    lines = get_lines(filename)
    points = [tuple(int(e) for e in line.split(',')) for line in lines]

    total = run_deez(points)

    print('final answer:', total)


def run_deez(points):
    # print('Running for ')
    # print(points)
    xbeams, ybeams, zbeams = [defaultdict(lambda sort_index=i: SortedList(key=lambda e: e[sort_index]))
                              for i in range(3)]
    lavaset = set()
    for point in points:
        xbeams[get_point_beam(point, X)].add(point)
        ybeams[get_point_beam(point, Y)].add(point)
        zbeams[get_point_beam(point, Z)].add(point)
        lavaset.add(point)
    total = 0
    point_to_space_group = dict()
    space_groups = []
    for beams, get_index in (xbeams, X), (ybeams, Y), (zbeams, Z):
        print(sorted(beams.values(), key=lambda e: e[0]))
        for beam in beams.values():
            total += 2

            for i in range(len(beam) - 1):
                if beam[i][get_index] + 1 == beam[i + 1][get_index]:
                    continue

                total += 2

                # for val in range(beam[i][get_index] + 1, beam[i + 1][get_index]):
                for val in {beam[i][get_index] + 1, beam[i + 1][get_index] - 1}:
                    new_point = beam[i][:get_index] + tuple([val]) + beam[i][get_index + 1:]
                    if new_point in point_to_space_group:
                        continue

                    neighbors = get_non_diagonal_neighbors(*new_point)

                    if all((neighbor not in point_to_space_group for neighbor in neighbors)):
                        new_group = set()
                        for point in [new_point]:
                            if point not in lavaset:
                                new_group.add(point)
                                point_to_space_group[point] = new_group
                        space_groups.append(new_group)
                    else:
                        involved_neighbor = next(
                            (neighbor for neighbor in neighbors if neighbor in point_to_space_group)
                        )
                        space_group = point_to_space_group[involved_neighbor]
                        space_group.add(new_point)
                        point_to_space_group[new_point] = space_group

    for group in space_groups:
        subtract = True
        for point in group:
            for neighbor in get_non_diagonal_neighbors(*point):
                # if neighbor not in group and neighbor not in lavaset:
                if neighbor not in lavaset:
                    subtract = False
        if subtract:
            val = run_deez(group)
            print(f'Subtracted {val} because of {group}')
            total -= val

    return total


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
