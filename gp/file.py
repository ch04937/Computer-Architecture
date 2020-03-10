# take an argument, load the values from that file and put it in an array
import sys

print(sys.argv)

mem_pointer = 0
if len(sys.argv) != 2:
    print('ERROR: Must have a file name')
    sys.exit(1)
try:
    # open the file
    with open(sys.argv[1]) as f:

        # read all the lines
        for line in f:
            # parse out the comments
            comment_slit = line.strip().split('#')
            # cast the numbers from strings to ints
            value = comment_slit[0].split()
            # ignore balnk lines
            if value == '':
                continue

            num = int(value)
            memory[mem_pointer] = num
            mem_pointer += 1
            print(f'{num:08}: {num}')

except FileNotFoundError:
    print('File not found')
    sys.exit(2)

# populate a memory array
