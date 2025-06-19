from typing import Union
from .fa import FA, State, Set

class NFA(FA):

    def __init__(self, alphabet : Set[str]) -> None:
        super().__init__(alphabet)
        self.epsilon = "&"

    # Calcula o e-fecho de um conjunto de estados
    def epsilon_closure(self, states: Set[State]) -> Set[State]:
        
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for transition in state.transitions:
                if transition.input_symbol == self.epsilon and transition.target_state not in closure:
                    closure.add(transition.target_state)
                    stack.append(transition.target_state)
        return closure

    # Verifica se uma entrada é válida nesse autômato não determinístico
    def isValidInput(self, input_str: str) -> bool:
        if self.initial_state is None:
            raise ValueError("Estado inicial não definido.")

        # Começa com o e-fecho do estado inicial
        current_states = self.epsilon_closure({self.initial_state})

        # Para cada símbolo da entrada
        for symbol in input_str:

            # Verifica se o símbolo faz parte do alfabeto 
            if symbol not in self.alphabet:
                raise ValueError(f"Símbolo inválido: {symbol}")

            found = False
            next_states = set()

            # Para cada estado do e-fecho
            for state in current_states:
                for transition in state.transitions:
                    # Se existe uma transição pelo símbolo que está na entrada, adiciona aos próximos estados
                    if transition.input_symbol == symbol:
                        next_states.add(transition.target_state)
                        
            # Aplica o e-fecho nos estados alcançados
            current_states = self.epsilon_closure(next_states)
            
            if next_states:
                found = True
                
            if not found:
                return False
            
        # Retorna verdadeiro se existir algum estado final no conjunto de próximos estados após percorrer todos síbolos da entrada
        return any(state.is_final for state in current_states)
    
    # Obtém o estado destino a partir de um estado inicial e transição
    def getDestinationStatesFromTransition(self, source_state: Union[State, str], symbol: str) -> Set[State]:
        source_state_obj = source_state
        if isinstance(source_state, str):
            source_state_obj = self._find_state_by_name(source_state)
        # Usa índice com lookup O(1)
        return self._transition_map.get(source_state_obj, {}).get(symbol, set())

    
    def deltaHat(self, states: Union[State, Set[State]], symbol: str) -> Set[State]:
        """
        Calcula o conjunto de estados alcançáveis a partir de um estado ou conjunto de estados,
        ao consumir um único símbolo do alfabeto, considerando transições-ε antes e depois.
        """
        if symbol not in self.alphabet:
            raise ValueError(f"Símbolo inválido: {symbol}")
        
        # Garante que 'states' seja um conjunto
        if isinstance(states, State):
            states = {states}

        # Aplica o e-fecho inicial
        current_states = self.epsilon_closure(states)

        # Realiza as transições pelo símbolo
        next_states = set()
        for st in current_states:
            destinations = self.getDestinationStatesFromTransition(st, symbol)
            next_states.update(destinations)

        # Aplica o e-fecho final
        result_states = self.epsilon_closure(next_states)

        return result_states
