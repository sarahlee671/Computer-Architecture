"""CPU functionality."""

import sys

class CPU:
    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        #R7 is reserved as the SP
        self.SP = 7


    def ram_read(self, MAR): # MAR = Memory Address Register
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR): #MDR = Memory Data Register
        self.ram[MAR] = MDR

    def load(self, argv):
        """Load a program into memory."""

        try:
            address = 0
            with open(sys.argv[1]) as file: 
                for line in file:
                    # ignore everything after #
                    split_hashes = line.split("#")
                    # convert binary strings to integer values to store in RAM 
                    num = split_hashes[0].strip()
                    # (can use build-in int() function by specifying a number base as the second argument)
                    self.ram[address] = int(num, 2)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        running = True

        while running:
            
            IR = self.ram[self.pc]
            #register
            operand_a = self.ram_read(self.pc + 1)
            #value
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                running = False
                self.pc += 1

            elif IR == LDI:
                #set specificed register to a specified value
                # increment program counter
                self.reg[operand_a] = operand_b
                self.pc += 3
                
            elif IR == PRN:
                #print numberic value stored in the given register
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                #Decrement the SP
                self.reg[self.SP] -= 1
                #Copy the value in the given register to the address pointed to by SP
                self.ram[self.reg[self.SP]] = self.reg[operand_a]
                self.pc += 2

            elif IR == POP:
                #copy the value from the address pointed to by SP to the given register
                self.reg[operand_a] = self.ram[self.reg[self.SP]]
                #Increment SP
                self.reg[self.SP] += 1
                self.pc += 2
            else:
                print(f"Unknown instruction: {IR}")
                sys.exit(1)




