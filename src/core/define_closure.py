from model.symbol_table import TokenType, RegexToken
import core.regex_parser as regex_parser
from typing import List, Set


def find_dot_in_regex(regex: list[RegexToken]) -> int:
    """Encontra a posição do ponto (.) na regex."""
    for i, token in enumerate(regex):
        if token.type == RegexToken.SLR_DOT:
            return i
    return -1


def define_closure(
    input_state: TokenType, tokenTypes: List[TokenType]
) -> Set[TokenType]:
    """
    Calcula o conjunto closure de um item (TokenType com ponto).
    """
    closure_set = set()
    visited = set()

    # Função recursiva para expandir o closure
    def expand(state: TokenType):
        # Se o estado já foi visitado, não expande novamente
        if state in visited:
            return
        # Marca o estado como visitado e adiciona ao closure
        visited.add(state)
        closure_set.add(state)

        # Encontra a posição do ponto
        regex = state.regex
        dot_index = find_dot_in_regex(regex)

        # Se não há ponto ou ele está no final, não expande
        if dot_index == -1 or dot_index + 1 >= len(regex):
            return

        # Obtém o símbolo imediatamente após o ponto
        next_tok = regex[dot_index + 1]

        # Se o símbolo após o ponto é um não terminal (REF), expande
        if next_tok.type == RegexToken.REF:
            # Obtém o nome do próximo não terminal
            next_non_terminal = next_tok.value
            # Para cada produção original
            for prod in tokenTypes:
                # Se a cabeça de produção corresponde ao não terminal armazenado
                if prod.name == next_non_terminal:
                    # Cria novo item com ponto no início
                    new_regex = [RegexToken(RegexToken.SLR_DOT, ".")] + prod.regex
                    new_token = TokenType(
                        prod.name, new_regex, prod.dfa.copy() if prod.dfa else None
                    )
                    expand(new_token)

    # Começa com o estado recebido
    expand(input_state)

    return closure_set
