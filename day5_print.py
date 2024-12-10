def load_print_data(filename):
    """
    Load print data from file containing two sections:
    1. Print order: pairs of ints formatted as "int|int"
    2. Updates: lists of ints separated by commas
    Sections are separated by an empty line
    """
    print_order = []
    updates = []
    
    with open(filename, 'r') as file:
        # Read print order section
        for line in file:
            line = line.strip()
            if not line:  # Empty line marks section boundary
                break
            left, right = line.split('|')
            print_order.append((int(left), int(right)))
            
        # Read updates section
        for line in file:
            line = line.strip()
            if line:
                numbers = [int(x) for x in line.split(',')]
                updates.append(numbers)
                
    return print_order, updates

def build_graph(print_order):
    """Build directed graph from print order rules"""
    graph = {}
    for before, after in print_order:
        if before not in graph:
            graph[before] = set()
        if after not in graph:
            graph[after] = set()
        graph[before].add(after)
    return graph

def is_valid_sequence(graph, sequence):
    """Check if sequence follows ordering rules"""
    for i in range(len(sequence)-1):
        current = sequence[i]
        next_page = sequence[i+1]
        
        # Do DFS to check if there's a path from next_page to current
        # If such path exists, it violates the ordering rules
        visited = set()
        stack = [next_page]
        while stack:
            node = stack.pop()
            if node == current:
                return False
            if node not in visited:
                visited.add(node)
                stack.extend(graph[node])
    return True

def process_updates(print_order, updates):
    """Process updates and return sum of valid middle numbers"""
    graph = build_graph(print_order)
    total = 0
    
    for update in updates:
        if len(update) >= 3 and is_valid_sequence(graph, update):
            middle_idx = len(update) // 2
            total += update[middle_idx]
            
    return total

if __name__ == "__main__":
    try:
        print_order, updates = load_print_data("day5_print.txt")
        result = process_updates(print_order, updates)
        print(f"Sum of middle numbers from valid sequences: {result}")
    except FileNotFoundError:
        print("Error: Input file 'day5_print.txt' not found")
    except Exception as e:
        print(f"Error processing file: {e}")
