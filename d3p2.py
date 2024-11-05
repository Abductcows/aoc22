import string

priorities = {c: ord(c) - ord('a') + 1 if ord(c) >= ord('a') else ord(c) - ord('A') + 27 for c in string.ascii_letters}


def run(filename):
    with open(filename) as file:
        lines = file.readlines()

    total = 0

    i = 0
    common = set()
    for line in lines:
        if i % 3 == 0:
            common = set(line.rstrip())
        else:
            common &= set(line.rstrip())

        i += 1
        if i % 3 == 0:
            for c in common:
                total += priorities[c]

    print(total)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
