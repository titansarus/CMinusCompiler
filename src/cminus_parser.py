from constants import *
from productions import *
import lexer

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tree = ParseTree()

    def parse(self):
        token = lexer.get_next_token()
        current_node = ParseNode(Program)
        stack = []
        while token.token_type != END_TOKEN:
            next_rule = current_node.production.get_next_rule(token)
            if next_rule: 
                pass
            else: # panic mode
                if token.lexeme in current_node.production.follow:
                    pass
                else:
                    pass
            token = lexer.get_next_token()

class ParseNode:
    def __init__(self, production=Program, parent=None):
        self.production = production
        self.parent = parent
        self.children = []
    def add_child(self, child: ParseNode):
        child.parent = self
        self.children.append(child)