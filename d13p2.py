def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


import ast
from functools import cmp_to_key, reduce


def parse(packet):
    return ast.literal_eval(packet)


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

    dividers = sorted([parse('[[2]]'), parse('[[6]]')], key=cmp_to_key(my_cmp))
    divider_index_in_sorted = [-1] + [None] * len(dividers)

    all_packets = [parse(line) for line in lines if line]
    for i, divider in enumerate(dividers):
        next_remaining = []
        index_to_previous_divider = 0

        for packet in all_packets:
            if my_cmp(packet, divider) < 0:
                index_to_previous_divider += 1
            else:
                next_remaining.append(packet)

        all_packets = next_remaining
        divider_index_in_sorted[i + 1] = divider_index_in_sorted[i] + index_to_previous_divider + 1

    divider_index_in_sorted = [v + 1 for v in divider_index_in_sorted[1:]]  # 1-indexed

    print(divider_index_in_sorted)
    print(reduce(lambda acc, v: acc * v, divider_index_in_sorted))


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
