def generate_code(program):
    output = ""
    for lineno, line in enumerate(program):
        output += f"{lineno}\t{line}"
        output += "\n"
    return output