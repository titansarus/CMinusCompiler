from constants import *

class ParserState:
    def __init__(self, ID, production, is_begin=False, is_final=False):
        self.ID = ID
        self.edges = []
        self.production = production
        self.is_begin = is_begin
        self.is_final = is_final
    def add_edge(self, destination, edge_type, label):
        edge = ParserEdge(self, destination, edge_type, label)
        self.edges.append(edge)

    def get_next_state(self, token, parser_states_dict, diagram_result=None):
        if diagram_result:
            for egde in self.edges:
                if egde.label == diagram_result:
                    return egde.destination
        epsilon_state = None
        for edge in self.edges:
            is_valid_NUM_or_ID = edge.edge_type == NUM_ID_PARSER_EDGE and token.token_type == edge.label
            is_valid_KEYWORD_or_SYMBOL = edge.edge_type == KEYWORD_SYMBOL_PARSER_EDGE and token.lexeme == edge.label
            is_valid_Nonterminal = edge.edge_type == PRODUCTION_PARSER_EDGE and token.lexeme in edge.label.first
            if is_valid_NUM_or_ID or is_valid_KEYWORD_or_SYMBOL:
                return edge.destination, False
            elif is_valid_Nonterminal:
                return parser_states_dict[edge.label], True
            elif edge.edge_type == EPSILON_PARSER_EDGE:
                epsilon_state = edge.destination
        return epsilon_state, False

class ParserEdge:
    def __init__(self, source: ParserState, destination: ParserState, edge_type, label):
        self.source = source
        self.destination = destination
        self.edge_type = edge_type
        self.label = label

def get_edge_type(rule_production):
    if rule_production == NUM or rule_production == ID:
        edge_type = NUM_ID_PARSER_EDGE
    elif type(rule_production) == str: # keywords and terminals
        edge_type = KEYWORD_SYMBOL_PARSER_EDGE
    elif type(rule_production).__name__ == "Production":
        edge_type = PRODUCTION_PARSER_EDGE
    else:
        print("invalid edge", rule_production)
        edge_type = None
    return edge_type

def generate_parser_states(productions):
    state_num = 0
    parser_states = [] # TODO delete if not needed
    parser_states_dict = {}
    for production in productions:
        initial_state = ParserState(state_num, production=production, is_begin=True)
        parser_states.append(initial_state)
        parser_states_dict[production] = initial_state
        state_num += 1
        final_state = ParserState(state_num, production=production, is_final=True)
        parser_states.append(final_state)
        if production.has_epsilon:
            initial_state.add_edge(final_state, EPSILON_PARSER_EDGE, label="EPSILON")
        state_num += 1
        for rule in production.rules:
            current_state = initial_state
            for rule_production in rule.rhs[:-1]:
                edge_type = get_edge_type(rule_production)
                next_state = ParserState(state_num, production=production)
                parser_states.append(next_state)
                state_num += 1
                current_state.add_edge(next_state, edge_type, label=rule_production)
                current_state = next_state
            current_state.add_edge(final_state, get_edge_type(rule.rhs[-1]), label=rule.rhs[-1])
    return parser_states_dict, parser_states