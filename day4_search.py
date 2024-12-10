def load_matrix(filename):
    """Load letter matrix from file"""
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            # Convert each line to a list of characters, removing whitespace
            row = [char for char in line.strip()]
            matrix.append(row)
    return matrix

def search_word(matrix, word):
    """
    Search for word in all 8 directions
    Returns count of occurrences
    """
    if not matrix or not matrix[0]:
        return 0
        
    rows = len(matrix)
    cols = len(matrix[0])
    count = 0
    
    # Define all 8 directions as (row_delta, col_delta)
    directions = [
        (-1, -1),  # up-left
        (-1, 0),   # up
        (-1, 1),   # up-right
        (0, -1),   # left
        (0, 1),    # right
        (1, -1),   # down-left
        (1, 0),    # down
        (1, 1)     # down-right
    ]
    
    def is_valid_position(row, col):
        return 0 <= row < rows and 0 <= col < cols
    
    def check_direction(start_row, start_col, delta_row, delta_col):
        """Check if word exists starting from given position in given direction"""
        if not is_valid_position(start_row + (len(word)-1)*delta_row, 
                               start_col + (len(word)-1)*delta_col):
            return False
            
        for i in range(len(word)):
            current_row = start_row + i*delta_row
            current_col = start_col + i*delta_col
            if matrix[current_row][current_col] != word[i]:
                return False
        return True
    
    # Check each position as potential start
    for row in range(rows):
        for col in range(cols):
            # Try all directions from this position
            for delta_row, delta_col in directions:
                if check_direction(row, col, delta_row, delta_col):
                    count += 1
                    
    return count

def find_xmas(filename):
    """
    Find all occurrences of 'XMAS' in the matrix
    Returns total count
    """
    try:
        matrix = load_matrix(filename)
        count = search_word(matrix, "XMAS")
        return count
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found")
        return 0
    except Exception as e:
        print(f"Error processing file: {e}")
        return 0

if __name__ == "__main__":
    count = find_xmas("day4_search.txt")
    print(f"Found 'XMAS' {count} times in the matrix")
