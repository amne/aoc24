def load_tumblers(file):
    tumblers = []
    keys = []
    with open(file, 'r') as f:
        tumbler = []
        for line in f:
            if line == '\n':
                if tumbler[0][0] == '.':
                    keys.append(tumbler)
                else:   
                    tumblers.append(tumbler)
                tumbler = []
            else:
                tumbler.append(list(line.strip()))
        else:
            if tumbler[0][0] == '.':
                keys.append(tumbler)
            else:
                tumblers.append(tumbler)
    return tumblers, keys


def key_code(key):
    return tumbler_code(list(reversed(key)))


def tumbler_code(tumbler):
    tumbler_heights = [0] * len(tumbler[0])
    for i in range(1, len(tumbler)):
        for j in range(len(tumbler[i])):
            if tumbler[i][j] == '#':
                tumbler_heights[j] += 1
    return tumbler_heights



def solve(tumblers, keys):
    tumbler_heights = []
    for tumbler in tumblers:
        # [print(''.join(row)) for row in tumbler]
        tumbler_heights.append(tumbler_code(tumbler))
        # print(tumbler_code(tumbler))
    key_heights = []
    for key in keys:
        # [print(''.join(row)) for row in key]
        key_heights.append(key_code(key))
        # print(key_code(key))
    key_lock_combos = 0
    for key in key_heights:
        for tumbler in tumbler_heights:
            # print(list(zip(key,tumbler)))
            l = [x[0]+x[1] for x in zip(key, tumbler)]
            if all([x <= 5 for x in l]):
                key_lock_combos += 1
    print(key_lock_combos)



if __name__ == '__main__':
    # tumblers, keys = load_tumblers('day25_tumblers_sample.txt')
    tumblers, keys = load_tumblers('day25_tumblers.txt')
    solve(tumblers, keys)
