import time
class Computer:
    registers = {}
    ip = 0
    code = []
    output = []
    opcodes = {}
    def __init__(self):
        self.registers = {'A': 0, 'B': 0, 'C': 0}
        self.ip = 0
        self.code = []
        self.opcodes = {
            0: self._adv,
            1: self._bxl,
            2: self._bst,
            3: self._jnz,
            4: self._bxc,
            5: self._out,
            6: self._bdv,
            7: self._cdv
        }


    def __str__(self):
        return f"Registers: {self.registers}\nIP: {self.ip}\nCode: {self.code}\nOutput: {self.output}"

    def _adv(self, operand):
        self.registers['A'] = self.registers['A'] // (2**self.resolve_operand(operand))

    def _bxl(self, operand):
        self.registers['B'] = self.registers['B'] ^ operand

    def _bxc(self, operand):
        self.registers['B'] = self.registers['B'] ^ self.registers['C']

    def _bst(self, operand):
        self.registers['B'] = self.resolve_operand(operand) % 8

    def _jnz(self, operand):
        if self.registers['A'] != 0:
            self.ip = operand - 2

    def _out(self, operand):
        self.output.append(self.resolve_operand(operand) % 8)

    def _bdv(self, operand):
        self.registers['B'] = self.registers['A'] // (2**self.resolve_operand(operand))

    def _cdv(self, operand):
        self.registers['C'] = self.registers['A'] // (2**self.resolve_operand(operand))


    def resolve_operand(self, operand) -> int:
        match operand:
            case 4:
                return self.registers['A']
            case 5:
                return self.registers['B']
            case 6:
                return self.registers['C']
            case 7:
                raise ValueError('Reserved operand')
            case _:
                return operand

    def run(self):
        # print(self)
        while self.ip >=0 and self.ip < len(self.code)-1:
            opcode = self.code[self.ip]
            operand = self.code[self.ip+1]
            self.opcodes[opcode](operand)
            self.ip += 2


    def repair(self):
        # a = 8 ** 13
        a = 37222273794941 # 8 ** 15
        p = 14
        # a = 48744869
        b = self.registers['B']
        c = self.registers['C']
        while True:
            # if a % 8 ** 5 == 0:
            time.sleep(0.01)
            print(a, p)
            print(len(self.code), ",".join([str(c) for c in self.code]))
            print(len(self.output), ",".join([str(o) for o in self.output]))
            if len(self.output) == len(self.code):
                l = 0
                while self.output[-(l+1):] == self.code[-(l+1):]:
                    l += 1
                p= max(0, 14-l)
            self.registers['A'] = a
            self.registers['B'] = b
            self.registers['C'] = c
            self.output = []
            self.ip = 0
            while self.ip >=0 and self.ip < len(self.code)-1:
                opcode = self.code[self.ip]
                operand = self.code[self.ip+1]
                self.opcodes[opcode](operand)
                self.ip += 2
                # if self.output != self.code[:len(self.output)]:
                #     break
            if self.output == self.code:
                print(f"Found a: {a}")
                break
            a += 8**p

def load_file(filename):
    pc = Computer()
    with open(filename) as f:
        for line in f:
            if not line.strip():
                continue
            if line.startswith('Register A'):
                pc.registers['A'] = int(line.split(': ')[-1]) 
            if line.startswith('Register B'):
                pc.registers['B'] = int(line.split(': ')[-1]) 
            if line.startswith('Register C'):
                pc.registers['C'] = int(line.split(': ')[-1])
            if line.startswith('Program:'):
                pc.code = [int(i) for i in line.split(': ')[-1].strip().split(',')]
    return pc


if __name__ == '__main__':
    # pc = load_file('day17_code_sample.txt')
    pc = load_file('day17_code.txt')
    pc.run()
    print(pc)
    pc.repair()

