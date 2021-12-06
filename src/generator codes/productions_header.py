from constants import *
from parser_states import *

class Rule:
    def __init__(self, rhs):
        self.rhs = rhs
    def goes_with_token(self, token):
        for production in self.rhs:
            if (token.token_type == NUM or token.token_type == ID) and production == token.token_type:
                return True
            elif token.lexeme == production: # keywords and terminals
                return
            elif token.lexeme in production.first:
                return True
            elif production.first_has_epsilon:
                continue
            else:
                False

class Production:
    def __init__(self, name):
        self.name = name
        self.rules = []
        self.has_epsilon = False
        self.first_has_epsilon = False
        self.first = []
        self.follow = []
    def add_rule(self, rhs):
        self.rules.append(Rule(rhs))
    def get_next_rule(self, token):
        for rule in self.rules:
            if rule.goes_with_token(token):
                return rule
        return None
