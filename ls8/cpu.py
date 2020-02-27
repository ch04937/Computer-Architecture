"""CPU functionality."""

import sys

# instruction definition so that we can refer to it by name isntead of numeric value

HLT = 0b00000001  # HALT: STOP
LDI = 0b10000010  # LDI: PRINT IMMEDIATE NUMBER
PRN = 0b01000111  # PRN: PRINT NUMERIC VALUE STORED
MUL = 0b10100010  # MUL: MULTIPLY 2 STORED VALUES
PSH = 0b01000101  # PSH: PUSH THE VALUE IN THE GIVEN REGISTER TO THE STACK
POP = 0b01000110  # POP: POP THE VALUE AT THE TOP OF THE STACK INTO THE GIVEN REGISTER
CAL = 0b01010000  # CAL: CALLS A SUBROUTINE AT TEH ADDRESS STORED IN THE REGISTER
RET = 0b00010001  # RET: RETURN FROM SUBROUTINE
ADD = 0b10100000  # ADD: ADD VALUES STORED IN REGISTER


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0]*49  # memory
        self.pc = 0  # Program counter
        self.reg = [0]*8  # list of registers
        self.sp = 7  # stack pointer is R7

        # set up the branch table
        self.branchtable = {}
        self.branchtable[HLT] = self.HLT
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[MUL] = self.MUL
        self.branchtable[PSH] = self.PSH
        self.branchtable[POP] = self.POP
        self.branchtable[CAL] = self.CAL
        self.branchtable[RET] = self.RET
        self.branchtable[ADD] = self.ADD

    def ADD(self):
        '''
        Add R0+R0
        '''
        self.reg[0] += self.reg[0]
        print('adding', self.reg)
        self.pc += 3

    def CAL(self):
        '''
        1. The address of the ***instruction*** _directly after_ `CALL` is
        pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.

        '''
        val = self.pc + 2
        reg = self.ram[self.pc+1]
        sub_routine = self.reg[reg]

        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = val

        self.pc = sub_routine
        # print(self.reg[0])

    def RET(self):
        '''
        Return from subroutine 
        Pop the value from the top of the stack and store it in the PC
        '''
        returning = self.reg[self.sp]
        self.pc = self.ram[returning]

        self.reg[self.sp] += 1

    def POP(self):
        '''
        1. Copy the value from the address pointed to by `SP` to the given register.
        2. Increment `SP`.

        '''
        # grab the value from the top of the stack
        reg = self.ram[self.pc+1]
        val = self.ram[self.reg[self.sp]]
        # copy the value from the address pointed to be sp to the given register
        self.reg[reg] = val
        # increment sp
        self.reg[self.sp] += 1
        self.pc += 2

    def PSH(self):
        '''
        1. Decrement the `SP`.
        2. Copy the value in the given register to the address pointed to by

        '''
        # grab the register argument
        reg = self.ram[self.pc+1]
        val = self.reg[reg]
        # decrement the SP
        self.reg[self.sp] -= 1
        # copy the value in the given register to the address pointed to by sp
        self.ram[self.reg[self.sp]] = val
        self.pc += 2

    def HLT(self):
        print('reg: ', c.reg)
        print('memory: ', c.ram)

        print('bye, bye')
        sys.exit(0)

    def LDI(self):
        '''
        Set the value of a register to an integer.
        '''
        register = self.ram[self.pc+1]
        num = self.ram[self.pc+2]

        self.reg[register] = num
        self.pc += 3

    def PRN(self):
        # print numeric value stored in the given register
        print(f'reg[0]: {self.reg[0]}')
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
print(c.ram)
c.run()
