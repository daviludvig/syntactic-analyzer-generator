from __future__ import annotations
from model.symbol_table import TokenType, RegexToken
from typing import List, Dict, Set


def define_follow(
    grammars_tokentypes: List[TokenType],
    gr_firsts: Dict[str, Set[str]],
    start_symbol: str,
) -> Dict[str, Set[str]]:

    gr_follows: Dict[str, Set[str]] = {t.name: set() for t in grammars_tokentypes}
    changed = [True]

    # Regra 1: símbolo inicial → $
    gr_follows[start_symbol].add("$")

    while changed[0]:
        changed[0] = False
        for grammar_tokentype in grammars_tokentypes:
            follow(
                grammar_tokentype,
                grammars_tokentypes,
                gr_follows,
                gr_firsts,
                changed,
            )

    return gr_follows


def follow(
    current_tokentype: TokenType,
    tokentypes: List[TokenType],
    gr_follows: Dict[str, Set[str]],
    gr_firsts: Dict[str, Set[str]],
    changed: List[bool],
) -> None:
    # É a cabeça da produção
    A = current_tokentype.name
    # É a produção
    production = current_tokentype.regex

    for i, token in enumerate(production):
        # Se for um não terminal
        if token.type == RegexToken.REF:
            B = token.value
            follow_B = gr_follows[B]
            original_size = len(follow_B)

            # β = produção após B
            beta = production[i + 1 :]

            # Regra 2
            first_beta = compute_first_of_sequence(beta, gr_firsts)
            follow_B.update(first_beta - {"&"})

            # Regra 3
            if "&" in first_beta or not beta:
                follow_B.update(gr_follows[A])

            if len(follow_B) > original_size:
                changed[0] = True


def compute_first_of_sequence(
    sequence: List[RegexToken], gr_firsts: Dict[str, Set[str]]
) -> Set[str]:

    result = set()
    nullable = True

    for token in sequence:
        # Se for um terminal
        if token.type == RegexToken.CHAR:
            result.add(token.value)
            nullable = False
            break
        # Se for um não terminal
        elif token.type == RegexToken.REF:
            token_first = gr_firsts.get(token.value, set())
            result.update(token_first - {"&"})
            if "&" in token_first:
                continue
            else:
                nullable = False
                break
        else:
            nullable = False
            break

    if nullable:
        result.add("&")

    return result
