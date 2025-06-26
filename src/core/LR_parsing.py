
from core.slr_table import Action

def LR_parsing(token_list, action_dict, initial_state=0):

    input_dict = {}

    # Coloca input em dict
    for i in range(len(token_list)):
        try:
            if token_list[i][1] == "PR":
                # Seleciona o lexema associado
                input_dict[i] = token_list[i][0]
            else:
                input_dict[i] = token_list[i][1].lower()
        except:
            print(f"Erro ao processar o token {i}: {token_list[i]}")
    input_dict[i+1] = "$"

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

        if action is None:
            return False

        if action.action_type == Action.SHIFT:
            t = action.transicao                   
            states_dict_top += 1
            # Inclui no dicionário o estado alcançado, no próximo índice
            states_dict[states_dict_top] = t
            # Aponta para o próximo simbolo da entrada
            input_ptr += 1

        elif action.action_type == Action.REDUCE:
            # É o estado reduzido e a produção correspondente
            head, pop_len = action.transicao[0], action.transicao[1]          
            # Retira estados da fila
            states_dict_top = states_dict_top - pop_len
            if states_dict_top < 0:
                return False
            # Ajusta qual é o estado em análise
            t = states_dict[states_dict_top]
            # Verifica para onde esse estado vai com a ação do reduce
            goto_action = action_dict[(t, head)]                
            if goto_action is None:
                return False
            # Ajusta o ponteiro do estado atual em análise
            states_dict_top += 1
            # Inclui no dicionario o estado alcançado
            states_dict[states_dict_top] = goto_action.transicao

        elif action.action_type == Action.ACCEPT:
            return True

        else:
            return False