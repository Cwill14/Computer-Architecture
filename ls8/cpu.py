"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        # regular registers
        self.reg = [0] * 8
        # internal registers
        self.pc = 0 # program counter, address of the currently executing instruction
        # self.ir = 0 # instruction register, contains a copy of the currently exexcuting instruction
        # self.mar = 0 # memory address register, holds the memory address we're reading or writing
        # self.mdr = 0 # memory data register, holds the value to write or the value just read
        self.fl = 0 # flags register, holds the current flags status. thest flags can change based on the operands given to the CMP opcode
        
        self.instructions = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
        }

        # clear pc everytime run cpu

    def load(self):
        """Load a program into memory."""
    
        address = 0
        program = []

        with open(sys.argv[1], 'r') as f:
            for line in f:
                x = line.find('#')
                if x >= 0:
                    line = line[:x]
                if len(line) > 1:
                    line = line.strip()
                    program.append(line)

        for instruction in program:
            self.ram[address] = int(instruction, 2)
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, write):
        self.ram[address] = write

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 2

    def PRN(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 1


    def run(self):
        """Run the CPU."""
        '''It needs to read the memory address that's stored in register PC, and store that result in IR, the Instruction Register. 
        This can just be a local variable in run().'''
        running = True

        while running:
            # ir = self.ram_read(self.pc)
            ir = self.ram[self.pc]
            # ^^ instruction register

            # HLT or halt
            if ir == 0b00000001:
                running = False
            else:
                self.instructions[ir]()
                self.pc += 1

            # LDI or save an integer
            # elif ir == 0b10000010:
            #     operand_a = self.ram_read(self.pc + 1)
            #     operand_b = self.ram_read(self.pc + 2)
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # # PRN or print register
            # elif ir == 0b01000111:
            #     print("self.ram_read(self.pc + 1) = ", self.ram_read(self.pc + 1))
            #     self.pc += 2
            # # elif ir == num:
            # #     pass
            # # elif ir == num:
            # #     pass
            # # elif ir == num:
            # #     pass
            # # elif ir == num:
            # #     pass
            # else:
            #     print(f"unknown instruction at address {self.pc}")