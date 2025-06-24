

class Action:
    REDUCE = "reduce"
    SHIFT = "shift"
    ACCEPT = "accept"
    GOTO = "goto"
    
    def __init__(self, action_type, transicao : int = None):
        self.action_type = action_type
        self.transicao = transicao
        
    def __repr__(self):
        return f"<Action(type={self.action_type}, transicao={self.transicao})>"
    
class SLRTable:
    def __init__(self):
        self.table = {}  # Dicionário para armazenar a tabela SLR
        self.start_state = None  # Estado inicial da tabela SLR
    
    def add_action(self, state: int, symbol: str, action: Action):
        """Adiciona uma ação à tabela SLR."""
        if state not in self.table:
            self.table[state] = {}
        self.table[state][symbol] = action
        
    def get_action(self, state: int, symbol: str) -> Action:
        """Obtém a ação para um estado e símbolo específicos."""
        return self.table.get(state, {}).get(symbol, None)
    
    def set_start_state(self, state: int):
        """Define o estado inicial da tabela SLR."""
        self.start_state = state