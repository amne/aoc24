def load_location_lists(filename):
    """
    Load and parse location pairs from file into two lists
    File format: each line contains two integers separated by space
    """
    list_a = []
    list_b = []
    
    with open(filename, 'r') as file:
        for line in file:
            a, b = map(int, line.strip().split())
            list_a.append(a)
            list_b.append(b)
    
    # Sort both lists
    list_a.sort()
    list_b.sort()
    
    return list_a, list_b

def process_locations(filename):
    """
    Process location pairs from file, sort them, and calculate sum of differences
    """
    list_a, list_b = load_location_lists(filename)
    return calculate_total_difference(list_a, list_b)

def calculate_total_difference(list_a, list_b):
    """Calculate the sum of absolute differences between two sorted lists"""
    return sum(abs(a - b) for a, b in zip(list_a, list_b))

if __name__ == "__main__":
    try:
        result = process_locations("locations.txt")
        print(f"Sum of differences: {result}")
    except FileNotFoundError:
        print("Error: locations.txt file not found")
    except ValueError:
        print("Error: Invalid file format. Each line should contain two integers separated by space")
