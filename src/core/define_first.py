'''
First
Pág 244

Computar o First(X) para todo não terminal da gramática

Se X é terminal, então First(X) = {X}.
Se X é não-terminal e X -> Y1Y2...Yn é uma produção, Então
Se Y1 é terminal, então First(X) = {Y1}.
Se Y1 é não-terminal, então First(X) = First(Y1) - {&}.
Se Y1 pode derivar &, então adiciona First(Y2) - {&} a First(X), e assim por diante até encontrar um Yk que não deriva & ou até n.
Se Y1, Y2, ..., Yn-1 podem derivar & e se Yn pode derivar em & então adiciona & a First(X).
Se X -> & é uma produção, então adiciona & a First(X).
Follow
Pag 244

Computar o Follow(X)

Se X é o símbolo inicial, então adiciona $ a Follow(X).
Se A -> αXβ é uma produção, então adiciona First(β) (menos &).
Se A -> αXβ e β pode derivar em &, então adiciona Follow(A) a Follow(X), faça o mesmo se A -> αX.
Considerar ordem para evitar recursividade ciclica infinita
'''

from __future__ import annotations
from . import utils

SEPARATOR = ':=='

def get_productions_from_file(file_path: str) -> dict():
    
    """
    Lê a grámatica no formato:
    <Não terminal> ::= <Corpo da produção>
    e retorna um dicionario em que a chave é o não terminal 
    e o valor é uma lista de produções daquele não terminal
    """
    lines = utils.get_file_lines(file_path)
    gr = {}


    if not lines:
        raise ValueError(f"O arquivo {file_path} está vazio ou não contém uma regex válida.")
    
    for line in lines:
        if SEPARATOR not in line:
            raise ValueError(f"Linha mal formatada: {line}")
        symbol, production = map(str.strip, line.split(SEPARATOR, 1))

        # Se não existe uma chave para o não terminal, adiciona a chave e a lista de produções na lista
        if symbol not in gr:
            gr[symbol] = [production]
        else:
            gr[symbol].append(production)


def define_first(grammar: dict) -> dict:
    gr_firsts = {}

    # Inicializa os conjuntos FIRST vazios para cada não-terminal
    for non_terminal in grammar:
        gr_firsts[non_terminal] = set()

    # Computa FIRSTs de todos os não-terminais
    for non_terminal in grammar:
        first(non_terminal, grammar, gr_firsts)

    return gr_firsts


# Função auxiliar para calcular o FIRST de um símbolo
def first(symbol, grammar, gr_firsts) -> set():

    # Caso base: terminal ou epsilon
    if symbol not in grammar:
        return {symbol}

    # Já foi computado
    if gr_firsts[symbol]:
        return gr_firsts[symbol]

    result = set()

    for production in grammar[symbol]:
        symbols = list(production)
        for i, sym in enumerate(symbols):
            sym_first = first(sym, grammar, gr_firsts)
            result.update(sym_first - {'&'})

            if '&' in sym_first:
                # Continua para o próximo símbolo
                if i == len(symbols) - 1:
                    result.add('&')
                continue
            else:
                break
        else:
                # Todos os símbolos da produção têm epsilon
            result.add('&')

    gr_firsts[symbol] = result
    return result

