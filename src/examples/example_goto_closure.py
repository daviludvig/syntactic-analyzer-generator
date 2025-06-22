import sys
import os
import itertools

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core.regex_parser as regex_parser
import core.goto as goto
import core.define_closure as define_closure
from model.symbol_table import RegexToken, TokenType

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

tokentypes = regex_parser.get_regex_from_lines(grammar)
print ("DEBUG tokentypes " , tokentypes )

# === FUNÇÃO AUXILIAR PARA OBTER O ÍNDICE ORIGINAL DE UMA PRODUÇÃO ===
def get_original_index(item: TokenType, base_productions: list[TokenType]) -> int:
    regex_without_dot = [t for t in item.regex if t.type != RegexToken.SLR_DOT]
    for i, prod in enumerate(base_productions):
        if prod.name == item.name and prod.regex == regex_without_dot:
            return i
    raise ValueError(f"Produção não encontrada para o item: {item}")

# === ITEM INICIAL ===
start_index = 0
i0 = define_closure.define_closure(tokentypes[start_index], tokentypes, start_index)

print("DEBUG: i0: " , i0)

# === CONJUNTO CANÔNICO ===
canonical_items = {"i0": i0}
transitions = {}
state_queue = [("i0", i0)]
state_counter = itertools.count(start=1)

def state_exists(new_state):
    for name, state in canonical_items.items():
        if state == new_state:
            return name
    return None

# === CONSTRUÇÃO DOS ESTADOS ===
while state_queue:
    current_name, current_set = state_queue.pop(0)
    # Para todo simbolo terminal ou não terminal da gramatica
    for symbol in terminals.union(non_terminals):
        # Obter o go to para cada simbolo
        goto_result = goto.goto(current_set, symbol, terminals, non_terminals, current_name)
        if goto_result:
            closure_result = set()
            for item in goto_result:
                print("DEBUG go_to item " , item, " for symbol: ", symbol, " state: ", current_name)
                try:
                    prod_index = get_original_index(item, tokentypes)
                    closure_result.update(define_closure.define_closure(item, tokentypes, prod_index))
                    print("DEBUG closure result  " , closure_result)
                except ValueError:
                    continue

            existing_name = state_exists(closure_result)
            if existing_name is None:
                new_name = f"i{next(state_counter)}"
                canonical_items[new_name] = closure_result
                state_queue.append((new_name, closure_result))
                transitions[(current_name, symbol)] = new_name
            else:
                transitions[(current_name, symbol)] = existing_name

# === EXIBIÇÃO DOS ITENS ===
for state_name, item_set in canonical_items.items():
    print(f"Conjunto de itens {state_name}:")
    for tokentype in sorted(item_set, key=lambda t: t.name):
        print(f"  TokenType: {tokentype.name}, Regex: {tokentype.regex}")
    print()

print("Transições:")
for (src, symbol), dest in transitions.items():
    print(f"  {src} -- {symbol} --> {dest}")
