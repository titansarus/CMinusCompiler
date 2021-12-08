import first_follow_converter

productions = '''Program -> Declaration-list $
Declaration-list -> Declaration Declaration-list | EPSILON 
Declaration -> Declaration-initial Declaration-prime
Declaration-initial ->  Type-specifier ID
Declaration-prime -> Fun-declaration-prime | Var-declaration-prime
Var-declaration-prime -> ; | [ NUM ] ; 
Fun-declaration-prime ->  ( Params ) Compound-stmt
Type-specifier -> int | void
Params -> int ID Param-prime Param-list | void
Param-list -> , Param Param-list | EPSILON
Param -> Declaration-initial Param-prime
Param-prime -> [  ] | EPSILON
Compound-stmt -> { Declaration-list Statement-list }
Statement-list -> Statement Statement-list | EPSILON
Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt
Expression-stmt -> Expression ; | break ; | ;
Selection-stmt -> if ( Expression ) Statement Else-stmt
Else-stmt -> endif | else Statement endif
Iteration-stmt -> repeat Statement until ( Expression ) 
Return-stmt -> return Return-stmt-prime
Return-stmt-prime -> ; | Expression ;
Expression -> Simple-expression-zegond | ID B
B -> = Expression | [ Expression ] H | Simple-expression-prime
H -> = Expression | G D C
Simple-expression-zegond -> Additive-expression-zegond C
Simple-expression-prime -> Additive-expression-prime C
C -> Relop Additive-expression | EPSILON
Relop -> < | ==
Additive-expression -> Term D
Additive-expression-prime -> Term-prime D
Additive-expression-zegond -> Term-zegond D
D -> Addop Term D | EPSILON
Addop -> + | -
Term -> Factor G
Term-prime -> Factor-prime G
Term-zegond -> Factor-zegond G
G -> * Factor G | EPSILON
Factor -> ( Expression ) | ID Var-call-prime | NUM
Var-call-prime -> ( Args ) | Var-prime
Var-prime -> [ Expression ] | EPSILON
Factor-prime -> ( Args ) | EPSILON
Factor-zegond -> ( Expression ) | NUM
Args -> Arg-list | EPSILON
Arg-list -> Expression Arg-list-prime
Arg-list-prime -> , Expression Arg-list-prime | EPSILON'''.split("\n")

program = ""
production_names = ""
with open("./src/generator codes/productions_header.py") as f:
    program += f.read() + '\n'
for production in productions:
    lhs, rhs = production.split(" -> ")
    production_names += f'{lhs.replace("-", "_")}, '
    program += f'{lhs.replace("-", "_")} = Production("{lhs}")\n'
for production in productions:
    lhs, rhs = production.split(" -> ")
    lhs_name = lhs.replace("-", "_")
    rhs = rhs.split(" | ")
    for rule in rhs:
        rule = rule.strip()
        if rule == "EPSILON":
            program += f'{lhs_name}.has_epsilon = True\n'
        else:
            temp = ""
            for semitoken in rule.split():
                if semitoken == "NUM" or semitoken == "ID":
                    temp += f'"{semitoken}", '
                elif semitoken[0].isupper():
                    temp += f'{semitoken.replace("-", "_")}, '
                else:
                    temp += f'"{semitoken}", '
            temp = f'[{temp}]'
            program += f'{lhs_name}.add_rule({temp})\n'
program += first_follow_converter.get_program()
program += f'\nproductions = [{production_names}]\n'
program += f'parser_states_dict, parser_states_list = generate_parser_states(productions)\n'

with open("./src/generator codes/program.py", "w") as f:
    print(program, file=f)
