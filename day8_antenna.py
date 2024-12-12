def load_antenna_map(filename):
    """
    Load antenna map from file.
    Returns a list of strings representing the grid.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def calculate_antinodes(antenna_map):
    """
    Calculate antinodes in the antenna map.
    To be implemented.
    """
    pass

def main():
    filename = "day8_antenna.txt"
    antenna_map = load_antenna_map(filename)
    result = calculate_antinodes(antenna_map)
    print(f"Antenna map loaded, size: {len(antenna_map)}x{len(antenna_map[0])}")

if __name__ == "__main__":
    main()
