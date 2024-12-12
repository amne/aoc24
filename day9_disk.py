def load_disk(filename):
    """
    Load antenna map from file.
    Returns a list of strings representing the grid.
    """
    with open(filename, 'r') as file:
        return [l.strip() for l in file][0]

def calculate_checksum(disk_raw):
    # expand disk
    disk_expanded = []
    fileBlock = True
    fileID = 0
    disk_blocks = []
    for c in disk_raw:
        if fileBlock:
            disk_expanded += [(fileID, int(c))]*int(c)
            disk_blocks += [(fileID, int(c))]
            fileID += 1
        else:
            disk_expanded += [('.', int(c))]*int(c)
            disk_blocks += [(-1, int(c))]
        fileBlock = not fileBlock
    n = len(disk_expanded)-1
    p = 0
    disk_array = list(disk_expanded)
    while '.' in [d[0] for d in disk_array[0:n-1]]:
        if disk_array[n][0] == '.':
            n-=1
            continue
        p = [d[0] for d in disk_array].index('.',p,n)
        disk_array[p] = disk_array[n]
        disk_array[n] = '.'
        n -= 1
    checksum = 0
    for i,c in enumerate(disk_array):
        if c[0] == '.':
            break
        checksum += i*c[0]

    disk_compact = list(disk_blocks)

    while fileID:
        fileID-=1
        # find file
        files = [(fileindex, f) for fileindex, f in enumerate(disk_compact) if f[0] == fileID]
        fi,f = files[-1]
        # find first block that fits this file
        blocks = [(blockindex, b) for blockindex, b in enumerate(disk_compact) if b[0] == -1 and blockindex < fi and b[1] >= f[1]]
        if not blocks:
            continue # bye
        bi,b = blocks[0]
        # replace file with empty space
        disk_compact[fi] = (-1, f[1])
        # shrink or replace empty block found
        if b[1] - f[1] > 0:
            disk_compact[bi] = (-1, b[1] - f[1])
            disk_compact = disk_compact[:bi] + [f] + disk_compact[bi:]
        else:
            disk_compact[bi] = f 

    pos = 0
    compact_checksum = 0
    for f in disk_compact:
        if f[0] == -1:
            pos += f[1]
            continue
        target = pos + f[1]
        while pos < target:
            compact_checksum += f[0] * pos
            pos += 1

        


    # print(''.join([str(d[0]) for d in disk_expanded]))
    # print(''.join([(str(d[0]).replace('-1','.'))*d[1] for d in disk_compact]))
    # print('arr: ',disk_array)
    # print('blocks:', disk_blocks)
    # print('compact: ', disk_compact)
    print(checksum)
    print('compact_xsum: ', compact_checksum)
    # print(''.join([str(d) for d in disk_array]))

def main():
    # filename = "day9_disk_sample.txt"
    filename = "day9_disk.txt"
    disk_raw = load_disk(filename)
    result = calculate_checksum(disk_raw)

if __name__ == "__main__":
    main()

