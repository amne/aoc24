from collections import deque
from functools import cache

def load_designs(filename):
    with open(filename, 'r') as file:
        designs = []
        patterns = None
        for line in file:
            if not line.strip():
                continue
            if patterns:
                designs.append(line.strip())
            patterns = list(map(str.strip, line.strip().split(','))) if patterns is None else patterns
    return tuple(patterns), designs

def select_patterns(patterns, design):
    patterns_to_use = deque()
    for p in patterns:
        if p == design[:len(p)]:
            patterns_to_use.append(p)
    return patterns_to_use


def build_design(patterns, design):
    # arrange all patterns to build design
    patterns_to_use = [[design, select_patterns(patterns, design)]]
    good_specs = 0

    while patterns_to_use: 
        if not patterns_to_use[-1][1]:
            patterns_to_use.pop()
            continue
        pattern = patterns_to_use[-1][1].popleft()
        new_design = patterns_to_use[-1][0][len(pattern):]
        if not new_design:
            good_specs += 1
            print(patterns_to_use)
            patterns_to_use.pop()
            continue
        patterns_to_use.append([new_design, select_patterns(patterns, new_design)])
    return good_specs

@cache
def build_design_recursive(patterns, design):
    specs = 0
    for p in patterns:
        if design.startswith(p):
            new_design = design[len(p):]
            if not new_design:
                specs += 1
            else:
                specs += build_design_recursive(patterns, new_design)
    return specs

def match_designs(patterns, designs):
    print(patterns)
    print(designs)
    c = 0
    for design in designs:
        spec_count = build_design_recursive(patterns, design)
        c += spec_count
    print(c)




if __name__ == "__main__":
    # patterns, designs = load_designs("day19_towels_sample.txt")
    patterns, designs = load_designs("day19_towels.txt")
    match_designs(patterns, designs)
