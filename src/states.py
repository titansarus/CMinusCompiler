from constants import *


class State:
    states = {}

    def __init__(self, id, token_type=START, is_accept_state=False, is_retreat=False, is_panic_state=False):
        self.id = id
        self.transitions = {}
        self.token_type = token_type
        self.is_accept_state = is_accept_state
        self.is_retreat = is_retreat
        self.is_panic_state = is_panic_state
        State.states[id] = self

    def add_transition(self, dest_state, character):
        self.transitions[character] = dest_state

    def get_next_state(self, character):
        return self.transitions[character]


def add_eof_transition(src_state: State, dest_state: State):
    src_state.transitions[FINISH] = dest_state


def add_transitions(src_state: State, dest_state: State, character_lists, negate=False):
    if negate:
        valid_characters = all_valid
        for character_list in character_lists:
            valid_characters = valid_characters.replace(character_list, "")
        valid_characters = [valid_characters]
    else:
        valid_characters = character_lists

    for character_list in valid_characters:
        for c in character_list:
            src_state.add_transition(dest_state, c)


def initialize_keyword_states(start_state):
    state_1 = State(1, KEYWORD_ID)
    state_2 = State(2, KEYWORD_ID, is_accept_state=True, is_retreat=True)

    add_transitions(start_state, state_1, [letters])
    add_transitions(state_1, state_1, [letters, digits])
    add_transitions(state_1, state_2, [letters, digits], negate=True)
    add_eof_transition(state_1, state_2)


def initialize_num_states(start_state):
    state_3 = State(3, NUM)
    state_4 = State(4, NUM, True, True)

    add_transitions(start_state, state_3, [digits])
    add_transitions(state_3, state_3, [digits])
    add_transitions(state_3, state_4, [digits , letters], negate=True)
    add_eof_transition(state_3, state_4)


def initialize_symbol_states(start_state):
    state_5 = State(5, SYMBOL, is_accept_state=True, is_retreat=False)
    state_6 = State(6, SYMBOL, is_accept_state=False, is_retreat=False)
    state_7 = State(7, SYMBOL, is_accept_state=True, is_retreat=False)
    state_8 = State(8, SYMBOL, is_accept_state=False, is_retreat=False)
    state_9 = State(9, SYMBOL, is_accept_state=True, is_retreat=True)

    add_transitions(start_state, state_5, [symbol.replace("*", "").replace("=", "")])
    add_transitions(start_state, state_6, ["="])
    add_transitions(state_6, state_7, ["="])
    add_transitions(state_6, state_9, ["="], negate=True)
    add_transitions(start_state, state_8, ["*"])
    add_transitions(state_8, state_9, ["/"], True)
    add_eof_transition(state_6, state_9)
    add_eof_transition(state_8, state_9)


def initialize_comment_states(start_state):
    state_10 = State(10, COMMENT, is_accept_state=False, is_retreat=False)
    state_11 = State(11, COMMENT, is_accept_state=False, is_retreat=False)
    state_12 = State(12, COMMENT, is_accept_state=True, is_retreat=False)
    state_13 = State(13, COMMENT, is_accept_state=False, is_retreat=False)
    state_14 = State(14, COMMENT, is_accept_state=False, is_retreat=False)
    lone_slash_state = State(16, KEYWORD_ID, is_accept_state=False, is_retreat=True, is_panic_state=True)

    add_transitions(start_state, state_10, ['/'])
    add_transitions(state_10, state_11, ['/'])
    add_transitions(state_11, state_11, [all_characters.replace('\n', "")])
    add_transitions(state_11, state_12, ['\n'])
    add_eof_transition(state_11, state_12)
    add_transitions(state_10, state_13, ['*'])
    add_transitions(state_13, state_13, [all_characters.replace('*', "")])
    add_transitions(state_13, state_14, ['*'])
    add_transitions(state_14, state_14, ['*'])
    add_transitions(state_14, state_12, ['/'])
    add_transitions(state_14, state_13, [all_characters.replace('*', "").replace('/', "")])
    add_transitions(state_10, lone_slash_state, ['/', '*'], negate=True)


def initialize_whitespace_states(start_state):
    state_15 = State(15, WHITESPACE, is_accept_state=True, is_retreat=False)
    add_transitions(start_state, state_15, [whitespace])


def initialize_states():
    start_state = State(0, START)
    initialize_keyword_states(start_state)
    initialize_num_states(start_state)
    initialize_symbol_states(start_state)
    initialize_comment_states(start_state)
    initialize_whitespace_states(start_state)
