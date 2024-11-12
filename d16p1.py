def get_lines(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    while lines and not lines[-1]:
        lines.pop()

    return lines


import re
from functools import cache
from frozendict import frozendict

valve_map = None
valve_flow = None
memo = None


def backtrack(current_valve, time_remaining, opened_valves, released_pressure):
    if time_remaining <= 0:
        return released_pressure

    state = (current_valve, time_remaining, frozenset(opened_valves), released_pressure)
    if state in memo:
        return memo[state]

    max_pressure = released_pressure

    if current_valve not in opened_valves and valve_flow[current_valve] > 0:
        new_released_pressure = released_pressure + valve_flow[current_valve] * (time_remaining - 1)
        max_pressure = max(max_pressure, backtrack(
            current_valve,
            time_remaining - 1,
            opened_valves | {current_valve},
            new_released_pressure
        ))

    for neighbor in valve_map[current_valve]:
        max_pressure = max(max_pressure, backtrack(
            neighbor,
            time_remaining - 1,
            opened_valves,
            released_pressure
        ))

    memo[state] = max_pressure
    return max_pressure


def run(filename):
    lines = get_lines(filename)

    global valve_map, valve_flow, memo
    valve_map = dict()
    valve_flow = dict()
    memo = {}

    for line in lines:
        names = re.findall(r'[A-Z]{2}', line)
        valve_map[names[0]] = tuple(names[1:])

        flow = next(re.finditer(r'\d+', line)).group()
        valve_flow[names[0]] = int(flow)

    max_pressure_released = backtrack('AA', 30, set(), 0)

    print(max_pressure_released)


if __name__ == '__main__':
    # run('example.txt')
    run('input.txt')
