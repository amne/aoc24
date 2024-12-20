from collections import deque

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_char = {(0,1): '>', (1,0): 'v', (0,-1): '<', (-1,0): '^'}
char_dir = {'>': (0,1), 'v': (1,0), '<': (0,-1), '^': (-1,0)}

def load_file(filename):
    racetrack = []
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            racetrack.append(list(line.strip()))

    return racetrack

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
    path = [(start,start_dir, 0)]
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
        path.append(((pos[0]+directions[min_direction][0], pos[1]+directions[min_direction][1]), dir_char[directions[min_direction]], len(path)))
        if distance_map[path[-1][0][0]][path[-1][0][1]][0] == 'E':
            break
    return path




def race_track(racetrack):
    for l in range(len(racetrack)):
        for c in range(len(racetrack[0])):
            if racetrack[l][c] == 'E':
                end = (l, c)
            if racetrack[l][c] == 'S':
                start = (l, c)
    raceline, distance_map = quick_bfs(racetrack, start, end)
    print(raceline)
    print_path(racetrack, raceline)
    print(len(raceline))
    possible_cheats = find_cheats(racetrack, raceline, distance_map)
    print(len(possible_cheats))
    # [print(p) for p in possible_cheats]
    # times = set()
    # for cheat in possible_cheats:
    #     times.add(cheat[2])
    # times = list(times)
    # times.sort()
    # print(times)
    # for t in times:
    #     print(t, len([c for c in possible_cheats if c[2] == t]))
        # [print_cheat(racetrack, c) for c in possible_cheats if c[2] == t]
    print(count_long_cheats(racetrack, raceline, distance_map))


def print_cheat(racetrack, cheat):
    for l in range(len(racetrack)):
        for c in range(len(racetrack[0])):
            if (l,c) == cheat[0][0]:
                print('x', end='')
            elif (l,c) == cheat[1][0]:
                print('x', end='')
            else:
                print(racetrack[l][c], end='')
        print()

def find_cheats(racetrack, raceline, distance_map):
    possible_cheats = []
    min_cheat = 100
    for i,(p,p_dir,p_time) in enumerate(raceline):
        for pc, pc_dir, pc_time in raceline[i:]:
            if pc_time - p_time > min_cheat:
                if (((abs(pc[0] - p[0]) == 2 and pc[1] == p[1]) and racetrack[(pc[0]+p[0])//2][p[1]] == '#') or
                    ((abs(pc[1] - p[1]) == 2 and pc[0] == p[0]) and racetrack[p[0]][(pc[1]+p[1])//2] == '#')):
                    possible_cheats.append(((p, p_dir, p_time), (pc, pc_dir, pc_time), pc_time - p_time - 2))
    return possible_cheats



def count_long_cheats(racetrack, raceline, distance_map):
    count = 0
    min_cheat = 100
    possible_cheats = set()
    for i,(p,p_dir,p_time) in enumerate(raceline):
        for pc, pc_dir, pc_time in raceline[i:]:
            m = abs(pc[0] - p[0])
            n = abs(pc[1] - p[1])
            if m+n <= 20:
                if (pc_time - p_time - (m+n)) >= min_cheat:
                    possible_cheats.add((p, pc))
    return len(possible_cheats) 





if __name__ == '__main__':
    racetrack = load_file('day20_race.txt')
    # racetrack = load_file('day20_race_sample.txt')
    race_track(racetrack)

