#!/usr/bin/env python3

class CPU:
    def __init__(self):
        self.register = [0] * 8
        self.memory = [0] * 256
        self.pc = 0

    def ram_read(self, MAR): # MAR = Memory Address Register
        return self.memory[MAR]
    
    def raw_write(self, MAR, MDR): #MDR = Memory Data Register
        self.memory[MAR] = MDR



import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()