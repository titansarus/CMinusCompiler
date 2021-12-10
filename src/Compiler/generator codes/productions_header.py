from ..Parser.parser_states import *


class Rule:
    def __init__(self, rhs):
        self.rhs = rhs


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
