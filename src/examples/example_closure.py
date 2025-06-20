
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import core.regex_parser as regex_parser
import core.define_closure as define_closure


terminals = {"v", "a", "n", "identificador", "123"}
non_terminals = ["E", "E'", "T", "T'", "F"]
grammar = [
    "E:== <T><E'>",
    "E':== v<T><E'>",
    "E':== &",
    "T:== <F><T'>",
    "T':== a<F><T'>",
    "T':== 123",
    "F:== n<F>",
    "F:== identificador",
]


print(f"Analisando a gramática:{grammar}")
tokentypes = regex_parser.get_regex_from_lines(grammar)

print("todos tokentypes: ", tokentypes)

for tktp in tokentypes:
    closure = define_closure.define_closure(tktp, tokentypes)
    print("Para ", tktp, ": ")
    print (" CLOSURE: ", closure)