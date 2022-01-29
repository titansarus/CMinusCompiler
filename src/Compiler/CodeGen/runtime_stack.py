from ..Constants.constants import *
from .instructions import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .codegen import CodeGen

class RuntimeStack:
    def __init__(self, codegen: "CodeGen"):
        self.codegen = codegen
        self.sp_address = codegen.get_next_data_address()

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
