import core.define_first as define_first
import core.regex_parser as regex_parser

"""
"v" for 'or' / "a" for 'and' / "n" for 'not
Problema identificado: quando o terminal tem 2 letras (ex: id), só pega a primeira letra
"""
terminals = {'v', 'a', 'n', 'id'}
non_terminals = ["E", "E'", "T", "T'", "F"]
grammar = [
  "E:== <T><E'>",
  "E':== v<T><E'>",
  "E':== &",
  "T:== <F><T'>",
  "T':== a<F><T'>",
  "T':== [a-z]123",
  "F:== n<F>",
  "F:== id"
]
print(f"Analisando a gramática:{grammar}")
tokentypes = regex_parser.get_regex_from_lines(grammar)
firsts = define_first.define_first(tokentypes, terminals=terminals)
for nt, f in firsts.items():
    print(f"FIRST({nt}) = {f}")