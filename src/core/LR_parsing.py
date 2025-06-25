
from core.slr_table import SLRTable, Action

def LR_parsing(input_dict, action_dict, initial_state=0):
    states_dict = {0: initial_state}
    states_dict_top = 0
    input_ptr = 0

    while True:

        # Seleciona o primeiro estado
        state = states_dict[states_dict_top] 
        # Seleciona o primeiro simbolo da entrada
        symbol = input_dict.get(input_ptr)

        # Seleciona a cédula da tabela que contem essa combinação
        action = action_dict[(state, symbol)]
        print (f'debug {state} , {symbol} , {action}')

        if action is None:
            print(f"Erro de sintaxe: ação indefinida para (estado {state}, símbolo '{symbol}')")
            return False

        if action.action_type == Action.SHIFT:
            t = action.transicao                   
            states_dict_top += 1
            # Inclui no dicionário o estado alcançado, no próximo índice
            states_dict[states_dict_top] = t
            # Aponta para o próximo simbolo da entrada
            input_ptr += 1
            print(f"Shift: símbolo '{symbol}' → estado {t}")

        elif action.action_type == Action.REDUCE:
            # É o estado reduzido e a produção correspondente
            head, pop_len = action.transicao[0], action.transicao[1]          
            # Retira estados da fila
            states_dict_top = states_dict_top - pop_len
            if states_dict_top < 0:
                print("Erro: underflow na pilha.")
                return False
            # Ajusta qual é o estado em análise
            t = states_dict[states_dict_top]
            # Verifica para onde esse estado vai com a ação do reduce
            print(f'debug reduce {t}, {symbol}, {action_dict[(t, head)]}')
            goto_action = action_dict[(t, head)]                
            if goto_action is None:
                print(f"Erro: goto indefinido para (estado {t}, não-terminal '{head}')")
                return False
            # Ajusta o ponteiro do estado atual em análise
            states_dict_top += 1
            # Inclui no dicionario o estado alcançado
            states_dict[states_dict_top] = goto_action.transicao
            #print(f"Reduce: {head} → {' '.join(pop_len)}")

        elif action.action_type == Action.ACCEPT:
            print("Aceito: a palavra pertence à linguagem!")
            return True

        else:
            print("Erro de análise.")
            return False