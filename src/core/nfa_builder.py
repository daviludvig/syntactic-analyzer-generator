from core.regex_parser import RegexToken
from model.nfa import NFA
from model.fa import State, Transition
from typing import List
import itertools

class NFAFromRegex:
    def __init__(self, postfix_tokens: List[RegexToken]) -> None:
        self.postfix_tokens = postfix_tokens
        self.state_id_counter = itertools.count()

    def new_state(self, is_initial=False, is_final=False) -> State:
        return State(name=f"q{next(self.state_id_counter)}", is_initial=is_initial, is_final=is_final)

    def build(self) -> NFA:
        stack: List[NFA] = []
        for token in self.postfix_tokens:
            if token.type == 'CHAR':
                nfa = self._build_char_nfa(token.value)
                stack.append(nfa)
            elif token.type == '*':
                # Aplica fecho de Kleene ao autômato parcial do topo da pilha
                nfa = stack.pop()
                stack.append(self._kleene_star(nfa))
            elif token.type == '|':
                # Aplica união aos dois autômatos parciais do topo da pilha
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._union(nfa1, nfa2))
            elif token.type == '.':
                # Aplica concatenação aos dois autômatos parciais do topo da pilha
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._concat(nfa1, nfa2))
            elif token.type == '+':
                # Clona o autômato do topo da pilha, aplica fecho de Kleene ao clone, e concatena o original com o clone
                base = stack.pop()
                clone = base._cloneWithPrefix("cl")
                kleene = self._kleene_star(clone)
                stack.append(self._concat(base, kleene))
            elif token.type == '?':
                # Aplica operador opcional ao autômato parcial do topo da pilha
                nfa = stack.pop()
                stack.append(self._optional(nfa))

        # Só termina se sobrar somente um autômato no fim do processo
        if len(stack) != 1:
            raise ValueError("Expressão pós-fixada está mal-formada.")

        return stack[0]

    # Cria um autômato com apenas dois estados, e uma transição pelo caractere encontrado (ou um conjunto vazio para &)
    def _build_char_nfa(self, char: str) -> NFA:
        nfa = NFA({char} if char != '&' else set())
        s0 = self.new_state(is_initial=True)
        s1 = self.new_state(is_final=True)

        nfa.addStates({s0, s1})
        nfa.addTransition(Transition(s0, char, s1))
        return nfa

    # Cria um novo autômato que é o fecho de Kleene do autômato de entrada
    def _kleene_star(self, nfa: NFA) -> NFA:
        epsilon = '&'
        result = NFA(nfa.alphabet.copy())

        # Cria novos estados inicial e final
        start = self.new_state(is_initial=True)
        end = self.new_state(is_final=True)
        result.addStates({start, end})

        # Desabilita estado inicial do autômato original
        nfa._disableInitialState()

        # Adiciona ao novo autômato todos os estados e transições do autômato original
        for state in nfa.states:
            result.addState(state)
        for t in nfa.transitions:
            result.addTransition(t)

        # Adiciona epsilon-transições do novo estado inicial para o antigo e para o novo estado final
        result.addTransition(Transition(start, epsilon, nfa.initial_state))
        result.addTransition(Transition(start, epsilon, end))

        # Adiciona epsilon-transições dos antigo estados finais para o antigo estado inicial e para o novo estado final
        for f in nfa.final_states:
            f.is_final = False
            result.addTransition(Transition(f, epsilon, nfa.initial_state))
            result.addTransition(Transition(f, epsilon, end))
        
        result.final_states = {end}

        return result

    # Cria um novo autômato que é a união dos autômatos de entrada
    def _union(self, a: NFA, b: NFA) -> NFA:
        epsilon = '&'
        result = NFA(a.alphabet.union(b.alphabet))

        # Cria novos estados inicial e final
        start = self.new_state(is_initial=True)
        end = self.new_state(is_final=True)
        result.addStates({start, end})

        # Desabilita estados iniciais dos autômatos originais
        a._disableInitialState()
        b._disableInitialState()

        # Adiciona ao novo autômato todos os estados e transições dos autômatos originais
        for state in a.states.union(b.states):
            result.addState(state)
        for t in a.transitions.union(b.transitions):
            result.addTransition(t)

        # Adiciona epsilon-transições do novo estado inicial para os dois antigos
        result.addTransition(Transition(start, epsilon, a.initial_state))
        result.addTransition(Transition(start, epsilon, b.initial_state))

        # Adiciona epsilon-transições para o novo estado final
        for f in a.final_states.union(b.final_states):
            f.is_final = False
            result.addTransition(Transition(f, epsilon, end))

        result.final_states = {end}

        return result

    # Cria um novo autômato que é a concatenação dos autômatos de entrada
    def _concat(self, a: NFA, b: NFA) -> NFA:
        epsilon = '&'
        result = NFA(a.alphabet.union(b.alphabet))

        # Desabilita estados iniciais dos autômatos originais
        a._disableInitialState()
        b._disableInitialState()

        # Adiciona ao novo autômato todos os estados e transições dos autômatos originais
        for state in a.states.union(b.states):
            result.addState(state)
        for t in a.transitions.union(b.transitions):
            result.addTransition(t)

        # O estado inicial do novo autômato é o estado inicial do primeiro elemento da concatenação
        result.initial_state = a.initial_state

        # Adiciona uma epsilon-transição de cada estado final do primeiro autômato para o estado inicial do segundo
        for f in a.final_states:
            f.is_final = False
            result.addTransition(Transition(f, epsilon, b.initial_state))

        # O estado final do novo autômato é o estado final do segundo elemento da concatenação
        result.final_states = set()
        for f in b.final_states:
            f.is_final = True
            result.final_states.add(f)

        return result

    # Cria um novo autômato que é a união do autômato de entrada com um autômato que aceita a palavra vazia (operador opcional '?')
    def _optional(self, nfa: NFA) -> NFA:
        epsilon = '&'
        result = NFA(nfa.alphabet.copy())

        # Cria novos estados inicial e final
        start = self.new_state(is_initial=True)
        end = self.new_state(is_final=True)
        result.addStates({start, end})

        # Desabilita estado inicial do autômato original
        nfa._disableInitialState()

        # Adiciona ao novo autômato todos os estados e transições do autômato original
        for state in nfa.states:
            result.addState(state)
        for t in nfa.transitions:
            result.addTransition(t)

        # Adiciona epsilon-transições como na união usual
        result.addTransition(Transition(start, epsilon, nfa.initial_state))
        result.addTransition(Transition(start, epsilon, end))

        # Adiciona epsilon-transições para o novo estado final
        for f in nfa.final_states:
            f.is_final = False
            result.addTransition(Transition(f, epsilon, end))

        result.final_states = {end}

        return result