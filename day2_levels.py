def load_level_lists(filename):
    """
    Load lists of integers from file
    File format: each line contains space-separated integers
    """
    lists = []
    with open(filename, 'r') as file:
        for line in file:
            numbers = [int(x) for x in line.strip().split()]
            lists.append(numbers)
    return lists

def check_difference_rule(number_list):
    """
    Check if:
    1. Difference between consecutive numbers is between 1 and 3 (1 <= diff < 3)
    2. Numbers consistently increase or decrease based on first direction
    """
    if len(number_list) <= 1:
        return True
        
    # Determine initial direction
    increasing = number_list[1] > number_list[0]
    
    for i in range(len(number_list) - 1):
        diff = number_list[i + 1] - number_list[i]
        
        # Check threshold (must be between 1 and 3)
        if abs(diff) >= 3 or abs(diff) < 1:
            return False
            
        # Check direction consistency
        if increasing and diff <= 0:
            return False
        if not increasing and diff >= 0:
            return False
            
    return True

def process_levels(filename):
    """
    Process level lists and count those following the difference rule
    """
    lists = load_level_lists(filename)
    valid_count = sum(1 for lst in lists if check_difference_rule(lst))
    return valid_count

if __name__ == "__main__":
    try:
        result = process_levels("day2_levels_sample.txt")
        print(f"Number of valid lists: {result}")
    except FileNotFoundError:
        print("Error: Input file 'day2_levels.txt' not found")
    except Exception as e:
        print(f"Error processing file: {e}")
