from collections import deque

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_char = {(0,1): '>', (1,0): 'v', (0,-1): '<', (-1,0): '^'}


def load_memory_file(filename):
    byte_pos = []
    with open(filename, 'r') as file:
        for line in file:
            bc,bl = map(int, line.strip().split(','))
            byte_pos.append((bc,bl))
    return byte_pos

def drop_bytes(byte_pos, memory_size = 71):
    memory = [['.' for _ in range(memory_size)] for _ in range(memory_size)]
    print(byte_pos)
    # [print("".join(row)) for row in memory]
    for b in byte_pos[:1024]:
        bc, bl = b
        memory[bl][bc] = '#'
    [print("".join(row)) for row in memory]
    memory[0][0] = 'S'
    memory[-1][-1] = 'E'
    exit_path, distance_map = quick_bfs(memory, (0,0), (70,70))
    print(len(exit_path), exit_path)
    print_path(memory, exit_path)


def find_killer_byte(byte_pos, memory_size = 71):
    memory = [['.' for _ in range(memory_size)] for _ in range(memory_size)]
    print(byte_pos)
    # [print("".join(row)) for row in memory]
    for b in byte_pos:
        bc, bl = b
        memory[bl][bc] = '#'
        # [print("".join(row)) for row in memory]
        memory[0][0] = 'S'
        memory[-1][-1] = 'E'
        exit_path, distance_map = quick_bfs(memory, (0,0), (70,70))
        if len(exit_path) == 0:
            print("Found killer byte", b)
            return
        # print(len(exit_path), exit_path)
        # print('\u001B[1;1H', end="")
        print("=====")
        print_path(memory, exit_path)



def print_path(map, path):
    print_map = [[c for c in l] for l in map]
    for p in path:
        print_map[p[0][0]][p[0][1]] = p[1]
    [print("".join(l)) for l in print_map]


def min_neighbour(distance_map, pos):
    min_neighbour = None
    for d in directions:
        if pos[0]+d[0] < 0 or pos[1]+d[1] < 0 or pos[0]+d[0] >= len(distance_map) or pos[1]+d[1] >= len(distance_map[0]):
            continue
        neighbour = distance_map[pos[0]+d[0]][pos[1]+d[1]]
        if neighbour[1] == -1: 
            continue
        if min_neighbour is None or ( neighbour[2] > -1 and neighbour[2] < min_neighbour[1][2]):
            min_neighbour = ((pos[0]+d[0], pos[1]+d[1]), neighbour) 
    return min_neighbour 

def quick_bfs(raw_map, start, end, start_dir = '>'):
    map = [[[c, -1, -1] for c in l] for l in raw_map]
    d = 0
    to_visit = deque([[end]])
    map[end[0]][end[1]][1] = d
    map[end[0]][end[1]][2] = 0
    while to_visit:
        d += 1
        neighbours = to_visit.popleft()
        new_neighbours = []
        for neighbour in neighbours:
            l, c = neighbour
            for direction in directions:
                new_l = l + direction[0]
                new_c = c + direction[1]
                score = map[neighbour[0]][neighbour[1]][2] + 1
                if 0 <= new_l < len(map) and 0 <= new_c < len(map[0]) and map[new_l][new_c][0] != '#' and (map[new_l][new_c][2] == -1 or score < map[new_l][new_c][2]):
                    if d > 1:
                        prev_neighbour = min_neighbour(map, neighbour)
                        dir_to_prev = (neighbour[0]-prev_neighbour[0][0], neighbour[1]-prev_neighbour[0][1])
                        # if dir_to_prev != direction: 
                        #     score += 1000
                    map[new_l][new_c][1] = d

                    map[new_l][new_c][2] = score
                    new_neighbours.append((new_l, new_c))
        if new_neighbours:
            to_visit.append(new_neighbours)

    # [print("".join(['{0: >6}'.format(c[1]) for c in l])) for l in map]
    return walk_bfs(map, start, start_dir), map


def walk_bfs(distance_map, start, start_dir = '>'):
    path = [(start,start_dir)]
    while True:
        pos = path[-1][0]
        if distance_map[pos[0]][pos[1]][1] == -1:
            return []
        min_distance = distance_map[pos[0]][pos[1]][1]
        min_direction = -1
        for i,d in enumerate(directions):
            if pos[0]+d[0] < 0 or pos[1]+d[1] < 0 or pos[0]+d[0] >= len(distance_map) or pos[1]+d[1] >= len(distance_map[0]):
                continue
            if distance_map[pos[0]+d[0]][pos[1]+d[1]][1] == -1:
                continue
            if distance_map[pos[0]+d[0]][pos[1]+d[1]][1] < min_distance:
                min_distance = distance_map[pos[0]+d[0]][pos[1]+d[1]][1]
                min_direction = i
        if min_direction == -1:
            break
        path.append(((pos[0]+directions[min_direction][0], pos[1]+directions[min_direction][1]), dir_char[directions[min_direction]]))
        if distance_map[path[-1][0][0]][path[-1][0][1]][0] == 'E':
            break
    return path





if __name__ == "__main__":
    byte_pos = load_memory_file("day18_memory.txt")
    # byte_pos = load_memory_file("day18_memory_sample.txt")
    drop_bytes(byte_pos)
    find_killer_byte(byte_pos)
