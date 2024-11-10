def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


import re
from tqdm import tqdm


def manhatan_distance(c1, c2):
    return abs(c2[0] - c1[0]) + abs(c2[1] - c1[1])


def run(filename, search_bounds):
    sensors, beacons = [], []
    for line in get_lines(filename):
        coords = [int(e) for e in re.findall(r'(-?\d+)', line)]
        sensors.append((coords[1], coords[0]))  # reverse for row,col instead of x,y
        beacons.append((coords[3], coords[2]))

    distances = {sensors[i]: manhatan_distance(sensors[i], beacons[i]) for i in range(len(sensors))}

    for i in tqdm(range(search_bounds[0], search_bounds[1] + 1), miniters=700):

        j, limit = search_bounds[0], search_bounds[1]
        while j <= limit:
            slist = (sensor for sensor in sensors if manhatan_distance(sensor, (i, j)) <= distances[sensor])
            try:
                sensor = next(slist)
            except StopIteration:
                print(i + 4_000_000 * j)
                exit(0)

            vdiff = abs(sensor[0] - i)
            hjump = distances[sensor] - vdiff
            j = sensor[1] + hjump + 1

    raise Exception('what, why?')


if __name__ == '__main__':
    # run('example.txt', [0, 20])
    run('input.txt', [0, 4_000_000])
