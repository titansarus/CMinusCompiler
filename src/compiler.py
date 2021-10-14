import states
from lexer import Lexer
if __name__ == '__main__':
    states.initialize_states()
    lexer = Lexer()

    all_tokens = {}
    line_tokens = []
    while True:

        token = lexer.get_next_token()
        if not token:
            break
        line_tokens.append(token)
        if token[1] == '\n':
            all_tokens[lexer.curr_lineno]=line_tokens
            line_tokens=[]

    print (all_tokens)


