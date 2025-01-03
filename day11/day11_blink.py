def load_blink(filename):
    """
    Load blink state from file.
    Returns a string representing the state.
    """
    with open(filename, 'r') as file:
        return [[[s] for s in l.strip().split()] for l in file][0]

def xflatten(l):
    fl = []
    for a in l:
        if type(a) == list:
            fl += a
        else:
            fl += [a]
    return fl


def split_stone(stone):
    if len(stone) % 2 == 0:
        return [stone[:len(stone)//2],str(int(stone[len(stone)//2:]))]
    if stone == '0':
        return ['1']
    return [str(int(stone) * 2024)]

blink_cache = {}
def blink_stone(stone, blink_count = 1):
    if len(stone) == 1:
        if (stone[0] + '_' + str(blink_count)) in blink_cache:
            return blink_cache[stone[0] + '_' + str(blink_count)]
    if blink_count == 1:
        return sum([len(split_stone(s)) for s in stone])
    s = sum([blink_stone(split_stone(s), blink_count - 1) for s in stone])
    if len(stone) == 1:
        blink_cache[stone[0] + '_' + str(blink_count)] = s
    return s

def calc(stones):
    
    num_blinks = 75

    # num_stones = 0
    # splits = []
    # for s in stones:
    #     splits = s
    #     for b in range(0, num_blinks):
    #         new_splits = []
    #         for stone in splits:
    #             new_splits += split_stone(stone)
    #         splits = new_splits
    #         # print("blink #", b, len(splits))
    #     num_stones += len(splits)

    print('w cache: ', sum([blink_stone(s, num_blinks) for s in stones]))

    # print('no cache: ', num_stones)

def main():
    # filename = "day11_blink_sample.txt"
    filename = "day11_blink.txt"
    stones = load_blink(filename)
    calc(stones)

if __name__ == "__main__":
    main()


