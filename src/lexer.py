import states
from constants import *
from BufferedReader import *


# TODO EMPTY FILE

class Lexer:
    def __init__(self, filename="input.txt"):
        self.reader = BufferedReader(filename)
        self.lines = {}
        self.curr_lineno = 1
        self.curr_line = None
        self.char_index = 0
        pass

    def get_next_token(self):
        curr_state: states.State = states.State.states[0]
        lexeme = ""
        start_line = self.curr_lineno
        is_eof_step = False

        while True:
            character, must_continue = self.reader.next_char()
            if character == "":
                return None
            if character == '\n':
                self.curr_lineno += 1
            lexeme += character
            try:
                curr_state = curr_state.get_next_state(character)
            except KeyError:
                return self.panic_mode(curr_state, lexeme, must_continue, start_line)
            if curr_state.is_panic_state or curr_state.is_accept_state:
                break
            if not must_continue:
                try:
                    curr_state = curr_state.get_next_state(FINISH)
                    is_eof_step = True
                    break
                except KeyError:
                    return self.panic_mode(curr_state, lexeme, must_continue, start_line)

        if curr_state.is_retreat:
            if not is_eof_step:
                lexeme = lexeme[:-1]
            if character == '\n':
                self.curr_lineno -= 1
            self.reader.retreat()
        
        if (not curr_state.is_accept_state and not must_continue and not curr_state == states.State.states[0]) or curr_state.is_panic_state:
            return self.panic_mode(curr_state, lexeme, must_continue, start_line)

        return self.final_return(curr_state, lexeme, must_continue, start_line)

    def final_return(self, curr_state, lexeme, must_continue, start_line, panic_state=None):
        token_type = Lexer.get_token_type(curr_state.token_type, lexeme)
        return start_line, (panic_state if panic_state else token_type), lexeme, must_continue

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
        if lexeme[-1] in whitespace:
            lexeme = lexeme[:-1]
        return self.final_return(curr_state, lexeme, must_continue, start_line, panic_state)

    @staticmethod
    def get_token_type(token_type, lexeme):
        if token_type != KEYWORD_ID:
            return token_type
        else:
            if lexeme in keywords:
                return KEYWORD
            return ID
