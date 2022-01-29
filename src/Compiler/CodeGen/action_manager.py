from ..Lexer.cminus_token import Token
from .symbol_table import SymbolTable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .codegen import CodeGen

class ActionManager:
    def __init__(self, codegen: "CodeGen", symbol_table: SymbolTable):
        self.codegen = codegen
        self.symbol_table = symbol_table

    def pid(self, token: Token):
        address = self.symbol_table.find_address(token.lexeme)
        self.codegen.semantic_stack.append(address)
    
    def pnum(self, token: Token):
        self.codegen.semantic_stack.append(int(token.lexeme))