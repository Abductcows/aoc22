def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


import ast


def my_cmp(e1, e2):
    if isinstance(e1, list) and isinstance(e2, list):
        for i in range(min(len(e1), len(e2))):
            if (res := my_cmp(e1[i], e2[i])) != 0:
                return res
        return (len(e1) > len(e2)) - (len(e1) < len(e2))

    if isinstance(e1, int) and isinstance(e2, int):
        return (e1 > e2) - (e1 < e2)

    if isinstance(e1, int):
        e1 = [e1]
    else:
        e2 = [e2]
    return my_cmp(e1, e2)


def run(filename):
    lines = get_lines(filename)

    total = 0
    i, n = 0, len(lines)
    while i < len(lines):
        l1 = ast.literal_eval(lines[i])
        l2 = ast.literal_eval(lines[i + 1])
        cmp = my_cmp(l1, l2)

        if cmp < 0:
            total += i // 3 + 1

        i += 3

    print(total)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
