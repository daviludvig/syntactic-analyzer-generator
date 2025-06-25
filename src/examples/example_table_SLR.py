
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

#import example_get_canonical_items as example_canonical_items
import core.get_canonical_items as get_canonical_items
import core.regex_parser as regex_parser
import core.slr_table as slr_table
import core.utils as utils
import model.symbol_table as symbol_table
import core.define_first as define_first
import core.define_follow as define_follow

import core.LR_parsing as parser


gramatica = [
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

#terminals = {"or", "and", "not", "true", "false", "lparen", "rparen"}
#non_terminals = {"S", "A", "B", "S'"}

tokentypes = regex_parser.get_regex_from_lines(gramatica)

tokentypes_copy = tokentypes.copy()
tokentypes_copy[0].regex.insert(
    0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, ".")
)  # Adiciona o ponto na primeira produção
estados, transicoes = get_canonical_items.get_canonical_items(
    tokentypes_copy, "S"
)

firsts = define_first.define_first(tokentypes)


follows = define_follow.define_follow(tokentypes, firsts, start_symbol="S")


print("\n Construir tabela SLR:")

non_terminals = utils.get_non_terminals(gramatica)
table = slr_table.SLRTable()

action_dict = {}

print (f'não terminais {non_terminals}')

# Adiciona SHIFT, ACCEPT e GOTO na tabela SLR
for (origem, simbolo), destino in transicoes.items():
    if (destino == slr_table.Action.ACCEPT ) and (simbolo == "$"):
        # Caso simbolo seja final de sentença
        action = slr_table.Action(slr_table.Action.ACCEPT, "acc")
        action_dict[(origem, simbolo)] = action
    elif simbolo not in non_terminals:
        # Caso simbolo seja um terminal
        action = slr_table.Action(slr_table.Action.SHIFT, destino)
        action_dict[(origem, simbolo)] = action
    elif simbolo in non_terminals:
        # Caso simbolo seja um não terminal
        action = slr_table.Action(slr_table.Action.GOTO, destino)
        action_dict[(origem, simbolo)] = action



# Adiciona o REDUCE na tabela SLR
for i, estado in enumerate(estados):
    for prod in estado:
        if prod.regex[-1].type == symbol_table.RegexToken.SLR_DOT:
            #print(prod.regex)
            cabeca_follow = follows[prod.name]  # O resultado disso é um set de terminais (follows da cabeca)


            for simbolo in cabeca_follow:
                action = slr_table.Action(slr_table.Action.REDUCE, [prod.name, len(prod.regex[:-1])])
                action_dict[((i, simbolo))] = action
                #print(i, simbolo, action)

print(f'debug dicionario para parser: {action_dict}')

entrada = {0: 'not', 1: 'lparen', 2: 'true', 3: 'or', 4:'false', 5:'rparen', 6:'and', 7:'true', 8:'$'}
resposta = parser.LR_parsing(entrada, action_dict)