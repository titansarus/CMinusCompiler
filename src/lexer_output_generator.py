from constants import *


class LexerOutputGenerator:

    @staticmethod
    def generate_symbol_table(token_lines: dict):
        symbol_table = {}
        symbol_table_set = set()
        iterator = 1
        for word in keywords:
            symbol_table_set.add(word)
            symbol_table[iterator] = (word)
            iterator += 1

        for lineno, token_list in token_lines.items():
            for token in token_list:
                if token[0] == ID:
                    if token[1] not in symbol_table_set:
                        symbol_table_set.add(token[1])
                        symbol_table[iterator] = (token[1])
                        iterator += 1
        return symbol_table

    # TODO LEXICAL ERROR SIZE LIMIT
    @staticmethod
    def generate_final_outputs(token_lines: dict):
        symbol_table = LexerOutputGenerator.generate_symbol_table(token_lines)
        lexical_errors = {}
        tokens = {}
        for lineno, token_list in token_lines.items():
            lexical_error_list = []
            token_string_list = []
            for token in token_list:
                if token[0] in PANIC_STATES:
                    lexical_error_list.append(f"({token[1]}, {token[0]})")
                elif token[0] not in [WHITESPACE, COMMENT]:
                    token_string_list.append(f"({token[0]}, {token[1]})")
            if lexical_error_list:
                lexical_errors[lineno] = " ".join(lexical_error_list) + " "
            if token_string_list:
                tokens[lineno] = " ".join(token_string_list) + " "
        return tokens, lexical_errors, symbol_table
