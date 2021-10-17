class LexerFileWriter():
    def __init__(self, tokens: dict, lexical_errors: dict, symbol_table: dict, token_filename="tokens.txt",
                 lexical_error_filename="lexical_errors.txt", symbol_table_filename="symbol_table.txt"):
        self.tokens = tokens
        self.lexical_errors = lexical_errors
        self.symbol_table = symbol_table
        self.token_filename = token_filename
        self.lexical_error_filename = lexical_error_filename
        self.symbol_table_filename = symbol_table_filename

    def write_token_file(self):
        output_string = ""
        with open(self.token_filename, 'w') as f:
            for k in sorted(self.tokens.keys()):
                output_string += f"{k}.\t{self.tokens[k]}\n"
            f.write(output_string)

    def write_lexical_errors_file(self):
        output_string = ""
        with open(self.lexical_error_filename, 'w') as f:
            if self.lexical_errors:
                for k in sorted(self.lexical_errors.keys()):
                    output_string += f"{k}.\t{self.lexical_errors[k]}\n"
            else:
                output_string = "There is no lexical error."
            f.write(output_string)

    def write_symbol_table_file(self):
        output_string = ""
        with open(self.symbol_table_filename, 'w') as f:
            for k in sorted(self.symbol_table.keys()):
                output_string += f"{k}.\t{self.symbol_table[k]}\n"
            f.write(output_string)
