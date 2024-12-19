from collections import deque
import time

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_char = {(0,1): '>', (1,0): 'v', (0,-1): '<', (-1,0): '^'}

def load_file(filename):
    map = []
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            map.append(list(line.strip()))

    return map

def min_neighbour(distance_map, pos):
    min_neighbour = None
    for d in directions:
        neighbour = distance_map[pos[0]+d[0]][pos[1]+d[1]]
        if neighbour[1] == -1: 
            continue
        if min_neighbour is None or ( neighbour[2] > -1 and neighbour[2] < min_neighbour[1][2]):
            min_neighbour = ((pos[0]+d[0], pos[1]+d[1]), neighbour) 
    return min_neighbour 

def quick_bfs(raw_map, start, end):
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
                        if dir_to_prev != direction: 
                            score += 1000
                    map[new_l][new_c][1] = d

                    map[new_l][new_c][2] = score
                    new_neighbours.append((new_l, new_c))
        if new_neighbours:
            to_visit.append(new_neighbours)

    [print("".join(['{0: >6}'.format(c[2]) for c in l])) for l in map]
    return walk_bfs(map, start), map


def walk_bfs(distance_map, start):
    path = [(start,'S')]
    while True:
        pos = path[-1][0]
        min_distance = distance_map[pos[0]][pos[1]][2]
        min_direction = 0
        for i,d in enumerate(directions):
            if distance_map[pos[0]+d[0]][pos[1]+d[1]][2] == -1:
                continue
            if distance_map[pos[0]+d[0]][pos[1]+d[1]][2] < min_distance:
                min_distance = distance_map[pos[0]+d[0]][pos[1]+d[1]][2]
                min_direction = i
        path.append(((pos[0]+directions[min_direction][0], pos[1]+directions[min_direction][1]), dir_char[directions[min_direction]]))
        if distance_map[path[-1][0][0]][path[-1][0][1]][0] == 'E':
            break
    return path



def score_path(path):
    score = 0
    path[0] = (path[0][0], '>') # face east
    for i in range(1, len(path)):
        score += 1
        if path[i-1][1] != path[i][1]:
            score += 1000
    return score


def print_path(map, path):
    print_map = [[c for c in l] for l in map]
    for p in path:
        print_map[p[0][0]][p[0][1]] = p[1]
    [print("".join(l)) for l in print_map]

def full_bfs(map, best_score, start, end):
    paths = []




def solve_maze(map):
    # [print("".join(l)) for l in map]
    # find "S" and "E"
    for l in range(len(map)):
        for c in range(len(map[0])):
            if map[l][c] == 'E':
                end = (l, c)
            if map[l][c] == 'S':
                start = (l, c)
    [print("".join(l)) for l in map]
    print(start, end)
    path, distance_map = quick_bfs(map, start, end)
    print_path(map, path)
    print(score_path(path))


if __name__ == '__main__':
    # map = load_file('day16_reinmaze_sample.txt')
    # map = load_file('day16_reinmaze_sample2.txt')
    map = load_file('day16_reinmaze_sample3.txt')
    # map = load_file('day16_reinmaze.txt')
    solve_maze(map)
