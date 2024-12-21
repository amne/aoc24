from itertools import permutations
from functools import cache

def load_keycodes(filename):
    keycodes = []
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            keycodes.append(line.strip())

    return keycodes

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_char = {(0,1): '>', (1,0): 'v', (0,-1): '<', (-1,0): '^'}
char_dir = {'>': (0,1), 'v': (1,0), '<': (0,-1), '^': (-1,0)}

number_pad = {
    '7': (0,0), '8': (0,1), '9': (0,2),
    '4': (1,0), '5': (1,1), '6': (1,2),
    '1': (2,0), '2': (2,1), '3': (2,2),
                '0': (3,1), 'A': (3,2)
}
arrow_pad = {
                '^': (0,1), 'A': (0,2),
    'v': (1,1), '<': (1,0), '>': (1,2)
}

def print_number_pad():
    numpad = [['.' for _ in range(3)] for _ in range(4)]
    for n, pos in number_pad.items():
        numpad[pos[0]][pos[1]] = n
    [print("".join(l)) for l in numpad]

def print_arrow_pad():
    dpad = [['.' for _ in range(3)] for _ in range(2)]
    for n, pos in arrow_pad.items():
        dpad[pos[0]][pos[1]] = n
    [print("".join(l)) for l in dpad]

def left_right(a,b):
    if a < b:
        return '>' * (b - a)
    else:
        return '<' * (a - b)
def up_down(a,b):
    if a < b:
        return 'v' * (b - a)
    else:
        return '^' * (a - b)


def move_robot_numpad(code_from, code_to, n = 2):
    pos_from = number_pad[code_from]
    pos_to = number_pad[code_to]
    moves = ''
    if pos_from[1] == 0 and pos_to[0] == 3:
        moves += left_right(pos_from[1], pos_to[1])
        moves += up_down(pos_from[0], pos_to[0])
    elif pos_from[0] == 3 and pos_to[1] == 0:
        moves += up_down(pos_from[0], pos_to[0])
        moves += left_right(pos_from[1], pos_to[1])
    elif pos_from[0] < pos_to[0] and pos_from[1] < pos_to[1]:
        moves += up_down(pos_from[0], pos_to[0]) + left_right(pos_from[1], pos_to[1])
    else:
        moves += left_right(pos_from[1], pos_to[1]) + up_down(pos_from[0], pos_to[0])

        # move_1 = left_right(pos_from[1], pos_to[1]) + up_down(pos_from[0], pos_to[0])
        # move_2 = up_down(pos_from[0], pos_to[0]) + left_right(pos_from[1], pos_to[1])
        # moves_1 = type_code_arrowpad('A'.join(type_code_arrowpad(move_1+'A'))+'A')
        # moves_2 = type_code_arrowpad('A'.join(type_code_arrowpad(move_2+'A'))+'A')
        #
        # # if type_code_arrowpad('A'.join(type_code_arrowpad(move_2+'A'))+'A') < type_code_arrowpad('A'.join(type_code_arrowpad(move_1+'A'))+'A'):
        # #     moves += move_2
        # #     print("ohohoh")
        # # else:
        # #     moves += move_1
        # if len(seq_to_string(type_code_arrowpad_n(move_2, n-1))) < len(seq_to_string(type_code_arrowpad_n(move_1, n-1))):
        #     print('oh oh oh', pos_from, pos_to)
        #     moves += move_2
        # else:
        #     moves += move_1
    return moves

def move_robot_arrowpad(d_from, d_to, n = 2):
    pos_from = arrow_pad[d_from]
    pos_to = arrow_pad[d_to]
    moves = ''
    if pos_from[1] == 0 and pos_to[0] == 0:
        moves += up_down(pos_from[0], pos_to[0])
        moves += left_right(pos_from[1], pos_to[1])
    elif pos_from[1] == 0 and pos_to[0] == 0:
        moves += left_right(pos_from[1], pos_to[1])
        moves += up_down(pos_from[0], pos_to[0])
    elif pos_from[0] < pos_to[0] and pos_from[1] < pos_to[1]:
        moves += up_down(pos_from[0], pos_to[0]) + left_right(pos_from[1], pos_to[1])
    else:
        moves += left_right(pos_from[1], pos_to[1]) + up_down(pos_from[0], pos_to[0])
    return moves


def type_code_numpad(keycode, n = 2):
    pos = 'A' 
    code_moves = []
    for k in keycode:
        code_moves.append(move_robot_numpad(pos, k, n))
        pos = k
    return code_moves

@cache
def type_code_arrowpad(move_sequence, n = 2):
    pos = 'A' 
    arrow_moves = []
    for k in move_sequence:
        arrow_moves.append(move_robot_arrowpad(pos, k))
        pos = k
    return arrow_moves

@cache
def type_code_arrowpad_n(move_sequence, n=2):
    if n == 0:
        return type_code_arrowpad(move_sequence)
    return type_code_arrowpad(seq_to_string(type_code_arrowpad_n(move_sequence, n-1)))

def seq_to_string(seq):
    return ''.join(seq)

def print_keycodes(keycodes):
    # [print("".join(l)) for l in keycodes]
    print_number_pad()
    print()
    print_arrow_pad()
    sum_codes = 0
    for keycode in keycodes:
        number_code = int(''.join([c for c in keycode if c in '1234567890']).lstrip('0'))
        keypad_moves = type_code_numpad(keycode, 2)
        arrow_moves_A = type_code_arrowpad('A'.join(keypad_moves) + 'A')
        moves = type_code_arrowpad('A'.join(arrow_moves_A) + 'A')
        print('===== ', str(number_code), keycode, len('A'.join(moves) + 'A'))
        print('keypad:     ', 'A '.join(keypad_moves)+'A')
        print('arrow A:    ', 'A '.join(arrow_moves_A) + 'A')
        print('arrow B:    ', 'A '.join(moves) + 'A')
        sum_codes += len('A'.join(moves) + 'A') * number_code
        # rec_moves = type_code_arrowpad_n(seq_to_string(keypad_moves), 1)
        # print('n robots:   ', 'A '.join(rec_moves)+'A')
    print(sum_codes)

    a = type_code_numpad('129A')
    print(a) 
    m = type_code_arrowpad_n(a[0] + 'A', 1)
    print(m)
    

if __name__ == "__main__":
    # keycodes = load_keycodes('day21_keypad_sample.txt')
    keycodes = load_keycodes('day21_keypad.txt')
    print_keycodes(keycodes)
