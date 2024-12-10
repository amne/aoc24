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
    Process location pairs from file, sort them, and calculate metrics
    """
    list_a, list_b = load_location_lists(filename)
    difference = calculate_total_difference(list_a, list_b)
    similarity = calculate_similarity(list_a, list_b)
    return difference, similarity

def calculate_total_difference(list_a, list_b):
    """Calculate the sum of absolute differences between two sorted lists"""
    return sum(abs(a - b) for a, b in zip(list_a, list_b))

def calculate_similarity(list_a, list_b):
    """Calculate similarity by counting occurrences of each item from A in B"""
    similarity = 0
    for item in list_a:
        count_in_b = item * list_b.count(item)
        similarity += count_in_b
    return similarity

if __name__ == "__main__":
    try:
        difference, similarity = process_locations("locations.txt")
        print(f"Sum of differences: {difference}")
        print(f"Similarity score: {similarity}")
    except FileNotFoundError:
        print("Error: locations.txt file not found")
    except ValueError:
        print("Error: Invalid file format. Each line should contain two integers separated by space")
