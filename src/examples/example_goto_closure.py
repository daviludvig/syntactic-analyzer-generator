import core.regex_parser as regex_parser
import core.goto as goto
from model.symbol_table import RegexToken, TokenType
import core.define_closure as define_closure

# === GRAMÁTICA ===
# terminals = {"mais", "vezes", "id", "(", ")"}
# non_terminals = {"E", "E'", "T", "F"}
# grammar = [
#     "E':== <E>",
#     "E:==<E>mais<T>",
#     "E:==<T>",
#     "T:==<T>vezes<F>",
#     "T:==<F>",
#     "F:==(<E>)",
#     "F:==id",
# ]

grammar = [
    "S':== <S>",
    "S:== <S> or <A>",
    "S:== <A>",
    "A:== <A> and <B>",
    "A:== <B>",
    "B:== not <B>",
    "B:== lparen<S>rparen",
    "B:== true",
    "B:== false",
]
terminals = {"or", "and", "not", "true", "false", "lparen", "rparen"}
non_terminals = {"S", "A", "B", "S'"}

# Gerar TokenTypes
tokentypes = regex_parser.get_regex_from_lines(grammar, terminals)
tokentypes_copy = tokentypes.copy()
tokentypes_copy[0].regex.insert(
    0, RegexToken(RegexToken.SLR_DOT, ".")
)  # Adiciona o ponto na primeira produção

i0 = define_closure.define_closure(tokentypes_copy[0], tokentypes)

for tokentype in i0:
    print(tokentype.name, ":", tokentype.regex)

goto_i0_a = goto.goto(i0, "A", terminals, non_terminals)
i1 = set()
for tokentype in goto_i0_a:
    tokentype_closure = define_closure.define_closure(tokentype, tokentypes)
    i1.update(tokentype_closure)

print("\ni1 (i0 -> A -> i1):")
for tokentype in i1:
    print(tokentype.name, ":", tokentype.regex)

goto_i1_and = goto.goto(i1, "and", terminals, non_terminals)
i2 = set()
for tokentype in goto_i1_and:
    tokentype_closure = define_closure.define_closure(tokentype, tokentypes)
    i2.update(tokentype_closure)

print("\ni2 (i1 -> and -> i2):")
for tokentype in i2:
    print(tokentype.name, ":", tokentype.regex)
