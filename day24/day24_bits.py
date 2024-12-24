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


def op_tree(op_root, ops): 
    op_root_dest = op_root[0]
    op_root_left, op_root_right = op_root[1][1]
    left_bit_op_root = None
    right_bit_op_root = None
    for op in ops.values():
        if op[0] == op_root_left:
            left_bit_op_root = op
        if op[0] == op_root_right:
            right_bit_op_root = op
    if left_bit_op_root is not None:
        op_root_left = op_tree(left_bit_op_root, ops)
    if right_bit_op_root is not None:
        op_root_right = op_tree(right_bit_op_root, ops)
    return (op_root_dest, (op_root[1][0], (op_root_left, op_root_right))) 
    
    




def eval_ops(source_bits, source_ops):
    # print(bits)
    # print(ops)
    ops = list(source_ops.items())
    bits = source_bits.copy()
    while ops:
        for dest_bit, op in ops:
            dest_bit, (op_name, ( left_bit, right_bit)) = op
            if bits[left_bit] is None or bits[right_bit] is None:
                continue
            if op_name == 'AND':
                bits[dest_bit] = bits[left_bit] & bits[right_bit]
            elif op_name == 'OR':
                bits[dest_bit] = bits[left_bit] | bits[right_bit]
            elif op_name == 'XOR':
                bits[dest_bit] = bits[left_bit] ^ bits[right_bit]
            ops.remove((dest_bit, op))
    return bits

def find_mangled_bits(bits, source_ops):
    # I was in way over my head for p2.
    # But now I know how a carry adder actually works bit by bit
    # The pattern that helped most with fixing this by hand was that for each
    # Zn bit there should be only one XOR step back to Xn^Yn
    # I printed the op tree for the bad Z bit and looked by eye what needs to be swapped
    # to fix the order of operations
    outputx = {k:v for k,v in bits.items() if k[0] == 'x'}
    outputy = {k:v for k,v in bits.items() if k[0] == 'y'}
    outputz = {k:v for k,v in bits.items() if k[0] == 'z'}
    inputnumberx = int(''.join([str(v) for k,v in sorted(outputx.items(), reverse=True)]), 2)
    inputnumbery = int(''.join([str(v) for k,v in sorted(outputy.items(), reverse=True)]), 2)
    outputnumber = int(''.join([str(v) for k,v in sorted(outputz.items(), reverse=True)]), 2)
    print('x,y: ',inputnumberx, inputnumbery)
    print('x+y: ',inputnumberx+inputnumbery, bin(inputnumberx+inputnumbery))
    print('  z: ',outputnumber, bin(outputnumber))
    good_z_bits = {'z'+f"{k:02d}":v for k,v in enumerate(reversed(bin(inputnumberx+inputnumbery)[2:]))}
    actual_z_bits = {'z'+f"{k:02d}":v for k,v in enumerate(reversed(bin(outputnumber)[2:]))}
    mangled_z_bits = []
    for k,v in good_z_bits.items():
        if actual_z_bits[k] != v:
            mangled_z_bits.append(k)
    print(good_z_bits)
    print(actual_z_bits)
    print(mangled_z_bits)


    op_z = [op for op in source_ops.values() if op[0][0] == 'z']
    op_tree_z = {}
    for op in op_z:
        op_tree_z[op[0]] = op_tree(op, source_ops)
    z_bits = {}
    z_names = [z for z in sorted(op_tree_z.keys())]
    # good_wires = []
    for z in z_names:
        z_tree = op_tree_z[z]
        z_bits[z] = eval_tree(z_tree, bits)
        print(z, '=(',z_bits[z],',',int(good_z_bits[z]),')', print_tree_paranthesis(z_tree))
        if z in mangled_z_bits:
            break
        # good_wires.extend(walk_op_tree(z_tree))
    # good_wires = set(good_wires)
    # print(len(good_wires), good_wires)
    ### swaps
    # z09, gwh
    # wgb, wbw
    # rcb, z21
    # jct, z39
    ### anwer
    # gwh,jct,rcb,wbw,wgb,z09,z21,z39

    z_bitstring = ''.join(reversed([str(z_bits[z_bit]) for z_bit in sorted(z_bits.keys())]))
    good_z_bitstring = ''.join(reversed([str(good_z_bits[z_bit]) for z_bit in sorted(good_z_bits.keys())]))
    print(z_bitstring, int(z_bitstring, 2))
    print(good_z_bitstring, int(good_z_bitstring, 2))






def print_tree_paranthesis(op_tree):
    if type(op_tree[1][1][0]) == str:
        left_bit = op_tree[1][1][0]
    else:
        left_bit = '(' + print_tree_paranthesis(op_tree[1][1][0]) + ')'
    if type(op_tree[1][1][1]) == str:
        right_bit = op_tree[1][1][1]
    else:
        right_bit = '(' + print_tree_paranthesis(op_tree[1][1][1]) + ')'
    ops = {'AND':' & ', 'OR':' | ', 'XOR':' ^ '}
    return left_bit + ops[op_tree[1][0]] + right_bit




def eval_tree(op_tree, bits):
    if type(op_tree[1][1][0]) == str:
        left_bit = bits[op_tree[1][1][0]]
    else:
        left_bit = eval_tree(op_tree[1][1][0], bits)
    if type(op_tree[1][1][1]) == str:
        right_bit = bits[op_tree[1][1][1]]
    else:
        right_bit = eval_tree(op_tree[1][1][1], bits)
    if op_tree[1][0] == 'AND':
        return left_bit & right_bit
    elif op_tree[1][0] == 'OR':
        return left_bit | right_bit
    elif op_tree[1][0] == 'XOR':
        return left_bit ^ right_bit


def walk_op_tree(op_tree):
    if type(op_tree[1][1][0]) == str:
        return []
    if type(op_tree[1][1][1]) == str:
        return []
    return [(op_tree[0],(op_tree[1][0], (op_tree[1][1][0][0], op_tree[1][1][1][0])))] + walk_op_tree(op_tree[1][1][0]) + walk_op_tree(op_tree[1][1][1])


if __name__ == '__main__':
    bits,ops = load_bits('day24_bits.txt')
    # bits,ops = load_bits('day24_bits_fixed.txt')
    # bits,ops = load_bits('day24_bits_sample_2.txt')
    # bits,ops = load_bits('day24_bits_sample.txt')
    bits = eval_ops(bits,ops)
    find_mangled_bits(bits, ops)
    to_plantuml(bits, ops)
                         
