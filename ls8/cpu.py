"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        # general purpose registers for doing work
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.opcodes = {
            "LDI": 0b10000010,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "HLT": 0b00000001,
        }

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """
        Load a program into memory.
        """
        address = 0

        if len(sys.argv) != 2:
            print('Please Follow Example Usage: ls8.py filename')
            sys.exit(1)

        try:

            with open(sys.argv[1]) as f:
                for line in f:
                    split = line.split('#')
                    code = split[0].strip()

                    if code == '':
                        continue

                    num = int(code, 2)
                    self.ram_write(num, address)
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[1]} file not found')
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[0] = reg_a * reg_b
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True
        
        while running:
            # read line by line from ram
            instruction = self.ram[self.pc]

            if instruction == self.opcodes["LDI"]:
                self.load()
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == self.opcodes["MUL"]:
                self.alu("MUL", self.reg[0], self.reg[1])
                self.pc += 3

            elif instruction == self.opcodes["PRN"]:
                reg_locaton = self.ram_read(self.pc + 1)
                print(self.reg[reg_locaton])
                self.pc += 2

            elif instruction == self.opcodes["HLT"]:
                running = False
                self.pc += 1
                
            
            else:
                running = False
                print(f'Unknown instruction {instruction}')
                

            