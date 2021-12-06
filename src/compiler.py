import states
from lexer import Lexer
from lexer_output_generator import *
from lexer_file_writer import *
# from cminus_parser import Parser

if __name__ == '__main__':
    states.initialize_states()
    lexer = Lexer()
    # parser = Parser()

    all_tokens = {}

    while True:
        token = lexer.get_next_token()
        print(token)
        if token == None:
            break
        if token.lineno not in all_tokens.keys():
            all_tokens[token.lineno] = []
        token_type = token.token_type
        token_lexeme = token.lexeme
        all_tokens[token.lineno].append((token_type, token_lexeme))
        if not token.must_continue:
            break

    tokens, lexical_errors, symbol_table = LexerOutputGenerator.generate_final_outputs(all_tokens)
    writer = LexerFileWriter(tokens=tokens, lexical_errors=lexical_errors, symbol_table=symbol_table)
    writer.write_token_file()
    writer.write_lexical_errors_file()
    writer.write_symbol_table_file()
