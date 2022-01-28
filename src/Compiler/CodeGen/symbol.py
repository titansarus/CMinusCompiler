class Symbol:
    def __init__(self, address = None, lexeme = None, symbol_type = None, size = 0, param_count = 0):
        self.address = address
        self.lexeme = lexeme
        self.symbol_type = symbol_type
        self.size = size
        self.param_count = param_count
