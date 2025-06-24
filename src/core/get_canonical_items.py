from typing import Tuple, FrozenSet
import core.goto as goto
import core.define_closure as define_closure
from model.symbol_table import RegexToken, TokenType
from collections import deque
from core.slr_table import Action

def get_canonical_items(
    tokentypes: list[TokenType], terminals: set[str], non_terminals: set[str], start_symbol: str
):
    from copy import deepcopy

    # Cada estado será um conjunto imutável (frozenset) de TokenTypes
    estados: list[FrozenSet[TokenType]] = []
    transicoes: dict[Tuple[int, str], int] = {}

    # Estado inicial: closure da primeira produção (com ponto já adicionado)
    i0 = define_closure.define_closure(tokentypes[0], tokentypes)
    estado_inicial = frozenset(i0)
    estados.append(estado_inicial)

    fila = deque()
    fila.append(estado_inicial)

    while fila:
        estado_atual = fila.popleft()
        id_atual = estados.index(estado_atual)

        # Identifica todos os símbolos que aparecem imediatamente após o ponto
        simbolos_possiveis = set()
        for item in estado_atual:
            regex = item.regex
            for i in range(len(regex) - 1):
                if regex[i].type == RegexToken.SLR_DOT:
                    simbolo = regex[i + 1].value
                    simbolos_possiveis.add(simbolo)

        for simbolo in simbolos_possiveis:
            # Aplica GOTO ao estado atual com o símbolo
            estado_goto_raw = goto.goto(estado_atual, simbolo, terminals, non_terminals)
            print(">> Raw ", estado_goto_raw)

            # Aplica CLOSURE a cada produção do resultado do GOTO
            novo_estado = set()
            for item in estado_goto_raw:
                novo_estado.update(define_closure.define_closure(item, tokentypes))

            novo_estado_fs = frozenset(novo_estado)

            # Verifica se é um estado novo ou já existente
            if novo_estado_fs not in estados:
                estados.append(novo_estado_fs)
                fila.append(novo_estado_fs)

            id_destino = estados.index(novo_estado_fs)
            transicoes[(id_atual, simbolo)] = id_destino

    estado_destino = transicoes[(0,start_symbol)]
    transicoes[(estado_destino, "$")] = Action.ACCEPT
    return estados, transicoes
