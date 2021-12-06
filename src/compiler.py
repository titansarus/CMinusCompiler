import states
from lexer import Lexer
from lexer_output_generator import *
from lexer_file_writer import *

if __name__ == '__main__':
    states.initialize_states()
    lexer = Lexer()

    all_tokens = {}

    while True:
        token = lexer.get_next_token()
        print(token)
        if token == None:
            break
        if token[0] not in all_tokens.keys():
            all_tokens[token[0]] = []
        token_type = token[1]
        token_lexeme = token[2]
        all_tokens[token[0]].append((token_type, token_lexeme))
        if not token[3]:
            break

    tokens, lexical_errors, symbol_table = LexerOutputGenerator.generate_final_outputs(all_tokens)
    writer = LexerFileWriter(tokens=tokens, lexical_errors=lexical_errors, symbol_table=symbol_table)
    writer.write_token_file()
    writer.write_lexical_errors_file()
    writer.write_symbol_table_file()
