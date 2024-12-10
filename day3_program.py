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

def extract_controlled_multiplications(program):
    """
    Extract multiplications considering do() and don't() control instructions
    Returns list of tuples (x,y) for valid multiplications
    """
    # Find all control instructions and multiplications with their positions
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    
    # Get positions of all control instructions
    do_positions = [m.start() for m in re.finditer(do_pattern, program)]
    dont_positions = [m.start() for m in re.finditer(dont_pattern, program)]
    
    # Get multiplications with their positions
    mul_matches = list(re.finditer(mul_pattern, program))
    valid_muls = []
    
    for mul_match in mul_matches:
        mul_pos = mul_match.start()
        # Find the closest control instruction before this multiplication
        closest_do = max((pos for pos in do_positions if pos < mul_pos), default=-1)
        closest_dont = max((pos for pos in dont_positions if pos < mul_pos), default=-1)
        
        # If closest control is 'do' or no control found, include the multiplication
        if closest_do > closest_dont:
            x, y = int(mul_match.group(1)), int(mul_match.group(2))
            valid_muls.append((x, y))
    
    return valid_muls

def process_program(filename):
    """
    Process program file and return both types of multiplication sums:
    1. Simple: sum of all multiplications
    2. Controlled: sum of multiplications following do() rules
    """
    program = load_program(filename)
    simple_muls = extract_multiplications(program)
    controlled_muls = extract_controlled_multiplications(program)
    
    # Calculate both sums
    simple_total = sum(x * y for x, y in simple_muls)
    controlled_total = sum(x * y for x, y in controlled_muls)
    return simple_total, controlled_total

if __name__ == "__main__":
    try:
        simple_result, controlled_result = process_program("day3_program.txt")
        print(f"Sum of all multiplications (simple): {simple_result}")
        print(f"Sum of controlled multiplications (do/don't): {controlled_result}")
    except FileNotFoundError:
        print("Error: Input file 'day3_program.txt' not found")
    except Exception as e:
        print(f"Error processing file: {e}")
