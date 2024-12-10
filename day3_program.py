import re

def load_program(filename):
    """Load program text from file"""
    with open(filename, 'r') as file:
        return file.read().strip()

def extract_multiplications(program):
    """
    Extract all valid mul(x,y) expressions where x,y are integers
    Returns list of tuples (x,y)
    """
    # Pattern matches 'mul' followed by two integers in parentheses
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.finditer(pattern, program)
    return [(int(m.group(1)), int(m.group(2))) for m in matches]

def process_program(filename):
    """
    Process program file and return sum of all multiplications
    """
    program = load_program(filename)
    multiplications = extract_multiplications(program)
    
    # Calculate each multiplication and sum results
    total = sum(x * y for x, y in multiplications)
    return total

if __name__ == "__main__":
    try:
        result = process_program("day3_program.txt")
        print(f"Sum of all multiplications: {result}")
    except FileNotFoundError:
        print("Error: Input file 'day3_program.txt' not found")
    except Exception as e:
        print(f"Error processing file: {e}")
