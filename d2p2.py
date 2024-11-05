def evaluate(enemy_move, player_move):
    enemy_map = {'A': 'R', 'B': 'P', 'C': 'S'}
    move_values = {'R': 1, 'P': 2, 'S': 3}
    beats = {'R': 'S', 'P': 'R', 'S': 'P'}
    loses = {beats[k]: k for k in beats}

    enemy_move = enemy_map[enemy_move]

    if player_move == 'X':
        return 0 + move_values[beats[enemy_move]]
    if player_move == 'Y':
        return 3 + move_values[enemy_move]
    return 6 + move_values[loses[enemy_move]]


def run(filename):
    with open(filename) as file:
        lines = file.readlines()

    total = 0
    for line in lines:
        enemy_move, player_move = line.rstrip().split(' ')
        total += evaluate(enemy_move, player_move)
    print(total)


if __name__ == '__main__':
    run('example.txt')
    run('input.txt')
