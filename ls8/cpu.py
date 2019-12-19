"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        # regular registers
        self.reg = [0] * 8
        # adds 256 bits of storage
        self.reg.append(0xf4)
        # internal registers
        self.pc = 0 # program counter, address of the currently executing instruction
        # self.ir = 0 # instruction register, contains a copy of the currently exexcuting instruction
        # self.mar = 0 # memory address register, holds the memory address we're reading or writing
        # self.mdr = 0 # memory data register, holds the value to write or the value just read
        self.fl = 0 # flags register, holds the current flags status. thest flags can change based on the operands given to the CMP opcode
        self.sp = 8

        self.instructions = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100000: self.ADD,
            0b10100001: self.SUB,
            0b10100010: self.MUL,
            # 0b10100011: self.DIV
            # 0b10100100: self.MOD,
            0b01000101: self.PUSH,
            0b01000110: self.POP
        }

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
            self.reg[reg_a] %= 0b100000000
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.reg[reg_a] %= 0b100000000
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.reg[reg_a] %= 0b100000000
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

    def load_ops(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.pc += 2
        return op_a, op_b

    def LDI(self):
        op_a, op_b = self.load_ops()
        self.reg[op_a] = op_b

    def PRN(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 1

    def ADD(self):
        op_a, op_b = self.load_ops()
        self.alu("ADD", op_a, op_b)
    
    def SUB(self):
        op_a, op_b = self.load_ops()
        self.alu("SUB", op_a, op_b)

    def MUL(self):
        op_a, op_b = self.load_ops()
        self.alu("MUL", op_a, op_b)

    # def PUSH(self):
    #     self.reg[self.sp] -= 1
    #     self.pc += 1
    #     new_reg = self.ram_read(self.pc)
    #     self.ram_write(self.reg[self.sp], self.reg[new_reg])
    def PUSH(self):
        self.reg[self.sp]-=1
        self.pc+=1
        reg = self.ram_read(self.pc)
        self.ram_write(self.reg[self.sp], self.reg[reg])

    def POP(self):
        self.pc += 1
        register = self.ram_read(self.pc)
        data = self.ram_read(self.reg[self.sp])
        self.reg[register] = data
        self.reg[self.sp] += 1

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
