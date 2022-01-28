# runtime memory: 
#   0 - 999 for code
#   1000 - 5000 for data
#   5000 - inf for temp

from ..Constants.constants import *
from instructions import *
from codegen import CodeGen

class RuntimeStack:
    def __init__(self, codegen: CodeGen, sp_address = 1000):
        self.sp_address = sp_address
        self.codegen = codegen

    def push(self, data):
        # SP shows last full cell
        instructions = [
            Sub(self.sp_address, f"#{WORD_SIZE}", self.sp_address),
            Assign(data, f"@{self.sp_address}"),
        ]
        self.codegen.push_instructions(instructions)

    def pop(self, address):
        instructions = [
            Assign(f"@{self.sp_address}", address),
            Add(self.sp_address, f"#{WORD_SIZE}", self.sp_address),
        ]
        self.codegen.push_instructions(instructions)
