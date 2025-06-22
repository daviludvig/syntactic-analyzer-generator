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

def goto(
    i: Set[TokenType], x_symbol: str, terminals: set[str], non_terminals: set[str], current_name
) -> Set[TokenType]:
    new_tokentypes = set()

    # Para cada item do estado em analise
    for tokentype in i:
        regex = tokentype.regex
        dot_index = find_dot_in_regex(regex)
        if dot_index == -1:
            print(
                f"TokenType {tokentype.name} does not contain a slr_dot (.) in its regex."
            )
            continue

        # Formar maior sequência de CHARs a partir da posição após o ponto
        # Caso em que o terminal é formado por mais de um char
        j = dot_index + 1
        composed = ""
        longest_match = None
        match_end = j

        while j < len(regex) and regex[j].type == RegexToken.CHAR:
            composed += regex[j].value
            if composed in terminals or composed in non_terminals:
                longest_match = composed
                match_end = j + 1  # posição logo após o último CHAR válido
            j += 1

        # Se encontrou um símbolo composto válido
        if longest_match == x_symbol:
            new_regex = (
                regex[:dot_index]
                + regex[dot_index + 1 : match_end]
                + [RegexToken(RegexToken.SLR_DOT, ".")]
                + regex[match_end:]
            )
            new_tokentypes.add(
                TokenType(
                    tokentype.name,
                    new_regex,
                    tokentype.dfa.copy() if tokentype.dfa else None,
                )
            )

        # Também trata símbolos simples do tipo REF ou CHAR (não compostos)
        elif dot_index + 1 < len(regex):
            token = regex[dot_index + 1]
            if token.type == RegexToken.REF or token.type == RegexToken.CHAR:
                if token.value == x_symbol:
                    # Move o ponto "."
                    new_regex = (
                        regex[:dot_index]
                        + [token]
                        + [RegexToken(RegexToken.SLR_DOT, ".")]
                        + regex[dot_index + 2 :]
                    )
                    new_tokentypes.add(
                        TokenType(
                            tokentype.name,
                            new_regex,
                            tokentype.dfa.copy() if tokentype.dfa else None,
                        )
                    )

    if not new_tokentypes:
        print(
            f"DEBUG i: {current_name} No valid transitions found for symbol '{x_symbol}' in the given token types."
        )
        return set()
    return new_tokentypes
