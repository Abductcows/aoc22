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

    x, cycle = 1, 0
    image = [['.'] * 40 for _ in range(6)]

    operations = deque()
    while True:
        if cycle < len(lines):
            operations.append(0)
            if lines[cycle].startswith('addx'):
                operations.append(int(lines[cycle].split(' ')[1]))

        crt_row, crt_col = cycle // 40, cycle % 40
        sprite_col = x

        if abs(crt_col - sprite_col) < 2:
            image[crt_row][crt_col] = '#'

        x += operations.popleft()

        if cycle >= len(lines) and not operations:
            break

        cycle += 1

    for line in image:
        print(line)
    print('\n\n')

if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
