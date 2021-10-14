import states
from constants import *


class Lexer:
    def __init__(self, filename="input.txt"):
        self.filename = filename
        self.file = open(filename, 'r')
        self.lines = {}
        self.curr_lineno = 0
        self.curr_line = None
        self.char_index = 0
        pass

    def get_next_token(self):
        if self.curr_line is None or len(self.curr_line) == self.char_index:
            self.curr_lineno += 1
            self.char_index = 0
            self.curr_line = self.file.readline()
            if not self.curr_line:
                return None
            if self.curr_line[-1] != '\n':
                self.curr_line += '\n'

        curr_state: states.State = states.State.states[0]
        lexeme = ""
        while not curr_state.is_accept_state and len(self.curr_line) > self.char_index:
            next_char = self.curr_line[self.char_index]
            self.char_index += 1
            lexeme += next_char
            curr_state = curr_state.get_next_state(next_char)
        if curr_state.is_retreat:
            lexeme = lexeme[:-1]
            self.char_index -= 1
        token_type = Lexer.get_token_type(curr_state.token_type, lexeme)
        return token_type, lexeme

    @staticmethod
    def get_token_type(token_type, lexeme):
        if token_type != KEYWORD_ID:
            return token_type
        else:
            if lexeme in keywords:
                return KEYWORD
            return ID
