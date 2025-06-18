import model.fa as fa
import model.nfa as nfa

def union(fa1: fa.FA, fa2: fa.FA) -> nfa.NFA:
    """
    Cria um novo autômato que aceita a união de duas linguagens aceitas por dois autômatos.

    Args:
        fa1 (FA): O primeiro autômato.
        fa2 (FA): O segundo autômato.

    Returns:
        NFA: Um novo autômato que aceita a união das linguagens de fa1 e fa2.
    """
    # Cria um novo autômato
    new_nfa = nfa.NFA(fa1.alphabet.union(fa2.alphabet))

    # Copia os alvos da union
    new_fa1 = fa1._cloneWithPrefix("fa1_")
    new_fa2 = fa2._cloneWithPrefix("fa2_")

    # Cria um novo estado inicial
    new_initial_state = fa.State(name="union_q0", is_final=False, is_initial=True)
    new_nfa.addState(new_initial_state)

    # Desativa os estados iniciais dos autômatos copiados
    new_fa1._disableInitialState()
    new_fa2._disableInitialState()

    # Adiciona todos os estados e transições do primeiro autômato
    new_nfa.addStates(new_fa1.states)
    new_nfa.addTransitions(new_fa1.transitions)

    # Adiciona todos os estados e transições do segundo autômato
    new_nfa.addStates(new_fa2.states)
    new_nfa.addTransitions(new_fa2.transitions)
    
    # Adiciona transições do novo estado inicial para os estados iniciais dos autômatos
    t1 : fa.Transition = fa.Transition(source_state=new_initial_state, input_symbol="&", target_state=new_fa1.initial_state)
    t2 : fa.Transition = fa.Transition(source_state=new_initial_state, input_symbol="&", target_state=new_fa2.initial_state)
    
    new_nfa.addTransitions({t1, t2})
    
    return new_nfa