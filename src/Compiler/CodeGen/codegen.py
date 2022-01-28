from instructions import *

class CodeGen:
    def __init__(self):
        self.program = []
        self.i = 0
        # self.scope_stack = [] TODO

    def check_program_size(self, size=self.i):
        while len(self.program) <= size:
            self.program.append(None)

    def push_instruction(self, instruction):
        self.check_program_size()
        self.program[self.i] = instruction.to_code()
        self.i += 1
    
    def save_space(self):
        self.i += 1

    def insert_instruction(self, instruction, destination):
        self.check_program_size(destination)
        self.program[destination] = instruction.to_code()

    def push_instructions(self, instructions):
        for instruction in instructions:
            self.push_instruction(instruction)