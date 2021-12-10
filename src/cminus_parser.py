from constants import *
from productions import *
from lexer import Lexer
from cminus_token import Token

current_token = None
errors = []
file_ended = False

def get_next_valid_token(lexer: Lexer):
    token = lexer.get_next_token()
    skip_states = PANIC_STATES + [WHITESPACE, COMMENT]
    while token.token_type in skip_states:
        token = lexer.get_next_token()
    return token

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        global current_token, errors, file_ended
        errors = []
        file_ended = False
        current_token = get_next_valid_token(self.lexer)
        root_parser = ProductionParser(Program, self.lexer)
        root = root_parser.parse()
        return root, errors


class ParseNode:
    def __init__(self, production=Program, label="Program", parent=None):
        self.production = production
        self.label = label
        self.parent = parent
        self.children = []
    def add_child(self, child: "ParseNode"):
        child.parent = self
        self.children.append(child)
    def get_name(self):
        if type(self.production) == str:
            return self.production
        return self.production.name

class ProductionParser:
    def __init__(self, production: Production, lexer: Lexer):
        self.production = production
        self.lexer = lexer
        self.current_state = None
        self.errors = []
        if type(production) == Production:
            self.current_state = parser_states_dict[production]
    def parse(self):
        global current_token, errors, file_ended
        if self.current_state == None:
            if current_token.token_type == END_TOKEN:
                node = ParseNode(self.production, self.production)
            else:
                node = ParseNode(f'({current_token.token_type}, {current_token.lexeme})', f'({current_token.token_type}, {current_token.lexeme})')
            current_token = get_next_valid_token(self.lexer)
            return node
        current_node = ParseNode(self.production, label=self.production.name)
        while not self.current_state.is_final:
            epsilon_state = None
            error_edge = None
            is_nonterminal_missing = False
            is_token_illegal = False
            is_NUM_or_ID_missing = False
            is_KEYWORD_or_SYMBOL_missing = False
            for edge in self.current_state.edges:
                is_in_first = False
                is_in_follow = False
                if edge.edge_type == PRODUCTION_PARSER_EDGE:
                    is_in_first = current_token.lexeme in edge.label.first or current_token.token_type in edge.label.first
                    is_in_follow = current_token.lexeme in edge.label.follow or current_token.token_type in edge.label.follow
                is_valid_NUM_or_ID = edge.edge_type == NUM_ID_PARSER_EDGE and current_token.token_type == edge.label
                is_valid_KEYWORD_or_SYMBOL = edge.edge_type == KEYWORD_SYMBOL_PARSER_EDGE and current_token.lexeme == edge.label
                is_valid_Nonterminal = edge.edge_type == PRODUCTION_PARSER_EDGE and is_in_first
                is_valid_epsilon_nonterminal = edge.edge_type == PRODUCTION_PARSER_EDGE and edge.label.first_has_epsilon and is_in_follow
                if is_valid_NUM_or_ID or is_valid_KEYWORD_or_SYMBOL:
                    epsilon_state = None
                    # print(self.current_state.ID, current_token.lexeme)
                    next_node = ProductionParser(edge.label, self.lexer).parse()
                    current_node.add_child(next_node)
                    if file_ended:
                        return current_node
                    self.current_state = edge.destination
                    error_edge = None
                    break
                elif is_valid_Nonterminal or is_valid_epsilon_nonterminal:
                    epsilon_state = None
                    # print(self.current_state.ID, current_token.lexeme)
                    next_node = ProductionParser(edge.label, self.lexer).parse()
                    current_node.add_child(next_node)
                    if file_ended:
                        return current_node
                    self.current_state = edge.destination
                    error_edge = None
                    break
                elif edge.edge_type == EPSILON_PARSER_EDGE:
                    epsilon_state = edge.destination
                else:
                    is_nonterminal_missing = edge.edge_type == PRODUCTION_PARSER_EDGE and not is_in_first and is_in_follow
                    is_token_illegal = edge.edge_type == PRODUCTION_PARSER_EDGE and not is_in_first and not is_in_follow
                    is_NUM_or_ID_missing = edge.edge_type == NUM_ID_PARSER_EDGE and not current_token.token_type == edge.label
                    is_KEYWORD_or_SYMBOL_missing = edge.edge_type == KEYWORD_SYMBOL_PARSER_EDGE and not current_token.lexeme == edge.label
                    error_edge = edge
            if epsilon_state:
                # print(self.current_state.ID, current_token.lexeme)
                next_node = ParseNode(EPSILON, EPSILON)
                current_node.add_child(next_node)
                if file_ended:
                    return current_node
                self.current_state = epsilon_state
            elif error_edge:
                try:
                    if is_nonterminal_missing:
                        self.current_state = error_edge.destination
                        raise Exception("missing", error_edge.label.name, current_token)
                    elif is_NUM_or_ID_missing or is_KEYWORD_or_SYMBOL_missing:
                        self.current_state = error_edge.destination
                        raise Exception("missing", error_edge.label, current_token)
                    elif is_token_illegal:
                        illegal_token = current_token
                        current_token = get_next_valid_token(self.lexer)
                        illegal_lexeme = illegal_token.lexeme
                        if illegal_token.token_type in [ID, NUM]:
                            illegal_lexeme = illegal_token.token_type
                        raise Exception("illegal", illegal_lexeme, illegal_token)
                except Exception as e:
                    message = e.args[0]
                    lexeme = e.args[1]
                    token: Token = e.args[2]
                    error_message = f"#{token.lineno} : syntax error, {message} {lexeme}"
                    if lexeme == "$":
                        message = "Unexpexted"
                        error_message = f"#{token.lineno} : syntax error, Unexpected EOF"
                        file_ended = True
                        errors.append(error_message)
                        break
                    errors.append(error_message)
                    continue

        # print(self.current_state.ID, current_token.lexeme)
        return current_node
        