def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


########## WHAT THE FUCK IS THIS CURSED PROBLEM (10/2024)
########## This is my response (I am not implementing recursion)

from itertools import islice


def take_while(predicate, lst, start=0):
    result = []
    for x in islice(lst, start, None):
        if not predicate(x):
            break
        result.append(x)
    return result


def run(filename):
    lines = get_lines(filename)

    cds = [i for i, line in enumerate(lines) if line.startswith('$ cd')]
    cd_contents = [''.join(lines[index].split(' ')[2:]) for index in cds]

    # list all dirs
    paths = set('/')
    sizes = {'/': 0}
    cur = ['/']
    for dir in cd_contents[1:]:
        if dir == '..':
            cur.pop()
            continue

        cur.append(dir)
        full_path = cur[0] + '/'.join(cur[1:])
        if full_path not in paths:
            paths.add(full_path)
            sizes[full_path] = 0

    # Calc size of all pure dirs (no child dirs)
    pure_dirs = set()
    cur = []
    for list_index, cd in enumerate(cds):
        if cd_contents[list_index] == '..':
            cur.pop()
            continue
        cur.append(cd_contents[list_index])

        next_line = lines[cd + 1]
        if next_line.startswith('$ cd'):
            continue
        assert next_line.startswith('$ ls')
        payload = take_while(lambda line: not line.startswith('$'), lines, start=cd + 2)

        full_path = cur[0] + '/'.join(cur[1:])
        if all([not line.startswith('dir') for line in payload]):
            pure_dirs.add(full_path)
        sizes[full_path] += sum(
            [int(file_result.split(' ')[0]) for file_result in payload if not file_result.startswith('dir')])


    # print(f'Pure dirs: {sorted(list(pure_dirs))}')
    # print(f'Only pure dirs have true size: {sorted(list(sizes.items()), key=lambda e: e[1])}')

    # And yep do n^2 loop
    sorted_paths = list(sorted(sizes.keys(), reverse=True))
    i, n = 0, len(sorted_paths)

    def ctw(e, start):
        if not my_start.startswith(e):
            return False
        return my_start[len(e):].lstrip('/').count('/') == 0

    while i < n:
        my_start = sorted_paths[i]
        sublist = [e for e in sorted_paths[i + 1:] if ctw(e, my_start)]

        for e in sublist:
            sizes[e] += sizes[my_start]

        i += 1

    # print(f'Final sizes: {sorted(list(sizes.items()), key=lambda e: e[1])}')
    print(sum([v for v in sizes.values() if v <= 100_000]))


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
