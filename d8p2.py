def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


def clamp(x, a, b):
    return max(a, min(x, b))


def shoot_forward(lines, start_row, start_col, row_step, col_step, do_while_pred):
    m, n = len(lines), len(lines[0])
    i, j = start_row + row_step, start_col + col_step
    while 0 <= i < m and 0 <= j < n:
        e = lines[i][j]
        if not do_while_pred(e):
            break

        i += row_step
        j += col_step

    return i, j


def run(filename):
    lines = get_lines(filename)
    lines = [[int(e) for e in line] for line in lines]

    m, n = len(lines), len(lines[0])

    max_scenic = -1
    i = 1
    while i < m - 1:
        j = 1
        while j < n - 1:
            val = lines[i][j]
            cur_scenic = 1
            for steps in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                end_i, end_j = shoot_forward(lines, i, j, steps[0], steps[1],
                                             do_while_pred=lambda e, base=val: e < base)
                for score in [abs(i - end_i), abs(j - end_j)]:
                    if score == 0:
                        continue
                    if end_i < 0 or end_i >= m or end_j < 0 or end_j >= n:
                        score -= 1
                    cur_scenic = cur_scenic * score if score > 0 else cur_scenic

            max_scenic = max(max_scenic, cur_scenic)
            j += 1
        i += 1

    print(max_scenic)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
