def load_file(file_path):
    claw_machines = []
    with open(file_path, 'r') as f:
        claw_machine = []
        for line in f:
            claw_spec = line.strip().split(':')
            if claw_spec[0].startswith('Button A'):
                buttonA_X = int(claw_spec[1].split(',')[0].split('+')[1].strip(','))
                buttonA_Y = int(claw_spec[1].split(',')[1].split('+')[1].strip(','))
                claw_machine.append((buttonA_X, buttonA_Y))
            if claw_spec[0].startswith('Button B'):
                buttonB_X = int(claw_spec[1].split(',')[0].split('+')[1].strip(','))
                buttonB_Y = int(claw_spec[1].split(',')[1].split('+')[1].strip(','))
                claw_machine.append((buttonB_X, buttonB_Y))
            if claw_spec[0].startswith('Prize'):
                prize_X = 10000000000000 + int(claw_spec[1].split(',')[0].split('=')[1].strip(','))
                prize_Y = 10000000000000 + int(claw_spec[1].split(',')[1].split('=')[1].strip(','))
                claw_machine.append((prize_X, prize_Y))
            if not line.strip():
                claw_machines.append(claw_machine)
                claw_machine = []
        else:
            claw_machines.append(claw_machine)
    return claw_machines

def solve_claw_machine(claw_machine):
    m = [
         [claw_machine[0][0], claw_machine[1][0], claw_machine[2][0]],
         [claw_machine[0][1], claw_machine[1][1], claw_machine[2][1]]
        ]
    m_det = m[0][0]*m[1][1] - m[0][1]*m[1][0]
    m_det_x = m[0][2]*m[1][1] - m[0][1]*m[1][2]
    m_det_y = m[0][0]*m[1][2] - m[0][2]*m[1][0]
    x = m_det_x / m_det
    y = m_det_y / m_det
    if int(x) == x and int(y) == y:
        return int(x*3 + y)
    return 0

def solve_claw_tokens(claw_machines):
    # [print(claw_machine) for claw_machine in claw_machines]
    print(sum(solve_claw_machine(claw_machine) for claw_machine in claw_machines))

if __name__ == "__main__":
    claw_machines = load_file('day13_claw.txt')
    # claw_machines = load_file('day13_claw_sample.txt')
    solve_claw_tokens(claw_machines)

