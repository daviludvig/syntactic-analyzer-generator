import core.source_parser as source_parser
import core.NFAtoDFA as nfa_to_dfa
import core.union as union
from core.shunting_yard import shunting_yard
from core.regex_parser import get_regex_from_file, resolve_references_add_concats
from core.nfa_builder import NFAFromRegex
import model
import model.symbol_table

def main():
    
    print(f"Exemplo de análise de código fonte com NFA e DFA")
    print(f"Construindo NFA e DFA a partir de expressões regulares definidas em arquivo inputs/main_regex.txt")
    print(f"Analisando código fonte definido no arquivo inputs/main_source.txt\n")
    
    # Cria uma lista de DFAs, começando com um DFA inicial vazio (irá armazenar o resultado da união de todos os DFAs)
    dfas = []
    dfa_inicial = None
    dfas.append(dfa_inicial)

    # Lê as expressões regulares do arquivo e constrói os DFAs correspondentes
    tokentypes_non_concat_non_resolved_from_regex_file = get_regex_from_file("inputs/main_regex.txt")
    tokentypes_concat_resolved_from_regex_file = resolve_references_add_concats(tokentypes_non_concat_non_resolved_from_regex_file)
    for tokentype in tokentypes_concat_resolved_from_regex_file:
        postfix_ = shunting_yard(tokentype.regex)
        nfa_ = NFAFromRegex(postfix_).build()
        dfa_ = nfa_to_dfa.NFAtoDFA(nfa_)
        dfa_.name = tokentype.name
        dfas.append(dfa_)

    # Realiza a união de todos os DFAs, começando com o primeiro DFA
    dfas[0] = dfas[1]._cloneWithPrefix("cl1_")
    for i in range(2, len(dfas)):
        dfas[0] = nfa_to_dfa.NFAtoDFA(union.union(dfas[0], dfas[i]))
    
    symbol_table = model.symbol_table.SymbolTable()
    
    # Análise do código fonte
    tokens = source_parser.parse_source_code_from_file("inputs/main_source.txt", dfas, symbol_table)
    for token in tokens:
        print(f"<{token.lexeme}, {token.tokentype}>")

if __name__ == "__main__":
    main()