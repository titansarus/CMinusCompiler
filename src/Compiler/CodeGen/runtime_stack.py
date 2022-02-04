from ..Constants.constants import *
from .instructions import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .codegen import CodeGen
    from .register_file import RegisterFile


class RuntimeStack:
    def __init__(self, codegen: "CodeGen", register_file: "RegisterFile"):
        self.codegen = codegen
        self.register_file = register_file

    def push(self, data):
        # SP shows last full cell
        instructions = [
            Sub(self.register_file.stack_pointer_register_address, f"#{WORD_SIZE}",
                self.register_file.stack_pointer_register_address),
            Assign(data, f"@{self.register_file.stack_pointer_register_address}"),
        ]
        self.codegen.push_instructions(instructions)

    def pop(self, address):
        instructions = [
            Assign(f"@{self.register_file.stack_pointer_register_address}", address),
            Add(self.register_file.stack_pointer_register_address, f"#{WORD_SIZE}",
                self.register_file.stack_pointer_register_address),
        ]
        self.codegen.push_instructions(instructions)
