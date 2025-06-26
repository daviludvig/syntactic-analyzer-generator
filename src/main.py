import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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


def format_slr_table(slr_table_obj: SLRTable) -> str:
    # Coleta todos os símbolos e estados
    col_symbols = sorted({symbol for (_, symbol) in slr_table_obj.table.keys()})
    states = sorted({state for (state, _) in slr_table_obj.table.keys()})

    # Cabeçalho da tabela
    table_data = []
    header = ["Estado"] + col_symbols
    table_data.append(header)

    # Preenche a matriz da tabela
    for state in states:
        row = [str(state)]
        for symbol in col_symbols:
            action = slr_table_obj.table.get((state, symbol))
            if action is None:
                row.append("")
            elif action.action_type == "shift":
                # Shift é representado como S<transição>
                row.append(f"S{action.transicao}")
            elif action.action_type == "reduce":
                # Reduce é representado como R<transição>
                row.append(f"R{action.transicao[1]}")
            elif action.action_type == "accept":
                # Accept é representado como "acc"
                row.append("acc")
            elif action.action_type == "goto":
                # Goto é representado como <transição>
                row.append(str(action.transicao))
            else:
                row.append("?")
        table_data.append(row)

    # Calcula largura de cada coluna
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table_data)]

    # Constrói string formatada
    formatted = ""
    for row in table_data:
        formatted += (
            " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
            + "\n"
        )

    return formatted


def write_in_files(firsts, follows, slr_table, final_analysis, estados, transicoes) -> None:
    """
    Escreve os resultados encontrados em um arquivo de saída.
    """
    first_output_str = ""
    for key, value in firsts.items():
        if not value == set():
            first_output_str += f"  Símbolo {key} : FIRST = {value}\n"
    utils.write_in_file(f"{utils.OUTPUT_PATH_DIR}/firsts.txt", first_output_str)

    follow_output_str = ""
    for key, value in follows.items():
        if not value == set():
            follow_output_str += f"  Símbolo {key} : FOLLOW = {value}\n"
    utils.write_in_file(f"{utils.OUTPUT_PATH_DIR}/follows.txt", follow_output_str)
    
    tabela_formatada_str = format_slr_table(slr_table)
    utils.write_in_file(f"{utils.OUTPUT_PATH_DIR}/slr_table.txt", tabela_formatada_str)
    
    if final_analysis:
        utils.write_in_file(
            f"{utils.OUTPUT_PATH_DIR}/analysis_result.txt", "[OK] A palavra pertence à linguagem!"
        )
    else:
        utils.write_in_file(
            f"{utils.OUTPUT_PATH_DIR}/analysis_result.txt", "[X] Erro de análise."
        )
        
    formatted_canonical_collection = utils.format_canonical_collection(estados, transicoes)
    utils.write_in_file(f"{utils.OUTPUT_PATH_DIR}/canonical_collection.txt", formatted_canonical_collection)


def main() -> None:
    """
    Função principal que executa o analisador sintático.
    Lê os arquivos de lista de tokens e gramática, calcula first e follow da gramática, faz tabela SLR e verifica se a entrada é válida.
    Uso: python src/main.py <main_rules> <token_list>
    """
    if len(sys.argv) != 3:
        print("Uso: python src/main.py <main_rules> <token_list>")
        sys.exit(1)

    main_rules = sys.argv[1]
    token_list = sys.argv[2]

    if not utils.file_exists(main_rules) or not utils.file_exists(token_list):
        print(
            f"[Erro] Arquivo de entrada ou gramática não encontrado:\n  - {main_rules}\n  - {token_list}"
        )
        sys.exit(1)

    gramatica = get_grammar_from_file(main_rules)
    print("\n==================== GRAMÁTICA ====================")
    for linha in gramatica:
        print(f"  {linha}")
    print("===================================================\n")

    tokentypes = regex_parser.get_regex_from_lines(gramatica)

    tokentypes_copy = tokentypes.copy()
    tokentypes_copy[0].regex.insert(
        0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, ".")
    )  # Adiciona o ponto na primeira produção
    estados, transicoes = get_canonical_items.get_canonical_items(tokentypes_copy, "S")

    # FIRST
    firsts = define_first.define_first(tokentypes)
    print("==================== FIRST ====================")
    for key, value in firsts.items():
        if not value == set():
            print(f"  Símbolo {key} : FIRST = {value}")
    print("================================================\n")

    # FOLLOW
    follows = define_follow.define_follow(tokentypes, firsts, start_symbol="S")
    print("==================== FOLLOW ===================")
    for key, value in follows.items():
        if not value == set():
            print(f"  Símbolo {key} : FOLLOW = {value}")
    print("================================================\n")

    # SLR Table
    non_terminals = utils.get_non_terminals(gramatica)
    slr_table = SLRTable()
    slr_table.populate(estados, transicoes, follows, non_terminals)

    print("==================== TABELA SLR ==================")
    print(format_slr_table(slr_table))
    print("==================================================\n")

    # Entrada (tokens)
    input = get_tokens_from_file(token_list)
    print("==================== TOKENS DE ENTRADA ==================")
    for item in input:
        print(f"  {item}")
    print("=========================================================\n")

    # Análise sintática
    try:
        analysis_result = parser.LR_parsing(input, slr_table.table)
    except Exception as e:
        print("[X] Erro ao executar a análise sintática.")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {e}")
        analysis_result = False

    print("==================== RESULTADO ====================")
    if analysis_result:
        print("[OK] A palavra pertence à linguagem!")
    else:
        print("[X] Erro de análise.")
    print("===================================================\n")

    # Escreve os resultados em arquivos
    write_in_files(firsts, follows, slr_table, analysis_result, estados, transicoes)

if __name__ == "__main__":
    utils.prepare_output_directory()
    main()
    sys.exit(0)
