def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

        while lines and not lines[-1]:
            lines = lines[:-1]

        return lines


import re


def parse_move(command):
    pattern = r'move (\d+) from (\d+) to (\d+)'
    match = re.match(pattern, command)
    x, y, z = map(int, match.groups())
    return x, y, z


def run(filename):
    lines = get_lines(filename)

    i = 0
    stacks = [list() for _ in range(32)]

    while not lines[i][1].isdigit():
        line = lines[i]
        letters = line[1::4]
        for j, letter in enumerate(letters):
            if letter.strip():
                stacks[j].insert(0, letter)
        i += 1

    i += 2
    for line in lines[i:]:
        to_move, from_stack, to_stack = parse_move(line)
        from_stack, to_stack = from_stack - 1, to_stack - 1

        for _ in range(to_move):
            stacks[to_stack].append(stacks[from_stack].pop())

    result = ''.join(stack[-1] for stack in stacks if stack)
    print(result)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
