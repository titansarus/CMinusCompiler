from ..Lexer.cminus_token import Token
from .symbol_table import SymbolTable
from .symbol import Symbol
from .instructions import *
from ..Constants.constants import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .codegen import CodeGen

class ActionManager:
    def __init__(self, codegen: "CodeGen", symbol_table: SymbolTable):
        self.codegen = codegen
        self.symbol_table = symbol_table
        self.argument_counts = []
        self.no_push_flag = False
        self.check_declaration_flag = False
        self.function_scope_flag = False
        self.breaks = []

    def pid(self, previous_token: Token, current_token: Token):
        address = self.symbol_table.find_address(previous_token.lexeme, self.check_declaration_flag)
        if not self.no_push_flag:
            self.codegen.semantic_stack.append(address)
        if self.argument_counts:
            self.argument_counts[-1] += 1
    
    def pnum(self, previous_token: Token, current_token: Token):
        num = f"#{previous_token.lexeme}"
        if not self.no_push_flag:
            self.codegen.semantic_stack.append(num)
        if self.argument_counts:
            self.argument_counts[-1] += 1

    def label(self, previous_token: Token, current_token: Token):
        self.codegen.semantic_stack.append(self.codegen.i)

    def save(self, previous_token: Token, current_token: Token):
        self.codegen.semantic_stack.append(self.codegen.i)
        self.codegen.i += 1

    def push_operation(self, previous_token: Token, current_token: Token):
        self.codegen.semantic_stack.append(previous_token.lexeme)

    def execute(self, previous_token: Token, current_token: Token):
        temp_address = self.codegen.get_next_temp_address()
        operand2 = self.codegen.semantic_stack.pop()
        operation = self.codegen.semantic_stack.pop()
        operand1 = self.codegen.semantic_stack.pop()
        self.codegen.semantic_stack.append(temp_address)
        operation_to_instruction = {
            "+": Add,
            "-": Sub,
            "<": LT,
            "==": Eq,
            "*": Mult,
        }
        instruction = operation_to_instruction[operation](operand1, operand2, temp_address)
        self.codegen.push_instruction(instruction)

    def start_argument_list(self, previous_token: Token, current_token: Token):
        self.argument_counts.append(0)

    def end_argument_list(self, previous_token: Token, current_token: Token):
        arg_count = self.argument_counts.pop()
        for i in range(arg_count):
            data = self.codegen.semantic_stack.pop()
            self.codegen.runtime_stack.push(data)

    def jp_from_saved(self, previous_token: Token, current_token: Token):
        instruction = JP(self.codegen.i)
        destination = self.codegen.semantic_stack.pop()
        self.codegen.insert_instruction(instruction, destination)

    def jpf_from_saved(self, previous_token: Token, current_token: Token):
        destination = self.codegen.semantic_stack.pop()
        condition = self.codegen.semantic_stack.pop()
        instruction = JPF(condition, self.codegen.i)
        self.codegen.insert_instruction(instruction, destination)
    
    def save_and_jpf_from_last_save(self, previous_token: Token, current_token: Token):
        destination = self.codegen.semantic_stack.pop()
        condition = self.codegen.semantic_stack.pop()
        instruction = JPF(condition, self.codegen.i + 1)
        self.codegen.insert_instruction(instruction, destination)
        self.codegen.semantic_stack.append(self.codegen.i)
        self.codegen.i += 1
    
    def assign(self, previous_token: Token, current_token: Token):
        value = self.codegen.semantic_stack.pop()
        address = self.codegen.semantic_stack.pop()
        instruction = Assign(value, address)
        self.codegen.push_instruction(instruction)
        self.codegen.semantic_stack.append(value)

    def start_no_push(self, previous_token: Token, current_token: Token):
        self.no_push_flag = True

    def end_no_push(self, previous_token: Token, current_token: Token):
        self.no_push_flag = False

    def declare_array(self, previous_token: Token, current_token: Token):
        # use [1:] to skip the '#'
        length = int(self.codegen.semantic_stack.pop()[1:])
        size = (length - 1) * WORD_SIZE
        self.codegen.get_next_data_address(size = size)

    def array(self, previous_token: Token, current_token: Token):
        offset = self.codegen.semantic_stack.pop()
        temp = self.codegen.get_next_temp_address()
        array_start = self.codegen.semantic_stack.pop()
        instructions = [
            Mult(offset, f"#{WORD_SIZE}", temp),
            Add(temp, f"#{array_start}", temp),
        ]
        self.codegen.push_instructions(instructions)
        self.codegen.semantic_stack.append(f"@{temp}")
        
    def until(self, previous_token: Token, current_token: Token):
        condition = self.codegen.semantic_stack.pop()
        destination = self.codegen.semantic_stack.pop()
        instruction = JPF(condition, destination)
        self.codegen.push_instruction(instruction)

    def add_break(self, previous_token: Token, current_token: Token):
        self.breaks.append(self.codegen.i)
        self.codegen.i += 1

    def handle_breaks(self, previous_token: Token, current_token: Token):
        for destination in self.breaks:
            instruction = JP(self.codegen.i)
            self.codegen.insert_instruction(instruction, destination)

    def pop(self, previous_token: Token, current_token: Token):
        self.codegen.semantic_stack.pop()

    def check_declaration(self, previous_token: Token, current_token: Token):
        self.check_declaration_flag = True

    def uncheck_declaration(self, previous_token: Token, current_token: Token):
        self.check_declaration_flag = False

    def declare_function(self, previous_token: Token, current_token: Token):
        pass

    def set_function_scope_flag(self, previous_token: Token, current_token: Token):
        self.function_scope_flag = True

    def open_scope(self, previous_token: Token, current_token: Token):
        if not self.function_scope_flag:
            self.codegen.symbol_table.scopes.append([])
        self.function_scope_flag = False
        self.codegen.data_and_temp_stack.append((self.codegen.data_address, self.codegen.temp_address))

    def close_scope(self, previous_token: Token, current_token: Token):
        self.codegen.symbol_table.scopes.pop()
        self.codegen.data_address, self.codegen.temp_address = self.codegen.data_and_temp_stack.pop()
    
    def pop_param(self, previous_token: Token, current_token: Token):
        address = self.codegen.semantic_stack.pop()
        self.codegen.runtime_stack.pop(address)

    def declare_function(self, previous_token: Token, current_token: Token):
        symbol: Symbol = self.codegen.symbol_table.scopes[-1][-1]
        symbol.address = f"#{self.codegen.i}"
        self.codegen.function_data_start_pointer = self.codegen.data_address
        self.codegen.function_temp_start_pointer = self.codegen.temp_address

    def call(self, previous_token: Token, current_token: Token):
        for address in range(self.codegen.function_data_start_pointer, self.codegen.data_address, WORD_SIZE):
            self.codegen.runtime_stack.push(address)
        for address in range(self.codegen.function_temp_start_pointer, self.codegen.temp_address, WORD_SIZE):
            self.codegen.runtime_stack.push(address)
        self.codegen.register_file.push_registers()
        
        self.codegen.register_file.save_return_address()

        address = self.codegen.semantic_stack.pop()
        instruction = JP(address)
        self.codegen.push_instruction(instruction)

        self.codegen.register_file.pop_registers()
        for address in range(self.codegen.temp_address - WORD_SIZE, self.codegen.function_temp_start_pointer, -WORD_SIZE):
            self.codegen.runtime_stack.pop(address)
        for address in range(self.codegen.data_address - WORD_SIZE, self.codegen.function_data_start_pointer, -WORD_SIZE):
            self.codegen.runtime_stack.pop(address)
    
    def set_return_value(self, previous_token: Token, current_token: Token):
        value = self.codegen.semantic_stack.pop()
        self.codegen.register_file.save_return_value(value)

    def jump_back(self, previous_token: Token, current_token: Token):
        instruction = JP(self.codegen.register_file.return_address_register_address)
        self.codegen.push_instruction(instruction)