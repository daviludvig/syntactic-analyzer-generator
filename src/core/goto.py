from typing import Set
from model.symbol_table import TokenType, RegexToken


def find_dot_in_regex(regex: list[RegexToken]) -> int:
    """Encontra a posição do ponto (.) na regex."""
    for i, token in enumerate(regex):
        if token.type == RegexToken.SLR_DOT:
            return i
    return -1


def get_element_after_dot(regex: list[RegexToken], dot_index: int) -> str:
    """Obtém o elemento imediatamente após o ponto (.) na regex."""
    if dot_index + 1 < len(regex):
        next_token = regex[dot_index + 1]
        if next_token.type == RegexToken.CHAR or next_token.type == RegexToken.REF:
            return next_token.value
    return None


def get_transitions_dot(tokentypes: Set[TokenType]) -> Set[str]:
    """Obtém os símbolos que podem ser alcançados a partir do ponto (.) em cada TokenType.
    Ex. T->.E, E->.id, E->.(E)
    Deve retornar {'E', 'id', '('}"""
    transitions = set()
    for tokentype in tokentypes:
        regex = tokentype.regex
        dot_index = find_dot_in_regex(regex)
        if dot_index != -1:
            element_after_dot = get_element_after_dot(regex, dot_index)
            if element_after_dot:
                transitions.add(element_after_dot)
    return transitions


def goto(i: Set[TokenType], x_symbol: str) -> Set[TokenType]:
    new_tokentypes = set()

    for tokentype in i:
        regex = tokentype.regex
        dot_index = find_dot_in_regex(regex)
        if dot_index == -1 or dot_index + 1 >= len(regex):
            continue

        next_token = regex[dot_index + 1]

        # Se o símbolo após o ponto corresponde ao símbolo de transição esperado
        if next_token.value == x_symbol:
            new_regex = (
                regex[:dot_index]
                + [next_token, RegexToken(RegexToken.SLR_DOT, ".")]
                + regex[dot_index + 2 :]
            )
            new_tokentypes.add(
                TokenType(
                    tokentype.name,
                    new_regex,
                    tokentype.dfa.copy() if tokentype.dfa else None,
                )
            )

    return new_tokentypes
