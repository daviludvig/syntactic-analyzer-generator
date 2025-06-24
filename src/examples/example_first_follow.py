import core.define_first as define_first
import core.define_follow as define_follow
import core.regex_parser as regex_parser

grammar = [
    "E:== <T> <E'>",
    "E':== v <T> <E'>",
    "E':== &",
    "T:== <F> <T'>",
    "T':== a <F> <T'>",
    "T':== 123",
    "F:==  dado n <F>",
    "F:== identificador dado",
]
print(f"Analisando a gramática:{grammar}")
tokentypes = regex_parser.get_regex_from_lines(grammar)
print(tokentypes)
firsts = define_first.define_first(tokentypes)
for nt, f in firsts.items():
    print(f"FIRST({nt}) = {f}")

follows = define_follow.define_follow(tokentypes, firsts, start_symbol="E")
for nt, f in follows.items():
    print(f"FOLLOW({nt}) = {f}")
