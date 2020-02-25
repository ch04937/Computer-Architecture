"""CPU functionality."""

import sys

# instruction definition so that we can refer to it by name isntead of numeric value

HLT = 0b00000001  # HALT: STOP
LDI = 0b10000010  # LDI: PRINT IMMEDIATE NUMBER
PRN = 0b01000111  # PRN: PRINT NUMERIC VALUE STORED
MUL = 0b10100010  # MUL: MULTIPLY 2 STORED VALUES


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0]*25
        self.pc = 0  # Program counter
        self.reg = [0]*8
        self.rg = 0  # register counter

        # set up the branch table
        self.branchtable = {}
        self.branchtable[HLT] = self.HLT
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[MUL] = self.MUL

    def HLT(self):
        print('bye, bye')
        sys.exit(0)

    def LDI(self):
        register = self.ram[self.pc+2]
        self.reg[self.rg] = register
        self.rg += 1
        self.pc += 3

    def PRN(self):
        # print numeric value stored in the given register
        print(f'MUL R0*R1: {self.reg[0]}')
        self.pc += 2

    def MUL(self):
        # multipy the values store in two registers and store results in registerA
        self.reg[0] = self.reg[0] * self.reg[1]
        self.pc += 3

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

    def load(self, filename):
        """Load a program into memory."""
        try:
            # Open the file
            with open(filename) as f:
                # Read all the lines
                address = 0
                for line in f:
                    # Parse out comments
                    comment_split = line.strip().split("#")
                    # Cast the numbers from strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == '':
                        continue
                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('File not found')
            sys.exit(2)

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
        while True:
            command = self.ram[self.pc]
            self.branchtable[command]()


if len(sys.argv) != 2:
    print('ERROR: Must have file name')
    sys.exit(1)


c = CPU()
c.load(sys.argv[1])
print('memory: ', c.ram)
# print('reg: ', c.reg)
c.run()
