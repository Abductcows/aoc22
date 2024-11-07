def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


from functools import reduce


def parse_operation(line):
    operator = line[21]
    r_operand = line.split(operator)[1].strip()

    if operator == '+':
        if r_operand == 'old':
            return lambda l: l + l
        elif r_operand.isdigit():
            r_operand = int(r_operand)
            return lambda l, r=r_operand: l + r
    elif operator == '*':
        if r_operand == 'old':
            return lambda l: l * l
        elif r_operand.isdigit():
            r_operand = int(r_operand)
            return lambda l, r=r_operand: l * r

    raise ValueError('Unsupported operation?')


def parse_test(line):
    divisor = int(line.strip().split(' ')[-1])
    return lambda D, d=divisor: D % d == 0


def run(filename):
    lines = get_lines(filename)

    monkey_count = len([line for line in lines if line.startswith('Monkey')])
    possessions = [[] for _ in range(monkey_count)]
    operations = [None] * monkey_count
    tests = [None] * monkey_count
    recipients = [[None, None] for _ in range(monkey_count)]

    monkey_index = -1
    for line in lines:
        if line.startswith('Monkey'):
            monkey_index += 1
            continue

        line = line.lstrip()
        if line.startswith('Starting'):
            possessions[monkey_index].extend((int(item) for item in line.split(':')[1].lstrip().split(', ')))
        elif line.startswith('Operation'):
            operations[monkey_index] = parse_operation(line)
        elif line.startswith('Test'):
            tests[monkey_index] = parse_test(line)
        elif line.startswith('If true'):
            recipients[monkey_index][0] = int(line.strip().split(' ')[-1])
        elif line.startswith('If false'):
            recipients[monkey_index][1] = int(line.strip().split(' ')[-1])

    times_inspected_any_item = [0] * monkey_count
    iterations = 20
    for _ in range(iterations):
        for monkey in range(monkey_count):

            times_inspected_any_item[monkey] += len(possessions[monkey])
            for possession in possessions[monkey]:
                worry_level = operations[monkey](possession) // 3
                next_monkey = recipients[monkey][1 - tests[monkey](worry_level)]
                possessions[next_monkey].append(worry_level)

            possessions[monkey] = []

    print(reduce(lambda p, n: p * n, sorted(times_inspected_any_item)[-2:]))


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
