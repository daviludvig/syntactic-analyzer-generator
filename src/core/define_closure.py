from model.symbol_table import TokenType, RegexToken
import core.regex_parser as regex_parser
from typing import List, Set


def define_closure(
    input_state: TokenType, tokenTypes: List[TokenType], production_index: int
) -> Set[TokenType]:
    closure_set = set()
    visited = set()
    symbol_stack = []

    def expand(state: TokenType):
        if state in visited:
            return
        visited.add(state)
        closure_set.add(state)

        # Encontra posição do ponto
        regex = state.regex
        dot_index = -1
        for i, tok in enumerate(regex):
            if tok.type == RegexToken.SLR_DOT:
                dot_index = i
                break

        if dot_index == -1 or dot_index + 1 >= len(regex):
            return

        next_tok = regex[dot_index + 1]
        if next_tok.type == RegexToken.REF:
            next_non_terminal = next_tok.value
            for i, prod in enumerate(tokenTypes):
                if prod.name == next_non_terminal:
                    # Cria uma nova regex com ponto no início
                    new_regex = [RegexToken(RegexToken.SLR_DOT, ".")] + prod.regex
                    new_token = TokenType(
                        prod.name, new_regex, prod.dfa.copy() if prod.dfa else None
                    )

                    expand(new_token)

    # Começa com a produção de índice production_index
    if production_index < 0 or production_index >= len(tokenTypes):
        raise ValueError(f"Índice inválido da produção: {production_index}")

    initial = tokenTypes[production_index]
    # Garantir que o ponto está inserido na cópia
    initial_with_dot = TokenType(
        initial.name,
        [RegexToken(RegexToken.SLR_DOT, ".")] + initial.regex,
        initial.dfa.copy() if initial.dfa else None,
    )
    expand(initial_with_dot)

    return closure_set
