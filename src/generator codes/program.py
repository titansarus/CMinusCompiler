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

Program = Production("Program")
Declaration_list = Production("Declaration-list")
Declaration = Production("Declaration")
Declaration_initial = Production("Declaration-initial")
Declaration_prime = Production("Declaration-prime")
Var_declaration_prime = Production("Var-declaration-prime")
Fun_declaration_prime = Production("Fun-declaration-prime")
Type_specifier = Production("Type-specifier")
Params = Production("Params")
Param_list = Production("Param-list")
Param = Production("Param")
Param_prime = Production("Param-prime")
Compound_stmt = Production("Compound-stmt")
Statement_list = Production("Statement-list")
Statement = Production("Statement")
Expression_stmt = Production("Expression-stmt")
Selection_stmt = Production("Selection-stmt")
Else_stmt = Production("Else-stmt")
Iteration_stmt = Production("Iteration-stmt")
Return_stmt = Production("Return-stmt")
Return_stmt_prime = Production("Return-stmt-prime")
Expression = Production("Expression")
B = Production("B")
H = Production("H")
Simple_expression_zegond = Production("Simple-expression-zegond")
Simple_expression_prime = Production("Simple-expression-prime")
C = Production("C")
Relop = Production("Relop")
Additive_expression = Production("Additive-expression")
Additive_expression_prime = Production("Additive-expression-prime")
Additive_expression_zegond = Production("Additive-expression-zegond")
D = Production("D")
Addop = Production("Addop")
Term = Production("Term")
Term_prime = Production("Term-prime")
Term_zegond = Production("Term-zegond")
G = Production("G")
Factor = Production("Factor")
Var_call_prime = Production("Var-call-prime")
Var_prime = Production("Var-prime")
Factor_prime = Production("Factor-prime")
Factor_zegond = Production("Factor-zegond")
Args = Production("Args")
Arg_list = Production("Arg-list")
Arg_list_prime = Production("Arg-list-prime")
Program.add_rule([Declaration_list, "$", ])
Declaration_list.add_rule([Declaration, Declaration_list, ])
Declaration_list.has_epsilon = True
Declaration.add_rule([Declaration_initial, Declaration_prime, ])
Declaration_initial.add_rule([Type_specifier, "ID", ])
Declaration_prime.add_rule([Fun_declaration_prime, ])
Declaration_prime.add_rule([Var_declaration_prime, ])
Var_declaration_prime.add_rule([";", ])
Var_declaration_prime.add_rule(["[", "NUM", "]", ";", ])
Fun_declaration_prime.add_rule(["(", Params, ")", Compound_stmt, ])
Type_specifier.add_rule(["int", ])
Type_specifier.add_rule(["void", ])
Params.add_rule(["int", "ID", Param_prime, Param_list, ])
Params.add_rule(["void", ])
Param_list.add_rule([",", Param, Param_list, ])
Param_list.has_epsilon = True
Param.add_rule([Declaration_initial, Param_prime, ])
Param_prime.add_rule(["[", "]", ])
Param_prime.has_epsilon = True
Compound_stmt.add_rule(["{", Declaration_list, Statement_list, "}", ])
Statement_list.add_rule([Statement, Statement_list, ])
Statement_list.has_epsilon = True
Statement.add_rule([Expression_stmt, ])
Statement.add_rule([Compound_stmt, ])
Statement.add_rule([Selection_stmt, ])
Statement.add_rule([Iteration_stmt, ])
Statement.add_rule([Return_stmt, ])
Expression_stmt.add_rule([Expression, ";", ])
Expression_stmt.add_rule(["break", ";", ])
Expression_stmt.add_rule([";", ])
Selection_stmt.add_rule(["if", "(", Expression, ")", Statement, Else_stmt, ])
Else_stmt.add_rule(["endif", ])
Else_stmt.add_rule(["else", Statement, "endif", ])
Iteration_stmt.add_rule(["repeat", Statement, "until", "(", Expression, ")", ])
Return_stmt.add_rule(["return", Return_stmt_prime, ])
Return_stmt_prime.add_rule([";", ])
Return_stmt_prime.add_rule([Expression, ";", ])
Expression.add_rule([Simple_expression_zegond, ])
Expression.add_rule(["ID", B, ])
B.add_rule(["=", Expression, ])
B.add_rule(["[", Expression, "]", H, ])
B.add_rule([Simple_expression_prime, ])
H.add_rule(["=", Expression, ])
H.add_rule([G, D, C, ])
Simple_expression_zegond.add_rule([Additive_expression_zegond, C, ])
Simple_expression_prime.add_rule([Additive_expression_prime, C, ])
C.add_rule([Relop, Additive_expression, ])
C.has_epsilon = True
Relop.add_rule(["<", ])
Relop.add_rule(["==", ])
Additive_expression.add_rule([Term, D, ])
Additive_expression_prime.add_rule([Term_prime, D, ])
Additive_expression_zegond.add_rule([Term_zegond, D, ])
D.add_rule([Addop, Term, D, ])
D.has_epsilon = True
Addop.add_rule(["+", ])
Addop.add_rule(["-", ])
Term.add_rule([Factor, G, ])
Term_prime.add_rule([Factor_prime, G, ])
Term_zegond.add_rule([Factor_zegond, G, ])
G.add_rule(["*", Factor, G, ])
G.has_epsilon = True
Factor.add_rule(["(", Expression, ")", ])
Factor.add_rule(["ID", Var_call_prime, ])
Factor.add_rule(["NUM", ])
Var_call_prime.add_rule(["(", Args, ")", ])
Var_call_prime.add_rule([Var_prime, ])
Var_prime.add_rule(["[", Expression, "]", ])
Var_prime.has_epsilon = True
Factor_prime.add_rule(["(", Args, ")", ])
Factor_prime.has_epsilon = True
Factor_zegond.add_rule(["(", Expression, ")", ])
Factor_zegond.add_rule(["NUM", ])
Args.add_rule([Arg_list, ])
Args.has_epsilon = True
Arg_list.add_rule([Expression, Arg_list_prime, ])
Arg_list_prime.add_rule([",", Expression, Arg_list_prime, ])
Arg_list_prime.has_epsilon = True
Program.first = ["$", "int", "void", ]
Declaration_list.first_has_epsilon = True
Declaration_list.first = ["int", "void", ]
Declaration.first = ["int", "void", ]
Declaration_initial.first = ["int", "void", ]
Declaration_prime.first = ["(", ";", "[", ]
Var_declaration_prime.first = [";", "[", ]
Fun_declaration_prime.first = ["(", ]
Type_specifier.first = ["int", "void", ]
Params.first = ["int", "void", ]
Param_list.first_has_epsilon = True
Param_list.first = [",", ]
Param.first = ["int", "void", ]
Param_prime.first_has_epsilon = True
Param_prime.first = ["[", ]
Compound_stmt.first = ["{", ]
Statement_list.first_has_epsilon = True
Statement_list.first = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", ]
Statement.first = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", ]
Expression_stmt.first = ["break", ";", "ID", "(", "NUM", ]
Selection_stmt.first = ["if", ]
Else_stmt.first = ["endif", "else", ]
Iteration_stmt.first = ["repeat", ]
Return_stmt.first = ["return", ]
Return_stmt_prime.first = [";", "ID", "(", "NUM", ]
Expression.first = ["ID", "(", "NUM", ]
B.first_has_epsilon = True
B.first = ["=", "[", "(", "*", "+", "_", "<", "==", ]
H.first_has_epsilon = True
H.first = ["=", "*", "+", "_", "<", "==", ]
Simple_expression_zegond.first = ["(", "NUM", ]
Simple_expression_prime.first_has_epsilon = True
Simple_expression_prime.first = ["(", "*", "+", "_", "<", "==", ]
C.first_has_epsilon = True
C.first = ["<", "==", ]
Relop.first = ["<", "==", ]
Additive_expression.first = ["(", "ID", "NUM", ]
Additive_expression_prime.first_has_epsilon = True
Additive_expression_prime.first = ["(", "*", "+", "_", ]
Additive_expression_zegond.first = ["(", "NUM", ]
D.first_has_epsilon = True
D.first = ["+", "_", ]
Addop.first = ["+", "_", ]
Term.first = ["(", "ID", "NUM", ]
Term_prime.first_has_epsilon = True
Term_prime.first = ["(", "*", ]
Term_zegond.first = ["(", "NUM", ]
G.first_has_epsilon = True
G.first = ["*", ]
Factor.first = ["(", "ID", "NUM", ]
Var_call_prime.first_has_epsilon = True
Var_call_prime.first = ["(", "[", ]
Var_prime.first_has_epsilon = True
Var_prime.first = ["[", ]
Factor_prime.first_has_epsilon = True
Factor_prime.first = ["(", ]
Factor_zegond.first = ["(", "NUM", ]
Args.first_has_epsilon = True
Args.first = ["ID", "(", "NUM", ]
Arg_list.first = ["ID", "(", "NUM", ]
Arg_list_prime.first_has_epsilon = True
Arg_list_prime.first = [",", ]
Declaration_list.follow = ["$", "{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", ]
Declaration.follow = ["int", "void", "$", "{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", ]
Declaration_initial.follow = ["(", ";", "[", ",", ")", ]
Declaration_prime.follow = ["int", "void", "$", "{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", ]
Var_declaration_prime.follow = ["int", "void", "$", "{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", ]
Fun_declaration_prime.follow = ["int", "void", "$", "{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", ]
Type_specifier.follow = ["ID", ]
Params.follow = [")", ]
Param_list.follow = [")", ]
Param.follow = [",", ")", ]
Param_prime.follow = [",", ")", ]
Compound_stmt.follow = ["int", "void", "$", "{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Statement_list.follow = ["}", ]
Statement.follow = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Expression_stmt.follow = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Selection_stmt.follow = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Else_stmt.follow = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Iteration_stmt.follow = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Return_stmt.follow = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Return_stmt_prime.follow = ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}", "endif", "else", "until", ]
Expression.follow = [";", ")", "]", ",", ]
B.follow = [";", ")", "]", ",", ]
H.follow = [";", ")", "]", ",", ]
Simple_expression_zegond.follow = [";", ")", "]", ",", ]
Simple_expression_prime.follow = [";", ")", "]", ",", ]
C.follow = [";", ")", "]", ",", ]
Relop.follow = ["(", "ID", "NUM", ]
Additive_expression.follow = [";", ")", "]", ",", ]
Additive_expression_prime.follow = ["<", "==", ";", ")", "]", ",", ]
Additive_expression_zegond.follow = ["<", "==", ";", ")", "]", ",", ]
D.follow = ["<", "==", ";", ")", "]", ",", ]
Addop.follow = ["(", "ID", "NUM", ]
Term.follow = ["+", "_", ";", ")", "<", "==", "]", ",", ]
Term_prime.follow = ["+", "_", "<", "==", ";", ")", "]", ",", ]
Term_zegond.follow = ["+", "_", "<", "==", ";", ")", "]", ",", ]
G.follow = ["+", "_", "<", "==", ";", ")", "]", ",", ]
Factor.follow = ["*", "+", "_", ";", ")", "<", "==", "]", ",", ]
Var_call_prime.follow = ["*", "+", "_", ";", ")", "<", "==", "]", ",", ]
Var_prime.follow = ["*", "+", "_", ";", ")", "<", "==", "]", ",", ]
Factor_prime.follow = ["*", "+", "_", "<", "==", ";", ")", "]", ",", ]
Factor_zegond.follow = ["*", "+", "_", "<", "==", ";", ")", "]", ",", ]
Args.follow = [")", ]
Arg_list.follow = [")", ]
Arg_list_prime.follow = [")", ]

productions = [Program, Declaration_list, Declaration, Declaration_initial, Declaration_prime, Var_declaration_prime, Fun_declaration_prime, Type_specifier, Params, Param_list, Param, Param_prime, Compound_stmt, Statement_list, Statement, Expression_stmt, Selection_stmt, Else_stmt, Iteration_stmt, Return_stmt, Return_stmt_prime, Expression, B, H, Simple_expression_zegond, Simple_expression_prime, C, Relop, Additive_expression, Additive_expression_prime, Additive_expression_zegond, D, Addop, Term, Term_prime, Term_zegond, G, Factor, Var_call_prime, Var_prime, Factor_prime, Factor_zegond, Args, Arg_list, Arg_list_prime, ]
parser_states_dict, parser_states_list = generate_parser_states(productions)

