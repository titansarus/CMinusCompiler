from .instructions import *
from ..Constants.constants import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .codegen import CodeGen

class RegisterFile:
    def __init__(self, codegen: "CodeGen"):
        self.codegen = codegen
        self.return_address_register_address = self.codegen.get_next_data_address()
        self.return_value_register_address = self.codegen.get_next_data_address()
        self.stack_pointer_register_address = self.codegen.get_next_data_address()

    def save_return_address(self, arg_count):
        self.codegen.push_instruction(Assign(f"#{self.codegen.i + arg_count * STACK_PUSH_INSTRUCTION_COUNT + 2}", self.return_address_register_address))

    def save_return_value(self, value):
        self.codegen.push_instruction(Assign(value, self.return_value_register_address))

    def push_registers(self):
        self.codegen.runtime_stack.push(self.return_address_register_address)
        # self.codegen.runtime_stack.push(self.return_value_register_address)
        self.codegen.runtime_stack.push(self.stack_pointer_register_address)

    def pop_registers(self):
        self.codegen.runtime_stack.pop(self.stack_pointer_register_address)
        # self.codegen.runtime_stack.pop(self.return_value_register_address)
        self.codegen.runtime_stack.pop(self.return_address_register_address)