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

    stream = lines[0]
    wlen = 14

    for w_start in range(len(stream) - wlen):
        cur_part = stream[w_start:w_start + wlen]
        if len(set(cur_part)) == wlen:
            print(w_start + wlen)
            break


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
