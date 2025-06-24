from model.symbol_table import TokenType, RegexToken
import core.regex_parser as regex_parser
from typing import List, Set


def define_closure(
    input_state: TokenType, tokenTypes: List[TokenType]
) -> Set[TokenType]:
    """
    Calcula o conjunto closure de um item LR(0) (TokenType com ponto).
    """
    closure_set = set()
    visited = set()

    def expand(state: TokenType):
        if state in visited:
            return
        visited.add(state)
        closure_set.add(state)

        # Encontra a posição do ponto
        regex = state.regex
        dot_index = next(
            (i for i, tok in enumerate(regex) if tok.type == RegexToken.SLR_DOT), -1
        )

        # Se não há ponto ou ele está no final, não expande
        if dot_index == -1 or dot_index + 1 >= len(regex):
            return

        next_tok = regex[dot_index + 1]

        # Se o símbolo após o ponto é um não terminal (REF), expande
        if next_tok.type == RegexToken.REF:
            next_non_terminal = next_tok.value
            for prod in tokenTypes:
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
