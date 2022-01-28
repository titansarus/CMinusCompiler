from .symbol import Symbol
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .codegen import CodeGen

class SymbolTable:
    def __init__(self, codegen: "CodeGen"):
        self.symbols = []
        self.codegen = codegen

    def find_address(self, lexeme):
        address = -1
        for symbol in self.symbols:
            if symbol.lexeme == lexeme:
                address = symbol.address
        if address == -1:
            address = self.codegen.get_next_data_address()
            symbol = self.add_symbol(lexeme=lexeme, address=address)
        return address

    def add_symbol(self, lexeme, address):
        symbol = Symbol(lexeme=lexeme, address=address)
        self.symbols.append(symbol)
        return symbol