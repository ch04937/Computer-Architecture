"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*25
        self.pc = 0  # Program counter
        self.reg = [0]*8

    def ram_read(self, address):
        '''
        should accept the address to read and return the value stored there
        '''
        self.ram[address]

    def raw_write(self, address, write_value):
        '''
        should accept a value to write, and the address to write it to
        '''
        self.ram[address] = write_value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # instruction definition so that we can refer to it by name isntead of numeric value
        HLT = 0b00000001  # HALT
        LDI = 0b10000010  # LDI
        PRN = 0b01000111  # PRN

        # self.ram_read(self.pc)
        command = self.ram[self.pc]
        print(self.ram)
        while True:
            if command == HLT:
                # HALT should exit the program
                print('bye, bye')
                sys.exit(0)
            elif command == LDI:
                # LDI print register immediate #
                register = self.ram[self.pc + 2]
                self.reg[self.pc] = register
                # self.pc += 1
                return print(f'{self.reg[self.pc]}')

            elif command == PRN:
                # print numeric value stored in the given register
                # self.pc += 1
                return print(f'{self.reg[self.pc]}')
            else:
                # else print error
                print('I did not understand that command')


c = CPU()

c.load()
c.run()
