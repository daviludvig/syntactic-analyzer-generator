"""

Algorithm 4.44 : LR-parsing algorithm. 
INPUT: An input string w and an LR-parsing table with functions ACTION and 
GOT0 for a grammar G. 
OUTPUT: If w is in L(G), the reduction steps of a bottom-up parse for w; 
otherwise, an error indication. 
METHOD: Initially, the parser has so on its stack, where so is the initial state, 
and w$ in the input buffer. The parser then executes the program in Fig. 4.36. 


let a be the first symbol of w$;
while(1) {
    let s be the state on top of the stack;
    if (action[s, a] = shift t) {
        push t onto the stack;
        let a be the next input symbol;
    } else if (action[s, a] = reduce A -> β) {
        pop |β| symbols from the stack;
        let state t now be on top of the stack;
        push goto(t, A) onto the stack;
        output the production A -> β;
    } else if (action[s, a] = accept) break;
    else call error-recovery routine;
}

Leitura sobre LR-Parsing Algorithm
Pag 271 do pdf

É o procedimento de avaliar palavras. 
Existe: entrada, saída, pilha de estados, tabela com ação/goto

a pilha inicia com [I0, $] (confirmar)

cada estado é alcançado por um único símbolo X; portanto, todo estaedo existe um X assiciado. Mas o mesmo X pode estar associado a mais de um estado.
Ou seja, o símbolo da gramatica que representa o estado é aquele que faz chegar no estado. Sendo assim I0 não tem isso

"""
"""
def LR_parsing():

    # Para cada símbolo na entrada, iniciando pelo mais a direita

        # Selecionar o primeiro estado na lista de estados, mais a direita

        # Buscar a correspondencia [simbolo entrada, estado atual] na tabela de símbolos

            # Se a ação for shift:

                #


            # Se a ação for reduce:


            # Se a ação for accept


            # Caso contrário : ERROR - a palavra não pertence a gramática

    # Se a redução deu certo, deve retornar o símbolo inicial da gramatica
    return 0
"""

"""Sugestão com dict"""

def LR_parsing(input_dict, ACTION, GOTO, initial_state=0):
    states_dict = {0: initial_state}
    states_dict_top = 0
    input_ptr = 0

    while True:

        # Seleciona o primeiro estado
        state = states_dict[states_dict_top] 
        # Seleciona o primeiro simbolo da entrada
        symbol = input_dict.get(input_ptr)

        # Seleciona a cédula da tabela que contem essa combinação - AJUSTE TABELA
        action = ACTION.get((state, symbol))

        if action is None:
            print(f"Erro de sintaxe: ação indefinida para (estado {state}, símbolo '{symbol}')")
            return False

        if action[0] == 'shift':
            t = action[1]                   # AJUSTE TABELA
            states_dict_top += 1
            # Inclui no dicionário o estado alcançado, no próximo índice
            states_dict[states_dict_top] = t
            # Aponta para o próximo simbolo da entrada
            input_ptr += 1
            print(f"Shift: símbolo '{symbol}' → estado {t}")

        elif action[0] == 'reduce':
            # É o estado reduzido e a produção correspondente
            A, beta = action[1], action[2]          # AJUSTE TABELA
            # Verifica o tamanho da produção
            pop_len = len(beta)
            # Retira estados da fila
            states_dict_top = states_dict_top - pop_len
            if states_dict_top < 0:
                print("Erro: underflow na pilha.")
                return False
            # Ajusta qual é o estado em análise
            t = states_dict[states_dict_top]
            # Verifica para onde esse estado vai com a ação do reduce
            goto_state = GOTO.get((t, A))                   # AJUSTE TABELA
            if goto_state is None:
                print(f"Erro: goto indefinido para (estado {t}, não-terminal '{A}')")
                return False
            # Ajusta o ponteiro do estado atual em análise
            states_dict_top += 1
            # Inclui no dicionario o estado alcançado
            states_dict[states_dict_top] = goto_state
            print(f"Reduce: {A} → {' '.join(beta)}")

        elif action[0] == 'accept':
            print("Aceito: a palavra pertence à linguagem!")
            return True

        else:
            print("Erro de análise.")
            return False