"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.sp = 256
        self.flag = '00000000'

    def load(self, program_file):
        """Load a program into memory."""

        address = 0

        program = []

        with open(str(program_file)) as f:
            for line in f:
                line = line.split(' ')[0].rstrip()
                if len(line) == 8:
                    program.append(line)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b, shift = None):
        
        if op == 'ADD':
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "AND":
            self.register[reg_a] = self.register[reg_a] & self.register[reg_b]
        elif op == "OR":
            self.register[reg_a] = self.register[reg_a] | self.register[reg_b]
        elif op == "NOT":
            if self.register[reg_b] == None:
                self.register[reg_a] = ~self.register[reg_a]
            elif self.register[reg_a] == None:
                self.register[reg_b] = ~self.register[reg_b]
        elif op == "SHL" and shift != None:
            if self.register[reg_a] != None and self.register[reg_b] == None:
                self.register[reg_a] != self.register[reg_a] << shift
            elif self.register[reg_b] != None and self.register[reg_a] == None:
                self.register[reg_b] == self.register[reg_b] >> shift
        elif op == "MOD":
            self.register[reg_a] = self.register[reg_a] % self.register[reg_b]
        else:
            raise Exception("Unsupported")

    def trace(self):
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
        """Run the CPU."""
        running = True
        while running:
            # LDI/ Load Immediate /Loads an 8 bit constant directly to reg 16 to 31
            if self.ram[self.pc] == '10000010':
                self.register[int(self.ram[self.pc + 1], 2)] = self.ram[self.pc + 2]
                self.pc += 3
            # PRN
            elif self.ram[self.pc] == '01000111':
                print(int(self.register[int(self.ram[self.pc + 1],2 )], 2))
                self.pc += 2

            # MUL
            elif self.ram[self.pc] == '10100010':
                a = self.register[int(self.ram[self.pc + 1], 2)]
                b = self.register[int(self.ram[self.pc + 2], 2)]
                a = int(str(a), 2)
                b = int(str(b), 2)
                print(a * b)
                self.pc += 3

            # ADD
            elif self.ram[self.pc] == '10100000':
                first = self.register[int(self.ram[self.pc +1], 2)]
                second = self.register[int(self.ram[self.pc + 2], 2)]
                byte = bin(int(first, 2) + int(second, 2)).lstrip('0b')
                byte = '0' * (8 - len(byte)) + byte 
                self.register[int(self.ram[self.pc + 1], 2)] = byte
                self.pc += 3
            # PUSH
            elif self.ram[self.pc] == '01000101':
                self.sp -= 1
                self.ram[self.sp] = self.register[int(self.ram[self.pc + 1], 2)]
                self.pc += 2

            # POP
            elif self.ram[self.pc] == '01000110':
                self.ram[self.sp] = self.register[int(self.ram[self.pc + 1], 2)] = self.ram[self.sp]
                self.sp += 1
                self.pc += 2

            # CALL
            elif self.ram[self.pc] == '01010000':
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                self.pc = int(self.register[int(self.ram[self.pc + 1], 2)], 2)

            #RET
            elif self.ram[self.pc] == '00010001':
                 self.pc = self.ram[self.sp]
                 self.sp += 1
            # CMP
            elif self.ram[self.pc] == '10100111':
                reg_a = int(self.register[int(self.ram[self.pc + 1], 2)], 2)
                reg_b = int(self.register[int(self.ram[self.pc + 2], 2)], 2)
                if reg_a == reg_b:
                    self.flag = '00000001'
                elif reg_a > reg_b:
                    self.flag = '00000010'
                elif reg_a < reg_b:
                    self.flag = '00000100'
                self.pc += 3

            # JMP
            elif self.ram[self.pc] == '01010100':
                self.pc = int(self.register[int(self.ram[self.pc + 1], 2)], 2)

            # JEQ
            elif self.ram[self.pc] == '01010101':
                if self.flag == '00000001':
                    self.pc = int(self.register[int(self.ram[self.pc + 1], 2)], 2)
                else:
                    self.pc += 2
            # JNE
            elif self.ram[self.pc] == '01010110':
                if self.flag != '00000001':
                    self.pc = int(self.register[int(self.ram[self.pc + 1], 2)], 2)
                else:
                    self.pc += 2
            # HLT
            elif self.ram[self.pc] == '00000001':
                    self.pc = 0
                    break
            else: 
                    print(f'{self.ram[self.pc]} is unknown')
                    break





    def ram_read(self, address):
        return self.ram[int(str(address), 2)]

    def ram_write(self, address, value):
        self.ram[int(str(address), 2)] = value