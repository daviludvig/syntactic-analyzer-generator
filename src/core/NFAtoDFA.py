# Code based on: https://viterbi-web.usc.edu/~breichar/teaching/2011cs360/NFAtoDFA.py
# Adapted by: Bruno, Davi, Julia Gazolla
import model.fa as fa
import model.dfa as dfa
import model.nfa as nfa

def NFAtoDFA(nfa: nfa.FA) -> dfa.DFA:
    """ Converte um autômato não determinístico em autômato determinístico.   
        O autômato de saída possui um estado para cada subconjunto de estados alcançável da entrada.
    """

    epsilon_cache = {}

    # Função auxiliar para otimizar e-fecho
    def cached_epsilon_closure(states):
        key = frozenset(states)
        if key not in epsilon_cache:
            epsilon_cache[key] = nfa.epsilon_closure(states)
        return epsilon_cache[key]
    
    deltaHat_cache = {}

    # Função auxiliar para otimizar deltaHat
    def cached_deltaHat(q, a):
        key = (q, a)
        if key not in deltaHat_cache:
            deltaHat_cache[key] = nfa.deltaHat(q, a)
        return deltaHat_cache[key]


    # Cria um frozenset do e-fecho de estado inicial para poder usar como chave em dicionários
    qo_closure = cached_epsilon_closure([nfa.initial_state])
    q0 = frozenset(qo_closure)  

    # Conjunto de estados do novo autômato
    Q = set([q0])
    # Conjunto de estados que ainda não foram processados quanto a transições
    unprocessedQ = Q.copy() 

    # Transições
    delta = {}

    # Estados finais
    F = []

    DFA_alphabet = nfa.alphabet - {"&"}


    # Enquanto os estados não forem marcados
    while unprocessedQ: 

        # Retira um subconjunto de estados dos que não foram marcados e processa suas transições
        qSet = unprocessedQ.pop()

        # Transições do subconjunto de estados
        delta[qSet] = {}

        # Para símbolo do alfabeto do autômato determinístico, verifica as transições
        for a in DFA_alphabet:
            moveResult = set()

            # Para cada estado do subconjunto
            for q in qSet:
                try:
                   moveResult |= cached_deltaHat(q, a)
                except KeyError:
                    pass
            if moveResult:
                nextStates = frozenset(cached_epsilon_closure(moveResult))
            else:
                nextStates = frozenset()
            
            delta[qSet][a] = nextStates
            if nextStates and nextStates not in Q:
                Q.add(nextStates)
                unprocessedQ.add(nextStates)

    for qSet in Q: 
        # Verifica se o estado final da NFA está naquele novo estado
        if (qSet & nfa.final_states): 
            F.append(qSet)

    # Inicializa elementos do novo autômato determinístico
    final_DFA = dfa.DFA(DFA_alphabet)
    DFA_states = set()
    DFA_transitions = set()
    subset_to_state = {}
    i = 0

    # Cria objetos estado do autômato determinístico
    for j, subset in enumerate(Q):

        is_initial = (subset == q0)
        is_final = bool(subset & nfa.final_states)

        if len(subset) > 0:
            qi = fa.State(name='q' + str(i), is_initial=is_initial, is_final=is_final)
            DFA_states.add(qi)
            subset_to_state[subset] = qi
            i+=1

    # Cria objetos transições do autômato determinístico
    for subset in Q:

        for s in DFA_alphabet:
            next_subset = delta[subset][s]
            if next_subset == frozenset():
                continue

            source_state = subset_to_state[subset]
            target_state = subset_to_state[next_subset]
            ti: fa.Transition = fa.Transition(source_state=source_state, input_symbol=s, target_state=target_state)
            DFA_transitions.add(ti)

    # Adiciona os objetos para o autômato determinístico
    final_DFA.addStates(DFA_states)
    final_DFA.addTransitions(DFA_transitions)

    return final_DFA