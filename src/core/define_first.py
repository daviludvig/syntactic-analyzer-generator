from __future__ import annotations
from model.symbol_table import TokenType, RegexToken
from typing import List, Dict, Set


def define_first(grammars_tokentypes: list[TokenType]) -> Dict[str, Set[str]]:
    gr_firsts = {}

    # Para cada terminal da gramática
    for grammar_tokentype in grammars_tokentypes:
        # Ex. E:== e<T>
        # gr_firsts['E'] = set()
        # Cria um conjunto para os firsts desse terminal
        if grammar_tokentype.name not in gr_firsts:
            gr_firsts[grammar_tokentype.name] = set()

    # Obtem todos os firsts
    for grammar_tokentype in grammars_tokentypes:
        first(grammar_tokentype.name, grammars_tokentypes, gr_firsts)

    return gr_firsts


# Função auxiliar para calcular o FIRST de um símbolo
def first(
    name: str,
    tokentypes: List[TokenType],
    gr_firsts: Dict[str, Set[str]],
    visited: Set[str] = None,
) -> Set[str]:

    # Registra quais já foram visitados
    if visited is None:
        visited = set()

    if name in visited:
        return gr_firsts[name]  # evita recursão infinita

    # Adiciona aquele item Nao-terminal - produção na lista de visitados
    visited.add(name)
    curr_gr_firsts = gr_firsts[name]
    curr_tokentypes = [t for t in tokentypes if t.name == name]

    for curr_tokentype in curr_tokentypes:
        # Grammar é a produção
        grammar = curr_tokentype.regex
        nullable = True  # se todos os símbolos da produção podem gerar ε

        # Trata caso da produção ser ε
        if (
            len(grammar) == 1
            and grammar[0].type == RegexToken.CHAR
            and grammar[0].value == "&"
        ):
            curr_gr_firsts.add("&")
            continue

        i = 0
        while i < len(grammar):
            token = grammar[i]

            # Se a producao comeca com terminal
            if token.type == RegexToken.CHAR:
                # tenta formar o maior terminal possível com sequência de CHARs
                value = token.value

                if value:
                    curr_gr_firsts.add(value)
                    nullable = False
                    break
                else:
                    # se nem parte da sequência for reconhecida, assume como inválido
                    nullable = False
                    break
            #Se a producao comeca com um não terminal
            elif token.type == RegexToken.REF:
                ref_name = token.value
                ref_first = first(ref_name, tokentypes, gr_firsts, visited)
                curr_gr_firsts.update(ref_first - {"&"})

                if "&" in ref_first:
                    i += 1
                    continue  # tenta o próximo símbolo
                else:
                    nullable = False
                    break

            elif token.type == RegexToken.LPAREN:
                # comportamento básico para parênteses (pode ser estendido)
                for token in grammar[i + 1 :]:
                    if token.type == RegexToken.RPAREN:
                        break
                    if token.type == RegexToken.CHAR:
                        curr_gr_firsts.add(token.value)
                nullable = False
                break

            else:
                nullable = False
                break

        if nullable:
            curr_gr_firsts.add("&")

    visited.remove(name)
    return curr_gr_firsts
