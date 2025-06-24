import core.get_canonical_items as get_canonical_items
import core.regex_parser as regex_parser

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

tokentypes = regex_parser.get_regex_from_lines(grammar, terminals)

tokentypes_copy = tokentypes.copy()
tokentypes_copy[0].regex.insert(
    0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, ".")
)  # Adiciona o ponto na primeira produção

estados, transicoes = get_canonical_items.get_canonical_items(
    tokentypes_copy, terminals, non_terminals
)

for i, estado in enumerate(estados):
    print(f"\nEstado I{i}:")
    for tok in estado:
        print(
            f"  {tok.name}: {' '.join(str(token.value) for token in tok.regex if token.value is not None)}"
        )

print("\nTransições (GOTO):")
for (origem, simbolo), destino in transicoes.items():
    print(f"  GOTO(I{origem}, {simbolo}) = I{destino}")
