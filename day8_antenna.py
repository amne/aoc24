def load_antenna_map(filename):
    """
    Load antenna map from file.
    Returns a list of strings representing the grid.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def inmap(antenna_map, pos):
    return (pos[0] >= 0 and pos[0] < len(antenna_map)
            and pos[1] >= 0 and pos[1] < len(antenna_map[0]))
           

def calculate_antinodes(antenna_map):
    """
    Calculate antinodes in the antenna map.
    To be implemented.
    """
    antennas = {}
    antinodes = set()
    for l in range(0, len(antenna_map)):
        for c in range(0, len(antenna_map[l])):
            if antenna_map[l][c] == '.':
                continue
            if antenna_map[l][c] in antennas.keys():
                antennas[antenna_map[l][c]].append((l,c))
            else:
                antennas[antenna_map[l][c]] = [(l,c)]

    def diffant(a1,a2):
        return (a2[0]-a1[0],a2[1]-a1[1])

    def addant(a1,a2):
        return (a1[0]+a2[0],a1[1]+a2[1])

    for ant_type in antennas.keys():
        for i in range(0, len(antennas[ant_type])-1):
            for ab in antennas[ant_type][i+1:]:
                aa = antennas[ant_type][i]
                antinodes.add(aa)
                antinodes.add(ab)
                # calculate in aa->ab direction
                an = addant(ab,diffant(aa,ab))
                while inmap(antenna_map,an):
                    antinodes.add(an)
                    an = addant(an,diffant(aa,ab))
                an = addant(aa,diffant(ab,aa))
                while inmap(antenna_map, an):
                    antinodes.add(an)
                    an = addant(an,diffant(ab,aa))
                # antinodes.add(addant(ab,diffant(aa,ab)))
                # antinodes.add(addant(aa,diffant(ab,aa)))

    # print(antennas)
    print(len([an for an in list(antinodes) if inmap(antenna_map, an)]))
    # print(len(filter(lambda a: inmap(antenna_map, a), list(antinodes))))

def main():
    # filename = "day8_antenna_sample.txt"
    filename = "day8_antenna.txt"
    antenna_map = load_antenna_map(filename)
    result = calculate_antinodes(antenna_map)
    print(f"Antenna map loaded, size: {len(antenna_map)}x{len(antenna_map[0])}")

if __name__ == "__main__":
    main()
