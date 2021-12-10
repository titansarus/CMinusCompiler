from ..Constants.constants import *

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

    @staticmethod
    def generate_lexical_errors(token_lines: dict):
        lexical_errors = {}
        for lineno, token_list in token_lines.items():
            lexical_error_list = []
            for token in token_list:
                if token[0] in PANIC_STATES:
                    lexical_error_list.append(
                        f"({token[1] if len(token[1]) <= 7 or token[0] != PANIC_UNCLOSED_COMMENT else token[1][:7] + '...'}, {token[0]})")
            if lexical_error_list:
                lexical_errors[lineno] = " ".join(lexical_error_list) + " "
        return lexical_errors

    @staticmethod
    def generate_tokens(token_lines: dict):
        tokens = {}
        for lineno, token_list in token_lines.items():
            token_string_list = []
            for token in token_list:
                if token[0] not in [WHITESPACE, COMMENT] + PANIC_STATES:
                    token_string_list.append(f"({token[0]}, {token[1]})")
            if token_string_list:
                tokens[lineno] = " ".join(token_string_list) + " "
        return tokens

    @staticmethod
    def generate_final_outputs(token_lines: dict):
        symbol_table = LexerOutputGenerator.generate_symbol_table(token_lines)
        lexical_errors = LexerOutputGenerator.generate_lexical_errors(token_lines)
        tokens = LexerOutputGenerator.generate_tokens(token_lines)
        return tokens, lexical_errors, symbol_table
