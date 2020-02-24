import sys

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4  # save a value to a register
PRINT_REGISTER = 5  # Print the value in a register
ADD = 6  # add 2 registers, store the result in the 1st reg

memory = [
    PRINT_BEEJ,
    SAVE,  # SAVE 65 in R2
    65,
    2,
    SAVE,  # save 20 in R3
    20,
    3,
    SAVE,  # R2 += R3
    ADD,
    2,
    3,
    PRINT_REGISTER,  # print R2 (85)
    2,
    HALT
]
register = [0] * 8

pc = 0  # Program counter

while True:
    command = memory[pc]

    if command == PRINT_BEEJ:
        # print beef
        print('beej!')
        pc += 1
    elif command == HALT:
        # print halt
        sys.exit(0)
    elif command == PRINT_NUM:
        # print num
        num = memory[pc + 1]
        pc += 2
        print(num)
    elif command == SAVE:
        # save a value to a register
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        # print the value in register
        reg = memory[pc+1]
        print(register[reg])
        pc += 2
    elif command == ADD:
        # add 2 register, sotre the results in 1sr reg
        reg_a = memory[pc+1]
        reg_b = memory[pc+2]
        register[reg_a] += register[reg_b]
        pc += 3
    else:
        print('I did not understand that command')
