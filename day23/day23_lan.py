from itertools import permutations

def load_lan(filename):
    connections = []
    computer_links = {}
    with open(filename) as f:
        for line in f:
            if not line.strip():
                break
            a,b = line.strip().split('-')
            if a[0] > b[0]:
                a,b = b,a
            connections.append((a,b))
            if a in computer_links:
                computer_links[a].append(b)
            else:
                computer_links[a] = [b]
            if b in computer_links:
                computer_links[b].append(a)
            else:
                computer_links[b] = [a]
    return connections, computer_links



def find_n3(computer_links, connections, match_1st = 't'):
    games = set()
    for computer, computer_network in computer_links.items():
        perms = [p for p in permutations(computer_network, 2) if (p[0], p[1]) in connections or (p[1], p[0]) in connections]
        for p in perms: 
            games.add(tuple(sorted((computer,) + p)))
    # [print(g) for g in games]
    print(len(list(filter(lambda x: [c[0] == match_1st for c in x].count(True) > 0, games))))

def find_n3_2(computer_links, connections, match_1st = 't'):
    networks = set() 
    for computer in sorted(computer_links.keys()):
        for network in connections:
            if computer < network[1]:
                continue
            connected = True
            for c in network:
                if computer not in computer_links[c]:
                    connected = False
                    break
            if connected:
                if 't' in network[0][0] + network[1][0] + computer[0]:
                    networks.add((network[0], network[1], computer))
    print(len(networks))
    # [print(n) for n in networks]
    


def find_max_network(computer_links, connections):
    # some of the sorts got left behind from a failed attempt to solve this problem
    for computer, computer_network in computer_links.items():
        computer_network.sort()
    # [print(c, computer_links[c]) for c in sorted(computer_links)]
    max_network = []
    networks = [[k] for k in computer_links.keys()]
    for computer in sorted(computer_links.keys()):
        for network in networks:
            connected = True
            for c in network:
                if computer not in computer_links[c]:
                    connected = False
                    break
            if connected:
                network.append(computer)
    for n in set([tuple(sorted(n)) for n in networks]):
        if len(n) > len(max_network):
            max_network = n
    # print(max_network)
    print(','.join(max_network))


def find_t(computer_links, connections):
    find_n3_2(computer_links, connections) # much faster than find_n3
    # find_n3(computer_links, connections)
    find_max_network(computer_links, connections)
    return



if __name__ == '__main__':
    # connections, computer_links = load_lan('day23_lan_sample.txt')
    connections, computer_links = load_lan('day23_lan.txt')
    find_t(computer_links, connections)

