def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            if line.strip():
                lines.append(line.rstrip('\n'))
    return lines


def ranges_total_overlap(r1, r2):
    return r1[0] >= r2[0] and r1[1] <= r2[1] or r2[0] >= r1[0] and r2[1] <= r1[1]



def run(filename):
    lines = get_lines(filename)

    total = 0

    for line in lines:
        line = line.split(',')
        p1, p2 = line[0].split('-'), line[1].split('-')
        p1, p2 = [int(n) for n in p1], [int(n) for n in p2]

        if ranges_total_overlap(p1, p2):
            total += 1

    print(total)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
