import numpy

def parse_equations():
    """
    Parse equations from stdin.
    Each line format: "int: list of ints separated by space"
    Returns list of tuples (target, numbers)
    """
    equations = []
    try:
        # while True:
        with open('day7_eq.txt', 'r') as f:
            for line in f:
            # return [list(line.strip()) for line in f]
                # line = input().strip()
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
    # allowed_ops = [('*', lambda x: x[0]*x[1]), ('+', lambda x: x[0]+x[1])]
    allowed_ops = [('*', lambda x: x[0]*x[1]), ('+', lambda x: x[0]+x[1]), ('||', lambda x: int(str(x[0])+str(x[1])))]
    # TODO: Implement solution
    # backtrack?
    # we only have two ops: 0 and 1
    # encode the op stack as a binary
    # we will have n-1 operations
    numops = len(allowed_ops)
    opstack = numops**(len(numbers)-1)-1
    def applyops(number_list, opstack):
        encoded_ops = numpy.base_repr(opstack, base=numops).zfill(len(number_list)-1)
        # encoded_ops = ('{:0=' + str(len(number_list)-1) + 'b}').format(opstack)
        # print(number_list, encoded_ops)
        # for op in encoded_ops:
        result = number_list[0]
        for i in range(1, len(number_list)):
            # op = allowed_ops[opstack & 1]
            op = allowed_ops[int(encoded_ops[i-1])]
            result = op[1]((result,number_list[i]))
            # opstack = opstack >> 1
        return result
    while opstack > -1:
        eq = applyops(numbers, opstack)
        # print(eq)
        if eq == target:
            return eq
        opstack-=1
    # print(0)
    return 0

def main():
    equations = parse_equations()
    total = 0
    for target, numbers in equations:
        result = eq_solve(target, numbers)
        total += result
        # TODO: Print results once eq_solve is implemented
        # print(f"Target: {target}, Numbers: {numbers}")
    print("total = ", total)

if __name__ == "__main__":
    main()
