
def get_program():
    firsts = '''Program	$ int void
Declaration_list	ε int void
Declaration	int void
Declaration_initial	int void
Declaration_prime	( ; [
Var_declaration_prime	; [
Fun_declaration_prime	(
Type_specifier	int void
Params	int void
Param_list	, ε
Param	int void
Param_prime	[ ε
Compound_stmt	{
Statement_list	ε { break ; if repeat return ID ( NUM
Statement	{ break ; if repeat return ID ( NUM
Expression_stmt	break ; ID ( NUM
Selection_stmt	if
Else_stmt	endif else
Iteration_stmt	repeat
Return_stmt	return
Return_stmt_prime	; ID ( NUM
Expression	ID ( NUM
B	= [ ( * + _ < == ε
H	= * ε + _ < ==
Simple_expression_zegond	( NUM
Simple_expression_prime	( * + _ < == ε
C	ε < ==
Relop	< ==
Additive_expression	( ID NUM
Additive_expression_prime	( * + _ ε
Additive_expression_zegond	( NUM
D	ε + _
Addop	+ _
Term	( ID NUM
Term_prime	( * ε
Term_zegond	( NUM
G	* ε
Factor	( ID NUM
Var_call_prime	( [ ε
Var_prime	[ ε
Factor_prime	( ε
Factor_zegond	( NUM
Args	ε ID ( NUM
Arg_list	ID ( NUM
Arg_list_prime	, ε'''.split('\n')
    follows = '''Declaration_list	$ { break ; if repeat return ID ( NUM }
Declaration	int void $ { break ; if repeat return ID ( NUM }
Declaration_initial	( ; [ , )
Declaration_prime	int void $ { break ; if repeat return ID ( NUM }
Var_declaration_prime	int void $ { break ; if repeat return ID ( NUM }
Fun_declaration_prime	int void $ { break ; if repeat return ID ( NUM }
Type_specifier	ID
Params	)
Param_list	)
Param	, )
Param_prime	, )
Compound_stmt	int void $ { break ; if repeat return ID ( NUM } endif else until
Statement_list	}
Statement	{ break ; if repeat return ID ( NUM } endif else until
Expression_stmt	{ break ; if repeat return ID ( NUM } endif else until
Selection_stmt	{ break ; if repeat return ID ( NUM } endif else until
Else_stmt	{ break ; if repeat return ID ( NUM } endif else until
Iteration_stmt	{ break ; if repeat return ID ( NUM } endif else until
Return_stmt	{ break ; if repeat return ID ( NUM } endif else until
Return_stmt_prime	{ break ; if repeat return ID ( NUM } endif else until
Expression	; ) ] ,
B	; ) ] ,
H	; ) ] ,
Simple_expression_zegond	; ) ] ,
Simple_expression_prime	; ) ] ,
C	; ) ] ,
Relop	( ID NUM
Additive_expression	; ) ] ,
Additive_expression_prime	< == ; ) ] ,
Additive_expression_zegond	< == ; ) ] ,
D	< == ; ) ] ,
Addop	( ID NUM
Term	+ _ ; ) < == ] ,
Term_prime	+ _ < == ; ) ] ,
Term_zegond	+ _ < == ; ) ] ,
G	+ _ < == ; ) ] ,
Factor	* + _ ; ) < == ] ,
Var_call_prime	* + _ ; ) < == ] ,
Var_prime	* + _ ; ) < == ] ,
Factor_prime	* + _ < == ; ) ] ,
Factor_zegond	* + _ < == ; ) ] ,
Args	)
Arg_list	)
Arg_list_prime	)'''.split('\n')

    program = ""
    for line in firsts:
        production, first = line.split('\t')
        production_first = ""
        for f in first.split():
            if f == "ε":
                program += f'{production}.first_has_epsilon = True\n'
            elif f == "_":
                production_first += f'"-", '
            else:
                production_first += f'"{f}", '
        program += f'{production}.first = [{production_first}]\n'

    for line in follows:
        production, follow = line.split('\t')
        production_follow = ""
        for f in follow.split():
            if f == "_":
                production_follow += f'"-", '
            else:
                production_follow += f'"{f}", '
        program += f'{production}.follow = [{production_follow}]\n'

    return program
