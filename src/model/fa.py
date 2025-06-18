from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set, Dict, DefaultDict
from collections import defaultdict

class State:
    def __init__(self, name: str, is_initial: bool = False, is_final: bool = False) -> None:
        self.name : str = name                           # Nome ou identificador do estado (ex: "q0", "q1")
        self.is_initial : bool = is_initial              # Indica se é o estado inicial
        self.is_final : bool = is_final                  # Indica se é um estado de aceitação
        self.transitions : Set[Transition] = set()       # Conjunto de transições de um estado
        
    def __repr__(self) -> str:
        return f"State('{self.name}', initial={self.is_initial}, final={self.is_final})"
    
    # Adiciona transições para esse estado
    def addTransition(self, transition : Transition) -> None:
        """Adiciona uma transição à lista de transições do estado."""
        self.transitions.add(transition)
        
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
        
class Transition:
    def __init__(self, source_state : State = None, input_symbol: str = None, target_state : State = None):
        self.source_state : State = source_state   # Estado de origem da transição
        self.input_symbol : str = input_symbol     # Símbolo do alfabeto do autômato que aciona a transição (por exemplo, 'a', '0', etc.)
        self.target_state : State = target_state   # Estado de destino para o qual a transição leva
        
    def __repr__(self) -> str:
        return f"Transition(from '{self.source_state.name}' by '{self.input_symbol}' for '{self.target_state.name}')"

    def __eq__(self, other):
        if not isinstance(other, Transition):
            return False
        return (self.source_state == other.source_state and
                self.input_symbol == other.input_symbol and
                self.target_state == other.target_state)

    def __hash__(self):
        return hash((self.source_state, self.input_symbol, self.target_state))

class FA(ABC):

    def __init__(self, alphabet : Set[str], name = None) -> None:
        self.states: Set[State] = set()
        self.alphabet: Set[str] = alphabet
        self.final_states: Set[State] = set()
        self.initial_state: State = None
        self.transitions: Set[Transition] = set()
        self.name: str = name
        
        # Index de transições: {source_state: {symbol: set(target_states)}}
        self._transition_map: DefaultDict[State, DefaultDict[str, Set[State]]] = defaultdict(lambda: defaultdict(set))

    # Adiciona um conjunto de transições ao autômato
    def addTransitions(self, transitions : Set[Transition]) -> None:
        for transition in transitions:
            self.addTransition(transition)

    # Adiciona uma transição ao autômato
    def addTransition(self, transition : Transition) -> None:
        self.transitions.add(transition)
        transition.source_state.addTransition(transition)
        # Atualiza índice
        self._transition_map[transition.source_state][transition.input_symbol].add(transition.target_state)

    # Adiciona um conjunto de estados ao autômato    
    def addStates(self, states: Set[State]) -> None:
        for state in states:
            self.addState(state)
        
    # Adiciona um estado ao autômato    
    def addState(self, new_state: State) -> None:
        self.states.add(new_state)
        if new_state.is_initial:
            if self.initial_state is not None:
                raise ValueError("Automato já possui estado inicial.")
            self.initial_state = new_state
        if new_state.is_final:
            self.final_states.add(new_state)
    
    @abstractmethod
    def isValidInput(self, input : str) -> bool:
        """Processa uma cadeia de entrada e retorna se é aceita."""
        pass
    
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}(\n"
            f"  States: {[state.name for state in self.states]},\n"
            f"  Initial: {self.initial_state.name if self.initial_state else None},\n"
            f"  Finals: {[state.name for state in self.final_states]},\n"
            f"  Alphabet: {sorted(self.alphabet)},\n"
            f"  Transitions: \n  [\n    " +
            ",\n    ".join(
                f"{t.source_state.name} --{t.input_symbol}--> {t.target_state.name}"
                for t in self.transitions
            ) +
            "\n  ]\n"
            f")>"
        )
    
    def getTabularFormat(self) -> str:
        """Retorna a representação do autômato no formato jFlap."""
        transitions = sorted(self.transitions, key=lambda t: (t.source_state.name, t.input_symbol))
        
        output = []
        output.append(str(len(self.states)))  # Número de estados
        output.append(self.initial_state.name)  # Estado inicial
        output.append(",".join(sorted(s.name for s in self.final_states)))  # Estados finais
        output.append(",".join(sorted(self.alphabet)))  # Alfabeto
        
        for t in transitions:
            output.append(f"{t.source_state.name},{t.input_symbol},{t.target_state.name}")
    
        return "\n".join(output)

    # Copia um autômato existente, sendo que o novo autômato terá estados com um prefixo
    def _cloneWithPrefix(self, prefix : str) -> FA:
        new_fa = self.__class__(self.alphabet.copy())

        state_map : Dict[str, State] = {}
        for state in self.states:
            new_state : State = State(
                name=f"{prefix}{state.name}",
                is_initial=state.is_initial,
                is_final=state.is_final
            )
            state_map[state.name] = new_state
            new_fa.addState(new_state)
            
            
        for transition in self.transitions:
            new_transition : Transition = Transition(
                source_state=state_map[transition.source_state.name],
                input_symbol=transition.input_symbol,
                target_state=state_map[transition.target_state.name]
            )
            new_fa.addTransition(new_transition)
            
        return new_fa
    
    def _disableInitialState(self) -> None:
        """Desabilita o estado inicial do autômato."""
        if self.initial_state is not None:
            self.initial_state.is_initial = False
    
    # Escontra estados do autômato pelo nome
    def _find_state_by_name(self, name: str) -> State:
        for state in self.states:
            if state.name == name:
                return state
        raise ValueError(f"Estado '{name}' não encontrado.")