import sys
import os
from typing import Set, Tuple, FrozenSet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core.regex_parser as regex_parser
import core.goto as goto
import core.define_closure as define_closure
from model.symbol_table import RegexToken, TokenType
from collections import deque


def get_canonical_items(
    tokentypes: list[TokenType],
    terminals: set[str],
    non_terminals: set[str]
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
            estado_goto_raw = goto.goto(estado_atual, simbolo, terminals, non_terminals, f"I{id_atual}")
            print(">> Raw ",estado_goto_raw)

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

    # Impressão opcional para debug
    for i, estado in enumerate(estados):
        print(f"\nEstado I{i}:")
        for tok in estado:
            print(f"  {tok.name}: {' '.join(str(token.value) for token in tok.regex if token.value is not None)}")

    print("\nTransições (GOTO):")
    for (origem, simbolo), destino in transicoes.items():
        print(f"  GOTO(I{origem}, {simbolo}) = I{destino}")

    return estados, transicoes


# === GRAMÁTICA ===
terminals = {"mais", "vezes", "id", "(", ")"}
non_terminals = {"E", "E'", "T", "F"}
grammar = [
    "E':== <E>",
    "E:==<E>mais<T>",
    "E:==<T>",
    "T:==<T>vezes<F>",
    "T:==<F>",
    "F:==(<E>)",
    "F:==id",
]

# grammar = [
#     "S':== <S>",
#     "S:== <S> or <A>",
#     "S:== <A>",
#     "A:== <A> and <B>",
#     "A:== <B>",
#     "B:== not <B>",
#     "B:== (<S>)",
#     "B:== true",
#     "B:== false",
# ]
# terminals = {"or", "and", "not", "true", "false", "(", ")"}
# non_terminals = {"S", "A", "B", "S'"}

# Gerar TokenTypes
tokentypes = regex_parser.get_regex_from_lines(grammar)
tokentypes[0].regex.insert(0, RegexToken(RegexToken.SLR_DOT, "."))  # Adiciona o ponto na primeira produção

get_canonical_items(tokentypes, terminals, non_terminals)


# i0 = define_closure.define_closure(tokentypes_copy[0], tokentypes)
# print(tokentypes[0])

# for tokentype in i0:
#     print(tokentype.name, ":", tokentype.regex)

# print("\n\n")

# goto_i0_e = goto.goto(i0, "E", terminals, non_terminals, "i0")
# i1 = set()
# for tokentype in goto_i0_e:
#     tokentype_closure = define_closure.define_closure(tokentype, tokentypes)
#     i1.update(tokentype_closure)
    
# print("i1:")
# for tokentype in i1:
#     print(tokentype.name, ":", tokentype.regex)
    
    
# goto_i1_mais = goto.goto(i1, "mais", terminals, non_terminals, "i1")
# i2 = set()
# for tokentype in goto_i1_mais:
#     tokentype_closure = define_closure.define_closure(tokentype, tokentypes)
#     i2.update(tokentype_closure)
    
# print("\ni2:")
# for tokentype in i2:
#     print(tokentype.name, ":", tokentype.regex)
