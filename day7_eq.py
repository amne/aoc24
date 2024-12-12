def parse_equations():
    """
    Parse equations from stdin.
    Each line format: "int: list of ints separated by space"
    Returns list of tuples (target, numbers)
    """
    equations = []
    try:
        while True:
            line = input().strip()
            if not line:
                break
            target, numbers = line.split(':')
            target = int(target)
            numbers = [int(x) for x in numbers.strip().split()]
            equations.append((target, numbers))
    except EOFError:
        pass
    return equations

def eq_solve(target, numbers):
    """
    Solve equation to find combination of numbers that sum to target
    Returns: To be implemented
    """
    # TODO: Implement solution
    pass

def main():
    equations = parse_equations()
    for target, numbers in equations:
        result = eq_solve(target, numbers)
        # TODO: Print results once eq_solve is implemented
        print(f"Target: {target}, Numbers: {numbers}")

if __name__ == "__main__":
    main()
