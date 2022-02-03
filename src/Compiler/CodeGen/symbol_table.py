from .symbol import Symbol
from ..Constants.constants import *
from .semantic_exception import SemanticException
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .codegen import CodeGen

class SymbolTable:
    def __init__(self, codegen: "CodeGen"):
        self.scopes = [[]]
        self.codegen = codegen

    def find_address(self, lexeme, check_declaration=False, force_declaration=False):
        return self.find_symbol(lexeme, check_declaration, force_declaration).address

    def find_symbol(self, lexeme, check_declaration=False, force_declaration=False):
        address = -1
        result_symbol = None
        if not force_declaration:
            for scope in reversed(self.scopes):
                for symbol in scope:
                    if symbol.lexeme == lexeme:
                        address = symbol.address
                        result_symbol = symbol
                        break
                if result_symbol:
                    break
        if address == -1:
            if check_declaration:
                raise SemanticException(SCOPE_SEMANTIC_ERROR.format(lexeme))
            address = self.codegen.get_next_data_address()
            result_symbol = self.add_symbol(lexeme=lexeme, address=address)
        return result_symbol

    def find_symbol_by_address(self, address):
        result_symbol = None
        for scope in self.scopes[::-1]:
            for symbol in scope:
                if symbol.address == address:
                    result_symbol = symbol
                    break
        return result_symbol

    def add_symbol(self, lexeme, address):
        symbol = Symbol(lexeme=lexeme, address=address)
        self.scopes[-1].append(symbol)
        return symbol

    def remove_symbol(self, lexeme):
        i = 0
        is_found = False
        for symbol in self.scopes[-1]:
            if symbol.lexeme == lexeme:
                is_found = True
                break
            i += 1
        if is_found:
            self.scopes[-1].pop(i)
