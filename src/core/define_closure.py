from model.symbol_table import TokenType, RegexToken
import core.regex_parser as regex_parser
from typing import List, Set


def define_closure(
    input_state: TokenType, tokenTypes: List[TokenType], production_index: int
) -> Set[TokenType]:
    
    # Conjunto resultado da ação do algoritmo closure
    closure_set = set()
    visited = set()
    symbol_stack = []

    def expand(state: TokenType):
        # Se o estado já foi visitado, já foi expandido
        if state in visited:
            return
        visited.add(state)
        # Se o estado será expandido, significa que faz parte do conjunto final
        closure_set.add(state)

        # Encontra posição do ponto
        regex = state.regex
        dot_index = -1
        # Para cada item na regex, localiza a posição do ponto.
        for i, tok in enumerate(regex):
            if tok.type == RegexToken.SLR_DOT:
                dot_index = i
                break
        
        # Se o ponto não existe ou está no final, não precisa expandir
        if dot_index == -1 or dot_index + 1 >= len(regex):
            return

        next_tok = regex[dot_index + 1]
        # Se o item após o ponto é um não terminal
        if next_tok.type == RegexToken.REF:
            next_non_terminal = next_tok.value
            # Busca aquele não terminal em todos itens da gramática
            for i, prod in enumerate(tokenTypes):
                if prod.name == next_non_terminal:
                    # Cria uma nova regex com ponto no início
                    # E se a regex nova já existir??
                    new_regex = [RegexToken(RegexToken.SLR_DOT, ".")] + prod.regex
                    new_token = TokenType(
                        prod.name, new_regex, prod.dfa.copy() if prod.dfa else None
                    )

                    expand(new_token)
        
        # E se o item apos o ponto é um terminal??

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
