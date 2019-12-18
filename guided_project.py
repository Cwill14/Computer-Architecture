import sys

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3 # like LDI
PRINT_REG = 4 #like PRN

# memory = [
#     PRINT_BEEJ,
#     SAVE_REG,
#     0,
#     256,
#     PRINT_REG,
#     0,
#     PRINT_BEEJ,
#     HALT
# ]
memory = [0] * 256

registers = [0] * 8
filename = sys.argv[1]

# read the file
address = 0

with open(filename) as f:
    for line in f:
        # print(line, end="")
        n = line.split("#")
        n[0] = n[0].strip()
        if n[0] == '':
            continue
        val = int(n[0])
        memory[address] = val
        address += 1

running = True
pc = 0 # Program Counter, index into memory of the current instruction

while running:
    current_instruction = memory[pc]

    if current_instruction == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    
    elif current_instruction == HALT:
        running = False
        pc += 1
    
    elif current_instruction == SAVE_REG:
        reg_num = memory[pc + 1] # operand A
        value = memory[pc + 2] # operand B
        registers[reg_num] = value
        pc += 3

    elif current_instruction == PRINT_REG:
        reg_num = memory[pc + 1] # operand A
        print(registers[reg_num])
        pc += 2

    else:
        print(f"unknown instruction at address {pc}")
