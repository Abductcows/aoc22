import string

priorities = {c: ord(c) - ord('a') + 1 if ord(c) >= ord('a') else ord(c) - ord('A') + 27 for c in string.ascii_letters}


def run(filename):
    with open(filename) as file:
        lines = file.readlines()

    total = 0

    for line in lines:
        line = line.rstrip()
        s1, s2 = line[:len(line) // 2], line[len(line) // 2:]
        s1, s2 = set(s1), set(s2)
        common = s1 & s2
        for c in common:
            total += priorities[c]

    print(total)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
