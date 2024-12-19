import re

def load_file(file_path):
    with(open(file_path, 'r')) as f:
        # parse each line with a regex to match p=int,int v=int,int and grab all the ints
        robots = []
        for l in f:
            # print(l)
            p = re.search(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', l)
            if p:
                # print(p.groups())
                robot_spec = [int(x) for x in p.groups()]
                # robots.append(((p.groups()[0], p.groups()[1]), (p.groups()[2], p.groups()[3])))
                robots.append(((robot_spec[0], robot_spec[1]), (robot_spec[2], robot_spec[3])))
    return robots

def walk_robot(robot, map_size, iterations=100):
    # walk robot for iterations and wrap around map limits
    px = (robot[0][0]+robot[1][0]*iterations) % map_size[0]
    py = (robot[0][1]+robot[1][1]*iterations) % map_size[1]
    return (px, py)

def print_robot_map(robots, map_size):
    # create a map of the robots
    robot_map = [[0 for x in range(map_size[0])] for y in range(map_size[1])]
    for robot in robots:
        robot_map[robot[1]][robot[0]] += 1
    for row in robot_map:
        print(''.join([str(r).replace('0','.') for r in row]))

def count_quadrant_robots(new_robots, map_size):
    # quadrant 1 = top left
    # each quadrant struct is ((min_x, miny), (max_x, max_y))
    middle_x = (map_size[0]-1)//2
    middle_y = (map_size[1]-1)//2
    quadrants = [( (0, 0), (middle_x-1, middle_y-1) ),
                 ( (middle_x+1, 0), (map_size[0]-1, middle_y-1) ),
                 ( (0, middle_y+1), (middle_x-1, map_size[1]-1) ),
                 ( (middle_x+1, middle_y+1), (map_size[0]-1, map_size[1]-1) )]
    print(quadrants)
    quadrant_robots = [0, 0, 0, 0]
    for i,q in enumerate(quadrants):
        for robot in new_robots:
            if q[0][0] <= robot[0] <= q[1][0] and q[0][1] <= robot[1] <= q[1][1]:
                quadrant_robots[i] += 1
    return quadrant_robots

def solve_robots(robots, map_size, iterations=100):
    for i in range(11,10000,101):
        new_robots = [walk_robot(robot, map_size, i) for robot in robots]
        print("iteration ", i)
        print_robot_map(new_robots, map_size)
    # [print(robot, walk_robot(robot, map_size, iterations)) for robot in robots]
    # print_robot_map(new_robots, map_size)
    # quadrant_counts = count_quadrant_robots(new_robots, map_size)
    # print(quadrant_counts)
    # print(quadrant_counts[0]*quadrant_counts[1]*quadrant_counts[2]*quadrant_counts[3])


if __name__ == "__main__":
    robots = load_file('day14_robots.txt')
    # robots = load_file('day14_robots_sample.txt')
    solve_robots(robots, (101, 103), 100)


