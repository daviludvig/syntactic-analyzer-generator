from typing import Tuple, FrozenSet
import core.goto as goto
import core.define_closure as define_closure
from model.symbol_table import RegexToken, TokenType
from collections import deque
from core.slr_table import Action


def get_canonical_items(tokentypes: list[TokenType], start_symbol: str):

    # Cada estado será um conjunto imutável (frozenset) de TokenTypes
    estados: list[FrozenSet[TokenType]] = []
    # As transições serão um dicionário onde a chave é uma tupla (estado_atual, símbolo) e o valor é o estado de destino
    transicoes: dict[Tuple[int, str], int] = {}

    # Estado inicial: closure da primeira produção (**com ponto já adicionado**)
    i0 = define_closure.define_closure(tokentypes[0], tokentypes)
    estado_inicial = frozenset(i0)
    estados.append(estado_inicial)

    # Fila para explorar os estados
    # Usamos deque para eficiência na remoção do primeiro elemento
    # e na adição de novos estados
    fila = deque()
    # Fila começa com o i0 expandido
    fila.append(estado_inicial)

    # Enquanto houver estados na fila a serem processados
    while fila:
        # Pega o primeiro estado da fila
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
            estado_goto_raw = goto.goto(estado_atual, simbolo)

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

    # Adiciona a transição de aceitação
    # i0 -> start_symbol -> estado_destino -> $ -> Action.ACCEPT
    estado_destino = transicoes[(0, start_symbol)]
    transicoes[(estado_destino, "$")] = Action.ACCEPT
    return estados, transicoes
