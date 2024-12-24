def load_bits(filename):
    with open(filename) as f:
        bits = {}
        ops = {}
        for line in f:
            if not line.strip():
                break
            bit_name, bit_value = line.strip().split(': ')
            bits[bit_name] = int(bit_value)
        for line in f:
            op = line.strip().split(' -> ')
            left_bit, op_name, right_bit = op[0].split(' ')
            dest_bit = op[1]
            if dest_bit not in bits:
                bits[dest_bit] = None
            ops[dest_bit] = (dest_bit, (op_name, (left_bit, right_bit)))  #  ((left_bit, op_name, right_bit, dest_bit))
    return bits, ops


def to_plantuml(bits, ops):
    print('@startuml')
    for bit, value in bits.items():
        print(f'object {bit}')
    for dest_bit, op in ops.items():
        op_name, (left_bit, right_bit) = op[1]
        print(f'object {left_bit}_{op_name}_{right_bit}')
        print(f'{left_bit} --> {left_bit}_{op_name}_{right_bit}')
        print(f'{right_bit} --> {left_bit}_{op_name}_{right_bit}')
        print(f'{left_bit}_{op_name}_{right_bit} --> {dest_bit}')
    print('@enduml')

if __name__ == '__main__':
    bits, ops = load_bits('day24_bits.txt')
    to_plantuml(bits, ops)
