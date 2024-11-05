def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


def run(filename):
    lines = get_lines(filename)


if __name__ == '__main__':
    run('example.txt')
    # run('input.txt')
