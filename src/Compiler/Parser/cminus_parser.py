from .productions import *
from ..Lexer.lexer import Lexer
from ..Lexer.cminus_token import Token
from ..CodeGen.codegen import CodeGen
from ..CodeGen.semantic_exception import SemanticException

previous_token = None
current_token = None
errors = []
semantic_errors = []
file_ended = False


def get_next_valid_token(lexer: Lexer):
    token = lexer.get_next_token()
    skip_states = PANIC_STATES + [WHITESPACE, COMMENT]
    while token.token_type in skip_states:
        token = lexer.get_next_token()
    return token


class Parser:
    def __init__(self, lexer: Lexer, codegen: CodeGen):
        self.lexer = lexer
        self.codegen = codegen

    def parse(self):
        global current_token, previous_token, errors, file_ended
        errors = []
        file_ended = False
        previous_token = current_token
        current_token = get_next_valid_token(self.lexer)
        root_parser = ProductionParser(Program, self.lexer, self.codegen)
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
    def __init__(self, production: Production, lexer: Lexer, codegen: CodeGen):
        self.production = production
        self.lexer = lexer
        self.current_state = None
        self.codegen = codegen
        self.errors = []
        if type(production) == Production:
            self.current_state = parser_states_dict[production]

    def parse(self):
        global current_token, previous_token, errors, file_ended, semantic_errors
        if self.current_state is None:
            if current_token.token_type == END_TOKEN:
                node = ParseNode(self.production, self.production)
            else:
                node = ParseNode(f'({current_token.token_type}, {current_token.lexeme})',
                                 f'({current_token.token_type}, {current_token.lexeme})')
            previous_token = current_token
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

                is_action_code = edge.edge_type == ACTION_PARSER_EDGE
                is_valid_NUM_or_ID = edge.edge_type == NUM_ID_PARSER_EDGE and current_token.token_type == edge.label
                is_valid_KEYWORD_or_SYMBOL = edge.edge_type == KEYWORD_SYMBOL_PARSER_EDGE and current_token.lexeme == edge.label
                is_valid_Nonterminal = edge.edge_type == PRODUCTION_PARSER_EDGE and is_in_first
                is_valid_epsilon_nonterminal = edge.edge_type == PRODUCTION_PARSER_EDGE and edge.label.first_has_epsilon and is_in_follow

                if is_action_code:
                    try:
                        self.codegen.act(edge.label, previous_token, current_token)
                    except SemanticException as e:
                        semantic_errors.append(f"#{current_token.lineno} : {e}")
                    # except:
                    #     pass
                    self.current_state = edge.destination
                    error_edge = None
                    break

                elif is_valid_NUM_or_ID or is_valid_KEYWORD_or_SYMBOL:
                    epsilon_state = None
                    next_node = ProductionParser(edge.label, self.lexer, self.codegen).parse()
                    current_node.add_child(next_node)
                    if file_ended:
                        return current_node
                    self.current_state = edge.destination
                    error_edge = None
                    break

                elif is_valid_Nonterminal or is_valid_epsilon_nonterminal:
                    epsilon_state = None
                    next_node = ProductionParser(edge.label, self.lexer, self.codegen).parse()
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
                next_node = ParseNode(EPSILON, EPSILON)
                current_node.add_child(next_node)
                if file_ended:
                    return current_node
                self.current_state = epsilon_state
            elif error_edge:
                try:
                    self.generate_panic(error_edge, is_KEYWORD_or_SYMBOL_missing, is_NUM_or_ID_missing,
                                        is_nonterminal_missing, is_token_illegal)
                except Exception as e:
                    should_continue = ProductionParser.handle_panic_error_message(e)
                    if should_continue:
                        continue
                    break

        return current_node

    @staticmethod
    def handle_panic_error_message(e: Exception) -> bool:
        global file_ended
        message = e.args[0]
        lexeme = e.args[1]
        token: Token = e.args[2]
        error_message = f"#{token.lineno} : syntax error, {message} {lexeme}"
        if token.lexeme == "$":
            message = "Unexpected EOF"
            error_message = f"#{token.lineno} : syntax error, {message}"
            file_ended = True
            errors.append(error_message)
            return False
        errors.append(error_message)
        return True

    def generate_panic(self, error_edge, is_KEYWORD_or_SYMBOL_missing, is_NUM_or_ID_missing, is_nonterminal_missing,
                       is_token_illegal):
        global current_token, previous_token
        if is_nonterminal_missing:
            self.current_state = error_edge.destination
            raise Exception("missing", error_edge.label.name, current_token)

        elif is_NUM_or_ID_missing or is_KEYWORD_or_SYMBOL_missing:
            self.current_state = error_edge.destination
            raise Exception("missing", error_edge.label, current_token)

        elif is_token_illegal:
            illegal_token = current_token
            previous_token = current_token
            current_token = get_next_valid_token(self.lexer)
            illegal_lexeme = illegal_token.lexeme
            if illegal_token.token_type in [ID, NUM]:
                illegal_lexeme = illegal_token.token_type
            raise Exception("illegal", illegal_lexeme, illegal_token)
