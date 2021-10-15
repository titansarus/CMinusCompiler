import states
from BufferedReader import *
from lexer import Lexer

if __name__ == '__main__':
    states.initialize_states()
    lexer = Lexer()

    all_tokens = {}

    while True:

        token = lexer.get_next_token2()
        if (token[0] not in all_tokens.keys()):
            all_tokens[token[0]] = []
        all_tokens[token[0]].append(token[1:3])
        if not token[3]:
            break

    print(all_tokens)
