
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

new_productions = ""
for production in productions:
    lhs, rhs = production.split(" -> ")
    for rule in rhs.split(" | "):
        new_productions += f'{lhs.replace("-", "_")} -> {rule.replace("-", "_")}\n'
with open("first_follow_productions.txt", "w") as f:
    print(new_productions, file=f)
