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


def goto(i: Set[TokenType], x_symbol: str) -> Set[TokenType]:
    # Cria um novo conjunto de TokenTypes para armazenar os resultados
    new_tokentypes = set()

    # Para cada produção dentro do item
    for tokentype in i:
        # Pega o regex da produção que está sendo analisada
        regex = tokentype.regex
        dot_index = find_dot_in_regex(regex)
        # Se não houver ponto ou se o ponto for o último símbolo, pula para a próxima produção
        if dot_index == -1 or dot_index + 1 >= len(regex):
            continue

        # Obtém o símbolo imediatamente após o ponto
        next_token = regex[dot_index + 1]

        # Se o símbolo após o ponto corresponde ao símbolo de transição esperado
        if next_token.value == x_symbol:
            # Cria uma nova regex com o ponto movido para a direita
            new_regex = (
                regex[:dot_index]
                + [next_token, RegexToken(RegexToken.SLR_DOT, ".")]
                + regex[dot_index + 2 :]
            )
            # Adiciona a nova produção ao conjunto de TokenTypes
            new_tokentypes.add(
                TokenType(
                    tokentype.name,
                    new_regex,
                    tokentype.dfa.copy() if tokentype.dfa else None,
                )
            )

    return new_tokentypes
