"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.opcodes = {
            "LDI": 0b10000010,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "HLT": 0b00000001,
            "PUSH": 0b01000101,
            "POP": 0b01000110,
            "CMP": 0b10100111,
            "JMP": 0b01010100,
            "JEQ": 0b01010101,
            "JNE": 0b01010110
        }
        # general purpose registers for doing work
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        # flags register
        self.reg[4] = {}
        self.flags = self.reg[4]
        self.flags['E'] = False
        self.flags['L'] = False
        self.flags['G'] = False
        # reserve position 7 for SP and set value to top position of ram
        self.reg[7] = len(self.ram) -1
        self.sp = self.reg[7]

        self.running = False
        # dict to map instructions to their respective function handler 
        self.branch_table = {}
        self.branch_table[self.opcodes["LDI"]] = self.handle_ldi
        self.branch_table[self.opcodes["PRN"]] = self.handle_prn
        self.branch_table[self.opcodes["MUL"]] = self.handle_mul
        self.branch_table[self.opcodes["HLT"]] = self.handle_hlt
        self.branch_table[self.opcodes["PUSH"]] = self.handle_push
        self.branch_table[self.opcodes["POP"]] = self.handle_pop
        self.branch_table[self.opcodes["CMP"]] = self.handle_cmp
        self.branch_table[self.opcodes["JMP"]] = self.handle_jmp
        self.branch_table[self.opcodes["JEQ"]] = self.handle_jeq
        self.branch_table[self.opcodes["JNE"]] = self.handle_jne


    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
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
        elif op == "CMP":
            if reg_a == reg_b:
                self.flags['E'] = True
            elif reg_a < reg_b:
                self.flags['L'] = True
            elif reg_b > reg_b:
                self.flags['G'] = True
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.flags,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_ldi(self):
        self.load()
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_mul(self):
        self.alu("MUL", self.reg[0], self.reg[1])
        self.pc += 3

    def handle_prn(self):
        reg_locaton = self.ram_read(self.pc + 1)
        print(self.reg[reg_locaton])
        self.pc += 2

    def handle_hlt(self):
        self.running = False
        self.pc += 1
    
    def handle_push(self):
        given_register = self.ram[self.pc + 1]
        value_in_register = self.reg[given_register]
        # decrement the Stack Pointer
        self.sp -= 1
        # write the value of the given register to memory AT the SP location
        self.ram[self.sp] = value_in_register
        self.pc += 2 

    def handle_pop(self):
        given_register = self.ram[self.pc + 1]
        # Write the value in memory at the top of stack to the given register
        value_from_memory = self.ram[self.sp]
        self.reg[given_register] = value_from_memory
        # increment the stack pointer
        self.sp += 1
        self.pc += 2

    def handle_cmp(self):
        self.alu("CMP", self.reg[0], self.reg[1])
        self.pc += 3
    
    def handle_jmp(self):
        # get the given register in the operand
        given_register = self.ram[self.pc + 1]
        self.pc = self.reg[given_register]

    def handle_jeq(self):
        given_register = self.ram[self.pc + 1]
        if self.flags['E'] is True:
            self.pc = self.reg[given_register]
        else:
            self.pc += 2
    
    def handle_jne(self):
        given_register = self.ram[self.pc + 1]
        if self.flags['E'] == False:
            self.pc = self.reg[given_register]
        else:
            self.pc += 2

    def run(self):
        self.running = True

        while self.running:
            # read line by line from ram
            instruction = self.ram[self.pc]
            # if instruction exists in branch table
            if instruction in self.branch_table:
                # run function handler for that instruction
                self.branch_table[instruction]()
            else:
                self.running = False
                print(f'Unknown instruction {bin(instruction)}')
                sys.exit(1)
