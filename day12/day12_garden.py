def load_garden_map(filename):
    """
    Load garden map from file.
    Returns a list of strings representing the grid.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def inmap(garden_map, pos):
    return (pos[0] >= 0 and pos[0] < len(garden_map)
            and pos[1] >= 0 and pos[1] < len(garden_map[0]))


def calculate_fence_cost(garden_map):
    """
    Calculate fence cost for the garden map.
    """
    UP = 8
    LEFT = 4
    DOWN = 2
    RIGHT = 1
    # directions are bitmask: 1: right, 2: down, 4: left, 8: up
    directions = {RIGHT: (0,1), DOWN: (1,0), LEFT: (0,-1), UP: (-1,0)}
    concave_corners = [UP & LEFT, DOWN & LEFT, DOWN & RIGHT, UP & RIGHT]
    corner_pairs = [(UP, RIGHT), (RIGHT, DOWN), (DOWN, LEFT), (LEFT, UP)]
    # directions in binary: right: 0b0001, down: 0b0010, left: 0b0100, up: 0b1000 
    # each point is tagged with an area id and a bitmask of connected points
    tagged_garden_map = [[(0,0) for c in range(0, len(garden_map[l]))] for l in range(0, len(garden_map))]
    areas = {}
    area = 1
    # function to find first point not tagged
    def find_next_point(tagged_garden_map):
        for l in range(0, len(tagged_garden_map)):
            for c in range(0, len(tagged_garden_map[l])):
                if tagged_garden_map[l][c][0] == 0:
                    return (l,c)
        return None
    np = find_next_point(tagged_garden_map)
    while np is not None:
        to_visit = set([np])
        areas[area] = set()
        while to_visit:
            p = to_visit.pop()
            tagged_garden_map[p[0]][p[1]] = (area, 0)
            for b, d in directions.items():
                next_p = (p[0]+d[0],p[1]+d[1])
                if inmap(garden_map, next_p) and (garden_map[next_p[0]][next_p[1]] == garden_map[p[0]][p[1]]):
                    tagged_garden_map[p[0]][p[1]] = (area, tagged_garden_map[p[0]][p[1]][1] | b)
                    if (tagged_garden_map[next_p[0]][next_p[1]][0] == 0):
                        to_visit.add(next_p)
        area+=1
        np = find_next_point(tagged_garden_map)

    # add each point to the area dict
    for l in range(0, len(tagged_garden_map)):
        for c in range(0, len(tagged_garden_map[l])):
            areas[tagged_garden_map[l][c][0]].add((l,c))

    # for l in range(0, len(garden_map)):
    #     print(garden_map[l])
    # print("===")
    # for l in range(0, len(tagged_garden_map)):
    #     print("".join([str(tagged_garden_map[l][c][0]) for c in range(0, len(tagged_garden_map[l]))]))
    # print("===")
    # for l in range(0, len(tagged_garden_map)):
    #     for c in range(0, len(tagged_garden_map[l])):
    #         # print(f"{tagged_garden_map[l][c][1]:04b}", end=" ")
    #         print(format(tagged_garden_map[l][c][1], "04b"), end=" ")
    #     print("")
    # print("===")
    # for l in range(0, len(tagged_garden_map)):
    #     for c in range(0, len(tagged_garden_map[l])):
    #         # print(f"{tagged_garden_map[l][c][1]:04b}", end=" ")
    #         print("%s*%s" % (tagged_garden_map[l][c][0], format(tagged_garden_map[l][c][1] ^ 0b1111, "04b")), end=" ")
    #     print("")
    # for a in areas:
    #     print(f"area {a}: {areas[a]}")
    cost = 0
    side_cost = 0
    # each garden point is fenced on the sides that are not connected to another garden point
    # for each bitmask calculate how many zeroes in the first 4 bits
    for a in areas:
        area_cost = 0
        side_area_cost = 0
        for p in areas[a]:
            area_cost += format(tagged_garden_map[p[0]][p[1]][1], "04b").count("0")
            side_area_cost += sum([1 for c in corner_pairs if ((0b1111 ^ tagged_garden_map[p[0]][p[1]][1]) & (c[0]+c[1])) == (c[0]+c[1])])
            # check if it is inside corner
            # an inside corner has neighbours up/left, up/right, down/left, down/right
            # but the point obtained by adding both directions is not in the area
            for ccp in corner_pairs:
                if tagged_garden_map[p[0]][p[1]][1] & (ccp[0] + ccp[1]) == (ccp[0] + ccp[1]):
                    inside_p = (p[0]+directions[ccp[0]][0] + directions[ccp[1]][0], p[1]+directions[ccp[0]][1] + directions[ccp[1]][1])
                    if tagged_garden_map[inside_p[0]][inside_p[1]][0] != a:
                        side_area_cost += 1
        # print(f"area {a} cost: {len(areas[a])} * {area_cost}")
        # print(f"area {a} side cost: {len(areas[a])} * {side_area_cost}")
        cost += len(areas[a]) * area_cost
        side_cost += len(areas[a]) * side_area_cost
    print(f"total fence cost p1: {cost}")


    # p2



            

    print(f"total fence cost p2: {side_cost}")


    # p2
    # iterate each line and count sides for each area

    return cost


def main():
    # filename = "day12_garden_sample.txt"
    filename = "day12_garden.txt"
    garden_map = load_garden_map(filename)
    calculate_fence_cost(garden_map)

# if __name__ == "__main__":
main()

