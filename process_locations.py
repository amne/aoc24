def process_locations(filename):
    """
    Process location pairs from file, sort them, and calculate sum of differences
    File format: each line contains two integers separated by space
    """
    list_a = []
    list_b = []
    
    # Read and parse the file
    with open(filename, 'r') as file:
        for line in file:
            a, b = map(int, line.strip().split())
            list_a.append(a)
            list_b.append(b)
    
    # Sort both lists
    list_a.sort()
    list_b.sort()
    
    # Calculate sum of differences
    total_diff = sum(abs(a - b) for a, b in zip(list_a, list_b))
    
    return total_diff

if __name__ == "__main__":
    try:
        result = process_locations("locations.txt")
        print(f"Sum of differences: {result}")
    except FileNotFoundError:
        print("Error: locations.txt file not found")
    except ValueError:
        print("Error: Invalid file format. Each line should contain two integers separated by space")
