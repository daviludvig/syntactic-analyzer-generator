
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

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
    "B:== id",
]

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

table.populate(estados, transicoes, follows, non_terminals)

print(f'debug dicionario para parser: {table.table}')

input_file = "inputs/tokens2.txt"

entrada = utils.get_tokens_from_file(input_file)

resposta = parser.LR_parsing(entrada, table.table)

print(f'\nEntrada: {entrada}, Resposta: {resposta}')