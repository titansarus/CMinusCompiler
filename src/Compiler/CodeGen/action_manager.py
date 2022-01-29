from ..Lexer.cminus_token import Token
from .symbol_table import SymbolTable
from .instructions import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .codegen import CodeGen

class ActionManager:
    def __init__(self, codegen: "CodeGen", symbol_table: SymbolTable):
        self.codegen = codegen
        self.symbol_table = symbol_table

    def pid(self, previous_token: Token, current_token: Token):
        address = self.symbol_table.find_address(previous_token.lexeme)
        self.codegen.semantic_stack.append(address)
    
    def pnum(self, previous_token: Token, current_token: Token):
        self.codegen.semantic_stack.append(f"#{previous_token.lexeme}")

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