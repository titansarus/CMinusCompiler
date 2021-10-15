import states
from constants import *
from BufferedReader import *


# TODO EMPTY FILE

class Lexer:
    def __init__(self, filename="input.txt"):
        self.reader = BufferedReader(filename)
        self.lines = {}
        self.curr_lineno = 0
        self.curr_line = None
        self.char_index = 0
        pass

    def get_next_token2(self):
        curr_state: states.State = states.State.states[0]
        lexeme = ""
        start_line = self.curr_lineno + 1

        while True:
            character, must_continue = self.reader.next_char()
            if character == '\n' or not must_continue:
                self.curr_lineno += 1
            lexeme += character
            try:
                curr_state = curr_state.get_next_state(character)
            except KeyError:
                return self.panic_mode(curr_state, lexeme, must_continue, start_line)
            if curr_state.is_accept_state:
                break
            if not must_continue:
                lexeme += '\n'  # TODO \n at end of wrong comment
                curr_state = curr_state.get_next_state('\n')
            if curr_state.is_accept_state:
                break
            if not must_continue:
                if not curr_state == states.State.states[0]:
                    return self.panic_mode(curr_state, lexeme, must_continue, start_line)
                    # return start_line, 'panic', lexeme, must_continue
                break

        if curr_state.is_retreat:
            lexeme = lexeme[:-1]
            if character == '\n':
                self.curr_lineno -= 1
            self.reader.retreat()
            must_continue = True

        token_type = Lexer.get_token_type(curr_state.token_type, lexeme)
        return start_line, token_type, lexeme, must_continue

    def panic_mode(self, curr_state, lexeme, must_continue, start_line):
        panic_state = PANIC_INVALID_INPUT
        if curr_state.token_type == NUM:
            panic_state = PANIC_INVALID_NUMBER
        if curr_state.token_type == COMMENT:
            if lexeme.startswith('/*'):
                panic_state = PANIC_UNCLOSED_COMMENT
        if curr_state.token_type == SYMBOL:
            if lexeme.startswith('*/'):
                panic_state = PANIC_UNMATCHED_COMMENT
        return start_line, panic_state, lexeme, must_continue

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
