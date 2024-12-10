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
    """Check if difference between consecutive numbers is less than 2"""
    for i in range(len(number_list) - 1):
        if abs(number_list[i] - number_list[i + 1]) >= 2:
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
        result = process_levels("day2_levels.txt")
        print(f"Number of valid lists: {result}")
    except FileNotFoundError:
        print("Error: Input file 'day2_levels.txt' not found")
    except Exception as e:
        print(f"Error processing file: {e}")
