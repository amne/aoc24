def load_patrol_map(filename):
    """Load patrol map from file and return as 2D list"""
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def find_guard(patrol_map):
    """Find guard position and direction in map"""
    for i, row in enumerate(patrol_map):
        for j, cell in enumerate(row):
            if cell in '^v<>':
                return i, j, cell
    return None

def get_prev_direction(current_dir):
    """Get prev direction when turning right"""
    directions = {'^': '<', '>': '^', 'v': '>', '<': 'v'}
    return directions[current_dir]

def get_next_direction(current_dir):
    """Get next direction when turning right"""
    directions = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
    return directions[current_dir]

def move_in_direction(row, col, direction):
    """Get next position based on direction"""
    moves = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    delta_row, delta_col = moves[direction]
    return row + delta_row, col + delta_col

def count_patrol_dots(patrol_map):
    """Count dots covered by guard's patrol until exit"""
    rows, cols = len(patrol_map), len(patrol_map[0])
    obstacles = []
    for r in range(0,len(patrol_map)):
        for c in range(0,len(patrol_map[r])):
            if patrol_map[r][c] == '#':
                obstacles.append((r,c))
    
    # Find guard
    guard = find_guard(patrol_map)
    if not guard:
        return 0
    
    row, col, direction = guard
    dots_covered = set()
    path = []
    loop_points = set()
    # turns = []
    count_loops = 0
    hit_obsts = set()
    
    # If starting on a dot, count it
    if patrol_map[row][col] in '^v<>':
        # patrol_map[row][col] = '.'
        dots_covered.add((row, col))
        # path.append((row,col))
    
    covered_map = [[c for c in cols] for cols in patrol_map]
    # [print(l) for l in covered_map]

    # can loop
    def canloop(obstacles, row, col, direction):
        # turns = obstacles.copy()
        # corner 0
        # start_row = row
        # start_col = col
        # start_dir = direction
        looppath = set([((row,col), direction)])

        while True:
            next_turn = []
            match direction:
                case '^':
                    # next_turn = [t for t in turns if t[1] == get_next_direction(direction) and ( t[0][1] == col and t[0][0] < row )]
                    next_turn = [((o[0]+1, o[1]), get_next_direction(direction)) for o in obstacles if o[1] == col and o[0] < row]
                    next_turn.sort(key=lambda o: o[0][0], reverse=True)
                    # next_turn = [((next_turn[0][0][0]-1, next_turn[0][0][1]), next_turn[0][1])]
                case '>':
                    # next_turn = [t for t in turns if t[1] == get_next_direction(direction) and ( t[0][0] == row and t[0][1] > col )]
                    next_turn = [((o[0],o[1]-1), get_next_direction(direction)) for o in obstacles if o[0] == row and o[1] > col]
                    next_turn.sort(key=lambda o: o[0][1], reverse=False)
                case 'v':
                    # next_turn = [t for t in turns if t[1] == get_next_direction(direction) and ( t[0][1] == col and t[0][0] > row )]
                    next_turn = [((o[0]-1,o[1]), get_next_direction(direction)) for o in obstacles if o[1] == col and o[0] > row]
                    next_turn.sort(key=lambda o: o[0][0], reverse=False)
                case '<':
                    # next_turn = [t for t in turns if t[1] == get_next_direction(direction) and ( t[0][0] == row and t[0][1] < col )]
                    next_turn = [((o[0],o[1]+1), get_next_direction(direction)) for o in obstacles if o[0] == row and o[1] < col]
                    next_turn.sort(key=lambda o: o[0][1], reverse=True)
                
            if not next_turn:
                return False 
            row, col = next_turn[0][0]
            direction = next_turn[0][1]
            if ((row,col), direction) in looppath:
                # print("-==-")
                # print_map_path(patrol_map, looppath)
                return True
            # turns.remove(((row,col), direction))
            looppath.add(((row,col), direction))

        return False

    def print_map_path(covered_map, path):
        for p in path:
            row,col = p[0]
            direction = p[1]
            if covered_map[row][col] == '.':
                if direction == '^' or direction == 'v':
                    covered_map[row][col] = '|'
                if direction == '>' or direction == '<':
                    covered_map[row][col] = '-'
            if covered_map[row][col] == '-':
                if direction == '^' or direction == 'v':
                    covered_map[row][col] = '+'
            if covered_map[row][col] == '|':
                if direction == '<' or direction == '>':
                    covered_map[row][col] = '+'
        [print(''.join(l)) for l in covered_map]

    while True:
        # Get next position
        next_row, next_col = move_in_direction(row, col, direction)
        
        # Check if guard exits the map
        if (next_row < 0 or next_row >= rows or 
            next_col < 0 or next_col >= cols):
            break
        
        # Check if guard hits obstacle
        if patrol_map[next_row][next_col] == '#':
            hit_obsts.add((next_row, next_col))
            direction = get_next_direction(direction)
            # turns.append(((row,col), direction))
            continue
            
        # Move guard
        row, col = next_row, next_col
        
        # Count dot if present
        if patrol_map[row][col] == '.':
            dots_covered.add((row, col))
        
        # if len(path)>0 and path[-1][1] != direction:
        #     turns.append((path[-1][0], direction))
        path.append(((row, col), direction))

    for p in path:
        row, col = p[0]
        direction = p[1]
        new_obstacle = p[0] 
        if new_obstacle in obstacles:
            continue
        if canloop(obstacles + [new_obstacle], guard[0], guard[1], guard[2]):
        # if canloop(obstacles + [new_obstacle], row, col, get_next_direction(direction)): 
            if patrol_map[new_obstacle[0]][new_obstacle[1]] in '#^':
                print("oh oh again")
            loop_points.add((new_obstacle[0], new_obstacle[1]))
            count_loops+=1
    # [print(c) for c in l] for l in patrol_map]
    print("guard at ", guard)
    print("covered map")
    # [print(''.join(l)) for l in covered_map]
    for l in loop_points:
        covered_map[l[0]][l[1]] = 'O'
    print_map_path(covered_map, path)
    print('can loop : ', len(loop_points), count_loops)
    print('dots covered : ', len(dots_covered))
    print('walk length : ', len(path))
    print('obst hit ratio: ', len(hit_obsts), len(obstacles))
    # print('turns: ', len(turns))

if __name__ == "__main__":
    # patrol_map = load_patrol_map("day6_patrol_sample.txt") 
    patrol_map = load_patrol_map("day6_patrol.txt") 

    count_patrol_dots(patrol_map)
