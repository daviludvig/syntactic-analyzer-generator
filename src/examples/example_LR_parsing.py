import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import core.get_canonical_items as get_canonical_items
import core.regex_parser as regex_parser
from core.slr_table import SLRTable, Action
import core.utils as utils
import model.symbol_table as symbol_table
import core.define_first as define_first
import core.define_follow as define_follow

import core.LR_parsing as parser
from core.utils import get_tokens_from_file, get_grammar_from_file

def main():

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
    tokens = [
        ('not', 'PR'),
        ('lparen', 'LPAREN'),
        ('true', 'TRUE'),
        ('or', 'PR'),
        ('false', 'FALSE'),
        ('rparen', 'RPAREN'),
        ('and', 'PR'),
        ('lparen', 'LPAREN'),
        ('true', 'TRUE'),
        ('rparen', 'RPAREN'),
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

    non_terminals = utils.get_non_terminals(gramatica)
    slr_table = SLRTable()

    slr_table.populate(estados, transicoes, follows, non_terminals)
                    
    print(f' Grámatica em análise:')
    for linha in gramatica:
        print(linha)
        
    resposta = parser.LR_parsing(tokens, slr_table.table)

    if resposta:
        print("A palavra pertence à linguagem!")
    else:
        print("Erro de análise.")

if __name__ == "__main__":
    main()