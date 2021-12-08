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
    
    def parse_util(self, production):
        for edge in edges:
            self.parse_util(edge)
            if okay:
                result = ...
                break
        self.parse_util(result)

        # initial_state = parser_states_dict[Program]
        # self.parse_util(initial_state)
        # return initial_state

    # def parse_util(self, state: ParserState, get_state_handler, is_nonterminal=False):
    #     if state.is_final:
    #         return DIAGRAM_ENDED, state
    #     if state == None:
    #         return NO_WAY_IN_DIAGRAM, None
    #     if not is_nonterminal:
    #         while (token := self.lexer.get_next_token()).token_type in [COMMENT, WHITESPACE]:
    #             continue
    #         self.current_token = token
    #     diagram_result = None
    #     next_state, is_nonterminal, final_state = state.get_next_state(self.current_token, parser_states_dict, diagram_result)
    #     result_status, diagram_result = self.parse_util(next_state, is_nonterminal=is_nonterminal)
            

        # # if token.token_type == END_TOKEN:
        # #     return ParseNode(production=None, label="$", parent=parent)
        
        # # we have parser_states from "productions"
        # current_state = parser_states_list[0]
        # stack = []
        # while token.token_type != END_TOKEN:
        #     if False:
        #         pass
        #     else: # panic mode
        #         if token.lexeme in current_node.production.follow:
        #             pass
        #         else:
        #             pass
        #     token = lexer.get_next_token()

class ParseNode:
    def __init__(self, production=Program, label="Program", parent=None):
        self.production = production
        self.label = label
        self.parent = parent
        self.children = []
    def add_child(self, child: "ParseNode"):
        child.parent = self
        self.children.append(child)

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
            while (token := self.lexer.get_next_token()).token_type in [WHITESPACE, COMMENT]:
                continue
            current_token = token
            return ParseNode(self.production, self.production)
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
                    print(self.current_state.ID, current_token.lexeme)
                    next_node = ProductionParser(edge.label, self.lexer).parse()
                    current_node.add_child(next_node)
                    self.current_state = edge.destination
                    break
                elif is_valid_Nonterminal or is_valid_epsilon_nonterminal:
                    epsilon_state = None
                    print(self.current_state.ID, current_token.lexeme)
                    next_node = ProductionParser(edge.label, self.lexer).parse()
                    current_node.add_child(next_node)
                    self.current_state = edge.destination
                    break
                elif edge.edge_type == EPSILON_PARSER_EDGE:
                    epsilon_state = edge.destination
            if epsilon_state:
                print(self.current_state.ID, current_token.lexeme)
                next_node = ParseNode(EPSILON, EPSILON)
                current_node.add_child(next_node)
                self.current_state = epsilon_state
        print(self.current_state.ID, current_token.lexeme)
        return current_node
        