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


def run(filename, target_row):
    sensors, beacons = [], []
    for line in get_lines(filename):
        coords = [int(e) for e in re.findall(r'(-?\d+)', line)]
        sensors.append((coords[1], coords[0]))  # reverse for row,col instead of x,y
        beacons.append((coords[3], coords[2]))

    distances = {sensors[i]: manhatan_distance(sensors[i], beacons[i]) for i in range(len(sensors))}

    leftmost_reaching_sensor = min(sensors, key=lambda e: e[1] - distances[e])
    rightmost_reaching_sensor = max(sensors, key=lambda e: e[1] + distances[e])
    col_start = leftmost_reaching_sensor[1] - distances[leftmost_reaching_sensor] - 1
    col_end = rightmost_reaching_sensor[1] + distances[rightmost_reaching_sensor] + 2

    total_impossibles = 0
    for j in tqdm(range(col_start, col_end)):
        for sensor in sensors:
            if (target_row, j) not in beacons and manhatan_distance((target_row, j), sensor) <= distances[sensor]:
                total_impossibles += 1
                break

    print(total_impossibles)


if __name__ == '__main__':
    # run('example.txt', 10)
    run('input.txt', 2_000_000)
