def load_file(filename):
    map = []
    robot_moves = []
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            map.append(list(line.strip()))
        for line in f:
            robot_moves.extend(line.strip())

    return map, robot_moves

def find_robot(map):
    for l in range(len(map)):
        for c in range(len(map[0])):
            if map[l][c] == '@':
                return l, c

def first_empty_space(map, pos, direction):
    l, c = pos
    while 0 < l < len(map)-1 and 0 < c < len(map[0])-1:
        l += direction[0]
        c += direction[1]
        if map[l][c] == '#':
            return pos
        if map[l][c] == '.':
            return l, c
    return pos

def move_robot(map, pos, empty_space, direction):
    robot = empty_space
    if robot != pos:
        map[empty_space[0]][empty_space[1]] = map[empty_space[0]-direction[0]][empty_space[1]-direction[1]]
        map[pos[0]+direction[0]][pos[1]+direction[1]] = '@'
        map[pos[0]][pos[1]] = '.'
        pos = (pos[0]+direction[0], pos[1]+direction[1])
    return map, pos

def solve_moves(map, robot_moves):
    # direction dict: ^ - up, v - down, < - left, > - right
    directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    # [print("".join(l)) for l in map]
    # print(robot_moves)
    pos = find_robot(map)
    print(pos)
    for m in robot_moves:
        map, pos = move_robot(map, pos, first_empty_space(map, pos, directions[m]), directions[m])
        # print("====", m, directions[m], pos)
        # [print("".join(l)) for l in map]
    [print("".join(l)) for l in map]
    gps_score = 0
    for l in range(len(map)): 
        for c in range(len(map[0])): 
            if map[l][c] == 'O':
                gps_score += l*100 + c
    print(gps_score)
        

if __name__ == '__main__':
    # map, robot_moves = load_file('day15_boxes_sample.txt')
    # map, robot_moves = load_file('day15_boxes_sample_large.txt')
    map, robot_moves = load_file('day15_boxes.txt')
    solve_moves(map, robot_moves)
