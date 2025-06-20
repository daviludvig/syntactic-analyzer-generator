"""
First
Pág 244

Computar o First(X) para todo não terminal da gramática

Se X é terminal, então First(X) = {X}.
Se X é não-terminal e X -> Y1Y2...Yn é uma produção, Então
Se Y1 é terminal, então First(X) = {Y1}.
Se Y1 é não-terminal, então First(X) = First(Y1) - {&}.
Se Y1 pode derivar &, então adiciona First(Y2) - {&} a First(X), e assim por diante até encontrar um Yk que não deriva & ou até n.
Se Y1, Y2, ..., Yn-1 podem derivar & e se Yn pode derivar em & então adiciona & a First(X).
Se X -> & é uma produção, então adiciona & a First(X).
Follow
Pag 244

Computar o Follow(X)

Se X é o símbolo inicial, então adiciona $ a Follow(X).
Se A -> αXβ é uma produção, então adiciona First(β) (menos &).
Se A -> αXβ e β pode derivar em &, então adiciona Follow(A) a Follow(X), faça o mesmo se A -> αX.
Considerar ordem para evitar recursividade ciclica infinita
"""

from __future__ import annotations
from . import utils
from model.symbol_table import TokenType, RegexToken
from typing import List, Dict, Set


def define_first(
    grammars_tokentypes: list[TokenType], terminals: Set[str]
) -> Dict[str, Set[str]]:
    gr_firsts = {}

    for grammar_tokentype in grammars_tokentypes:
        # Ex. E:== e<T>
        # gr_firsts['E'] = set()
        if grammar_tokentype.name not in gr_firsts:
            gr_firsts[grammar_tokentype.name] = set()

    for grammar_tokentype in grammars_tokentypes:
        first(
            grammar_tokentype.name, grammars_tokentypes, gr_firsts, terminals=terminals
        )

    print(gr_firsts)
    return gr_firsts


# Função auxiliar para calcular o FIRST de um símbolo
def first(
    name: str,
    tokentypes: List[TokenType],
    gr_firsts: Dict[str, Set[str]],
    terminals: Set[str],
    visited: Set[str] = None,
) -> Set[str]:

    if visited is None:
        visited = set()

    if name in visited:
        return gr_firsts[name]  # evita recursão infinita

    visited.add(name)
    curr_gr_firsts = gr_firsts[name]
    curr_tokentypes = [t for t in tokentypes if t.name == name]

    for curr_tokentype in curr_tokentypes:
        grammar = curr_tokentype.regex
        nullable = True  # se todos os símbolos da produção podem gerar ε

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

            if token.type == RegexToken.CHAR:
                # tenta formar o maior terminal possível com sequência de CHARs
                j = i
                composed = ""
                longest_match = None
                while j < len(grammar) and grammar[j].type == RegexToken.CHAR:
                    composed += grammar[j].value
                    if composed in terminals:
                        longest_match = composed
                    j += 1

                if longest_match:
                    curr_gr_firsts.add(longest_match)
                    nullable = False
                    break
                else:
                    # se nem parte da sequência for reconhecida, assume como inválido
                    nullable = False
                    break

            elif token.type == RegexToken.REF:
                ref_name = token.value
                ref_first = first(ref_name, tokentypes, gr_firsts, terminals, visited)
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
