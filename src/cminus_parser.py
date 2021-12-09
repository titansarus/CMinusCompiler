from constants import *
from productions import *
from lexer import Lexer

current_token = None

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        global current_token
        while (token := self.lexer.get_next_token()).token_type in [WHITESPACE, COMMENT]:
            continue
        current_token = token
        root_parser = ProductionParser(Program, self.lexer)
        root = root_parser.parse()
        return root
    
    def parse_util(self, production):
        for edge in edges:
            self.parse_util(edge)
            if okay:
                result = ...
                break
        self.parse_util(result)

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
        if type(production) == Production:
            self.current_state = parser_states_dict[production]
    def parse(self):
        global current_token
        if self.current_state == None:
            if current_token.token_type == END_TOKEN:
                node = ParseNode(self.production, self.production)
            else:
                node = ParseNode(f'({current_token.token_type}, {current_token.lexeme})', f'({current_token.token_type}, {current_token.lexeme})')
            while (token := self.lexer.get_next_token()).token_type in [WHITESPACE, COMMENT]:
                continue
            current_token = token
            return node
        current_node = ParseNode(self.production, label=self.production.name)
        while not self.current_state.is_final:
            epsilon_state = None
            for edge in self.current_state.edges:
                is_valid_NUM_or_ID = edge.edge_type == NUM_ID_PARSER_EDGE and current_token.token_type == edge.label
                is_valid_KEYWORD_or_SYMBOL = edge.edge_type == KEYWORD_SYMBOL_PARSER_EDGE and current_token.lexeme == edge.label
                is_valid_Nonterminal = edge.edge_type == PRODUCTION_PARSER_EDGE and (current_token.lexeme in edge.label.first or current_token.token_type in edge.label.first)
                is_valid_epsilon_nonterminal = edge.edge_type == PRODUCTION_PARSER_EDGE and edge.label.first_has_epsilon and (current_token.lexeme in edge.label.follow or current_token.token_type in edge.label.follow)
                if is_valid_NUM_or_ID or is_valid_KEYWORD_or_SYMBOL:
                    epsilon_state = None
                    # print(self.current_state.ID, current_token.lexeme)
                    next_node = ProductionParser(edge.label, self.lexer).parse()
                    current_node.add_child(next_node)
                    self.current_state = edge.destination
                    break
                elif is_valid_Nonterminal or is_valid_epsilon_nonterminal:
                    epsilon_state = None
                    # print(self.current_state.ID, current_token.lexeme)
                    next_node = ProductionParser(edge.label, self.lexer).parse()
                    current_node.add_child(next_node)
                    self.current_state = edge.destination
                    break
                elif edge.edge_type == EPSILON_PARSER_EDGE:
                    epsilon_state = edge.destination
            if epsilon_state:
                # print(self.current_state.ID, current_token.lexeme)
                next_node = ParseNode(EPSILON, EPSILON)
                current_node.add_child(next_node)
                self.current_state = epsilon_state
        # print(self.current_state.ID, current_token.lexeme)
        return current_node
        