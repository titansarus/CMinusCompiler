import graphviz
from ..Parser.productions import productions
from ..Parser.parser_states import generate_parser_states

parser_states_dict, parser_states_list = generate_parser_states(productions)
dot = graphviz.Digraph(comment='Transition Table')

for state in parser_states_list:
    if state.is_begin:
        dot.node(str(state.ID), f'{state.production.name} ({str(state.ID)})')
    else:
        dot.node(str(state.ID))

for state in parser_states_list:
    for edge in state.edges:
        label = edge.label
        if type(label) != str:
            label = label.name
        dot.edge(str(edge.source.ID), str(edge.destination.ID), label=label)

with open("transition_graph.dot", "w") as f:
    print(dot.source, file=f)
