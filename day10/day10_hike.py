def load_hike_map(filename):
    """
    Load hike map from file.
    Returns a list of strings representing the grid.
    """
    with open(filename, 'r') as file:
        return [[int(h) for h in line.strip()] for line in file]

def inmap(hike_map, pos):
    return (pos[0] >= 0 and pos[0] < len(hike_map)
            and pos[1] >= 0 and pos[1] < len(hike_map[0]))

def hike(hike_map, startpoint):
    directions = [(-1,0), (0,1), (1,0), (0,-1)]
    climb = lambda s,d: (s[0]+d[0], s[1]+d[1])
    next_paths = set()
    for d in directions:
        next_point = climb(startpoint, d)
        if inmap(hike_map, next_point) and hike_map[next_point[0]][next_point[1]] - hike_map[startpoint[0]][startpoint[1]] == 1:
            next_paths.add(next_point)
    return next_paths



def walk_map(hike_map):
    n,m = len(hike_map), len(hike_map[0])
    start_points = []
    for i in range(0,n):
        for j in range(0,m):
            if hike_map[i][j] == 0:
                start_points.append((i,j))
    # start_points = [(0,c) for c,h in enumerate(hike_map[0]) if h == 0]
    # start_points += [(n-1,c) for c,h in enumerate(hike_map[n-1]) if h == 0]
    # start_points += [(c,m-1) for c,h in enumerate(hike_map) if h[m-1] == 0]
    # start_points += [(c,0) for c,h in enumerate(hike_map) if h[0] == 0]


    hike_paths = [(sp, hike(hike_map, sp)) for sp in start_points]
    points_scores = [set() for _ in hike_paths]
    points_rating = [0 for _ in hike_paths]
    # print(start_points)
    # print(hike_paths)
    for i,path_start in enumerate(hike_paths):
        current_path = [path_start]
        while current_path:
            if len(current_path[-1][1]) == 0:
                if hike_map[current_path[-1][0][0]][current_path[-1][0][1]] == 9:
                    points_scores[i].add(current_path[-1][0])
                    points_rating[i] += 1
                current_path = current_path[:-1]
                continue
            next_path = current_path[-1][1].pop()
            current_path.append((next_path, hike(hike_map, next_path)))

    print(sum([len(p) for p in points_scores]))
    print(sum(points_rating))

            




def main():
    # filename = "day10_hike_sample.txt"
    filename = "day10_hike.txt"
    hike_map = load_hike_map(filename)
    walk_map(hike_map)
    # result = calculate_antinodes(hike_map)
    # print(f"hike map loaded, size: {len(hike_map)}x{len(hike_map[0])}")

if __name__ == "__main__":
    main()

