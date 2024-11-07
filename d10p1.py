def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


from collections import deque


def run(filename):
    lines = get_lines(filename)

    X, cycle = 1, 0
    total = 0

    operations = deque([0])
    while operations:
        if cycle < len(lines):
            operations.append(0)

            if lines[cycle].startswith('addx'):
                operations.append(int(lines[cycle].split(' ')[1]))

        X += operations.popleft()

        cycle += 1
        if cycle == 20 or (cycle - 20) % 40 == 0:
            total += X * cycle

    print(total)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
