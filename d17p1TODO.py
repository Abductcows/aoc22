def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


push_dirs = {'<': (0, -1), '>': (0, 1)}  # row, col
falling_pattern_strings = ['####', '.#.\n###\n.#.', '..#\n..#\n###', '#\n#\n#\n#', '##\n##']
board_width = 7


def generate_patterns():
    patterns = []
    for pattern_string in falling_pattern_strings:
        lines = pattern_string.replace('#', '@').split('\n')

        width_diff = board_width - len(lines[0])
        pad_left, pad_right = width_diff // 2 + width_diff % 2, width_diff // 2

        lines = ['.' * pad_left + line + '.' * pad_right for line in lines]
        pattern = [list(line) for line in lines]

        patterns.append(pattern)
    return patterns


def debug_s(stack, limit=15):
    return '\n'.join((''.join(line) for line in stack[limit:]))


def append_pattern(stack, pattern):
    stack.extend(pattern[::-1])


def stack_replace(stack, old, new, limit):
    for line in stack[-limit:]:
        for j in range(len(line)):
            if line[j] == old:
                line[j] = new


def stack_write_pattern(stack, pattern, start):
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            c = pattern[i][j]
            stack[-i - 1][j] = c


from functools import reduce
from copy import deepcopy


def get_charcount(lines, to_look_for='#@.'):
    return reduce(lambda acc, next: {k: acc[k] + next[k] if k in next else acc[k] for k in acc},
                  [{c: line.count(c) for c in to_look_for} for line in lines],
                  {c: 0 for c in to_look_for})


import json


def tick(stack, pattern_index, direction):
    # Horizontal movement
    pattern_lines = [line for line in reversed(stack[-pattern_index - 4:]) if '@' in line]
    assert pattern_lines

    sim_shift = deepcopy(pattern_lines)
    shift_falling_rocks(sim_shift, direction)

    original_char_count, new_char_count = get_charcount(pattern_lines), get_charcount(sim_shift)

    if new_char_count['@'] == original_char_count['@'] and new_char_count['#'] == original_char_count['#']:
        pattern_lines = sim_shift
        stack_replace(stack[:len(stack) - pattern_index], '@', '.', len(pattern_lines))
        stack_write_pattern(stack, pattern_lines, pattern_index + 1)

    moved_down = False
    next_line = stack[-pattern_index - len(pattern_lines)]

    assert pattern_lines
    simulated_merge = None
    if next_line:
        char_count_before_merge = get_charcount(next_line)
        simulated_merge = [next_line[j] if pattern_lines[-1][j] == '.' else pattern_lines[-1][j] for j in
                           range(len(pattern_lines[0]))]
        char_count_after_merge = get_charcount(simulated_merge)

        if char_count_after_merge['#'] == char_count_before_merge['#']:
            moved_down = True

    if not moved_down:
        stack[len(stack) + 1 - pattern_index - len(pattern_lines): len(stack) + 1 - pattern_index] = pattern_lines[::-1]
        stack_replace(stack, '@', '#', len(pattern_lines) + 4)
    else:
        pattern_index += 1
        pattern_lines = pattern_lines[:len(pattern_lines) - 1] + [simulated_merge]
        stack[len(stack) - pattern_index - len(pattern_lines): len(stack) - pattern_index] = pattern_lines[::-1]
        stack.pop()

    return moved_down


def shift_falling_rocks(pattern_lines, direction):
    n = len(pattern_lines[0])
    for line in pattern_lines:
        for j in range(1, n):
            c = line[j] if direction == '<' else line[n - j - 1]
            if c != '@':
                continue
            if direction == '<':
                line[j - 1] = c
                line[j] = '.'
            elif direction == '>':
                line[n - j] = c
                line[n - j - 1] = '.'


def run(filename):
    lines = get_lines(filename)

    patterns = generate_patterns()
    directions = lines[0]

    stack = [['#'] * board_width]  # Stack

    pattern_i, direction_i = 0, 0

    for _ in range(25):
        stack.extend(['.'] * board_width for _ in range(3))
        append_pattern(stack, patterns[pattern_i])
        pattern_i = (pattern_i + 1) % len(patterns)

        start_index = 0
        while tick(stack, start_index, directions[direction_i]):
            start_index += 1
            direction_i = (direction_i + 1) % len(directions)

    print(debug_s(stack))
    print(len(stack))


if __name__ == '__main__':
    run('example.txt')
    # run('input.txt')
