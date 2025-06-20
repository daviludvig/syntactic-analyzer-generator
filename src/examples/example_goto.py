import core.regex_parser as regex_parser
import core.goto as goto

terminals = {"v", "a", "n", "identificador", "123"}
non_terminals = {"E", "E'", "T", "T'", "F"}
grammar = [
    "E:== <T><E'>",
    "E':== <T><E'>",
    "E':== &",
    "T:== <F><T'>",
    "T':== a<F><T'>",
    "T':== 123",
    "F:== n<F>",
    "F:== identificador",
]

tokentypes = regex_parser.get_regex_from_lines(grammar)
for tokentype in tokentypes:
    regex = tokentype.regex
    regex.insert(0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, "."))

for tokentype in tokentypes:
    print(f"TokenType: {tokentype.name}, Regex: {tokentype.regex}")

print(f"Analisando a gramática: {grammar}\n")

for element in non_terminals.union(terminals):
    proximo = goto.goto(tokentypes, element, terminals, non_terminals)
    print(f"Próximo estado após a transição com '{element}':\n{proximo}\n")
