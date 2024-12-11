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

def count_patrol_dots(filename):
    """Count dots covered by guard's patrol until exit"""
    # Load map
    patrol_map = load_patrol_map(filename)
    rows, cols = len(patrol_map), len(patrol_map[0])
    
    # Find guard
    guard = find_guard(patrol_map)
    if not guard:
        return 0
    
    row, col, direction = guard
    dots_covered = set()
    
    # If starting on a dot, count it
    if patrol_map[row][col] in '^v<>':
        dots_covered.add((row, col))
    
    while True:
        # Get next position
        next_row, next_col = move_in_direction(row, col, direction)
        
        # Check if guard exits the map
        if (next_row < 0 or next_row >= rows or 
            next_col < 0 or next_col >= cols):
            break
        
        # Check if guard hits obstacle
        if patrol_map[next_row][next_col] == '#':
            direction = get_next_direction(direction)
            continue
            
        # Move guard
        row, col = next_row, next_col
        
        # Count dot if present
        if patrol_map[row][col] == '.':
            dots_covered.add((row, col))
            
    return len(dots_covered)

if __name__ == "__main__":
    result = count_patrol_dots("day6_patrol.txt")
    print(f"Number of dots covered: {result}")
