
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import sys
import core.utils as utils
import core.get_canonical_items as get_canonical_items
import core.regex_parser as regex_parser
from core.slr_table import SLRTable
import core.utils as utils
import core.define_first as define_first
import core.define_follow as define_follow

import core.LR_parsing as parser
from core.utils import get_tokens_from_file, get_grammar_from_file

def write_in_files(firsts, follows, slr_table, final_analysis ) -> None:
    """
    Escreve os resultados encontrados em um arquivo de saída.
    """
    utils.prepare_output_directory()
    for dfa in dfas:
        if dfa is not None:
            utils.write_in_file(f"{utils.OUTPUT_PATH_DIR}/automatos/{dfa.name}.txt", dfa.getTabularFormat())
    
    for token in tokens:
        utils.write_in_file(f"{utils.OUTPUT_PATH_DIR}/tokens.txt", str(token))
        
    utils.write_in_file(f"{utils.OUTPUT_PATH_DIR}/symbol_table.txt", str(symbol_table))



def main() -> None:
    """
    Função principal que executa o analisador sintático.
    Lê os arquivos de lista de tokens e gramática, calcula first e follow da gramática, faz tabela SLR e verifica se a entrada é válida.
    Uso: python src/main.py <token_list> <main_rules>
    """
    if len(sys.argv) != 3:
        print("Uso: python src/main.py <token_list> <main_rules>")
        sys.exit(1)
        
    token_list = sys.argv[1]
    main_rules = sys.argv[2]
    
    if not utils.file_exists(main_rules) or not utils.file_exists(token_list):
        print(f"Arquivo de entrada ou gramática não encontrado: {main_rules} ou {token_list}")
        sys.exit(1)
    
    gramatica = get_grammar_from_file(main_rules)

    print(f' Grámatica em análise:')
    for linha in gramatica:
        print(linha)
    print("\n")

    tokentypes = regex_parser.get_regex_from_lines(gramatica)

    tokentypes_copy = tokentypes.copy()
    tokentypes_copy[0].regex.insert(
        0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, ".")
    )  # Adiciona o ponto na primeira produção
    estados, transicoes = get_canonical_items.get_canonical_items(
        tokentypes_copy, "S"
    )

    firsts = define_first.define_first(tokentypes)

    print(f' First da gramática:')
    for key, value in firsts.items():
        print(f" Simbolo {key} : first : {value}")
    print("\n")

    follows = define_follow.define_follow(tokentypes, firsts, start_symbol="S")

    print(f' Follows da gramática:')
    for key, value in follows.items():
        print(f" Simbolo {key} : first : {value}")
    print("\n")

    non_terminals = utils.get_non_terminals(gramatica)
    slr_table = SLRTable()

    slr_table.populate(estados, transicoes, follows, non_terminals)
    
    print(f' Tabela SLR da gramática:')
    for x, y in slr_table.table.items():
        if y.action_type == 'reduce':
            print(f' Estado {x[0]}, símbolo {x[1]} -> ação {y.action_type} por {y.transicao[0]}')
        else:
            print(f' Estado {x[0]}, símbolo {x[1]} -> ação {y.action_type} por {y.transicao}')
    print("\n")

    input = get_tokens_from_file(token_list)

    analysis_result = parser.LR_parsing(input, slr_table.table)

    print(f' Lista de tokens em análise:')
    for item in input:
        print(item)
    print("\n")

    if analysis_result:
        print("A palavra pertence à linguagem!")
    else:
        print("Erro de análise.")


if __name__ == "__main__":
    main()
    sys.exit(0)