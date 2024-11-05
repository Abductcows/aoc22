def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


from itertools import groupby


def run(filename):
    lines = get_lines(filename)
    elves = [
        [int(calorie_row) for calorie_row in group if calorie_row.isdigit()]
        for _, group in groupby(lines, key=lambda x: x.isdigit())]

    elves = [sum(calorie_list) for calorie_list in elves if calorie_list]

    print(sum(sorted(elves)[-3::]))


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
