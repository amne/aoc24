import time
directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

def load_file(filename):
    boxmap = []
    robot_moves = []
    tr = {'#' : '##', '.': '..', '@': '@.', 'O' : '[]'}
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            boxmap.append(list("".join([tr[c] for c in line.strip()])))
        for line in f:
            robot_moves.extend(line.strip())

    return boxmap, robot_moves

def find_robot(boxmap):
    for l in range(len(boxmap)):
        for c in range(len(boxmap[0])):
            if boxmap[l][c] == '@':
                return l, c

def first_empty_space(boxmap, pos, direction):
    l, c = pos
    while 0 < l < len(boxmap)-1 and 0 < c < len(boxmap[0])-1:
        l += direction[0]
        c += direction[1]
        if boxmap[l][c] == '#':
            return pos
        if boxmap[l][c] == '.':
            return l, c
    return pos



def move_robot_left_right(boxmap, pos, direction):
    robot = first_empty_space(boxmap, pos, direction)
    if robot != pos:
        while robot != pos:
            boxmap[robot[0]][robot[1]] = boxmap[robot[0]-direction[0]][robot[1]-direction[1]]
            robot = (robot[0]-direction[0], robot[1]-direction[1])
            # map[empty_space[0]][empty_space[1]] = map[empty_space[0]-direction[0]][empty_space[1]-direction[1]]
            # map[pos[0]+direction[0]][pos[1]+direction[1]] = '@'
        boxmap[pos[0]][pos[1]] = '.'
        pos = (pos[0]+direction[0], pos[1]+direction[1])
    return boxmap, pos



def move_robot_up_down(boxmap, pos, direction):
    robot = pos
    slice_list = [[(pos[1], pos[1])]]
    while 0 < robot[0] < len(boxmap)-1:
        slices = slice_list[-1]
        robot = (robot[0] + direction[0], robot[1] + direction[1])
        view = ""
        for slice in slices:
            view += "".join([boxmap[robot[0]][p] for p in range(slice[0], slice[1]+1)])
        # print(pos, view)
        # view = "".join([boxmap[robot[0]][slice[0]:slice[1]+1] for slice in slices) 
        if '#' in view:
            return boxmap, pos
        if set(view) == {'.'}:
            # need to move all previous slices up or down
            # sometimes two boxes push the same, one with left edge and the other with the right edge
            # so with this algo we could move some cells twice but the second time they would be empty space
            # and lose the shared box in the process
            # so we keep track of what cells we already moved
            moved_positions = set()
            for move_slices in slice_list[::-1]:
                # print("preparing to move ", move_slices)
                for slice in move_slices:
                    # print("moving ", list(range(slice[0], slice[1]+1)))
                    for s in range(slice[0], slice[1]+1):
                        # print("moving character ", boxmap[robot[0]-direction[0]][s], " from ",(robot[0]-direction[0],s)," to ", (robot[0],s), "over", boxmap[robot[0]][s])
                        if (robot[0],s) not in moved_positions:
                            moved_positions.add((robot[0],s))
                            boxmap[robot[0]][s] = boxmap[robot[0]-direction[0]][s]
                            boxmap[robot[0]-direction[0]][s] = '.'
                robot = (robot[0]-direction[0], robot[1]-direction[1])
            robot = (pos[0]+direction[0], pos[1]+direction[1])
            boxmap[robot[0]][robot[1]] = '@'
            boxmap[pos[0]][pos[1]] = '.'
            pos = robot
            return boxmap, pos
        # and now the fun: look if we are on top of a box
        # and see how many boxes we are overlapping
        new_slices = []
        for slice in slices:
            p  = slice[0]
            while p < slice[1]+1:
            # for p in range(slice[0], slice[1]+1):
                if boxmap[robot[0]][p] == ']':
                    new_slices.append((p-1,p))
                if boxmap[robot[0]][p] == '[':
                    new_slices.append((p,p+1))
                    p += 1
                p += 1
        slice_list.append(new_slices)

    return boxmap, pos

# ESC = '\u001B['
#
# def cursorTo(x, y=None):
#     if y is None:
#         return ESC + str(int(x + 1)) + 'G'
#
#     return ESC + str(int(y + 1)) + ';' + str(int(x + 1)) + 'H'

def solve_moves(boxmap, robot_moves):
    [print("".join(l)) for l in boxmap]
    # print("".join(robot_moves))
    # print(len(robot_moves))
    pos = find_robot(boxmap)
    # print(pos)
    # print("\033c", end="")
    for i,m in enumerate(robot_moves):
        # time.sleep(0.5)
        # print('\u001B[1;1H', end="")
        # print("====",i, m, directions[m], pos)
        if (m == '^' or m == 'v'):
            boxmap, pos = move_robot_up_down(boxmap, pos, directions[m])
        else:
            boxmap, pos = move_robot_left_right(boxmap, pos, directions[m])
        # [print("".join(l)) for l in boxmap]
    [print("".join(l)) for l in boxmap]
    pos = find_robot(boxmap)
    print(pos)
    gps_score = 0
    for l in range(len(boxmap)): 
        for c in range(len(boxmap[0])): 
            if boxmap[l][c] == '[':
                gps_score += l*100 + c
    print(gps_score)
        

if __name__ == '__main__':
    # boxmap, robot_moves = load_file('day15_boxes_sample.txt')
    # boxmap, robot_moves = load_file('day15_boxes_sample_p2.txt')
    # boxmap, robot_moves = load_file('day15_boxes_sample_alt_p2.txt')
    # boxmap, robot_moves = load_file('day15_boxes_sample_large.txt')
    boxmap, robot_moves = load_file('day15_boxes.txt')
    solve_moves(boxmap, robot_moves)
