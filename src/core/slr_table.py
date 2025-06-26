import model.symbol_table as symbol_table

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

    def populate(self, estados, transicoes, follows, non_terminals) -> None:
        # Adiciona SHIFT, ACCEPT e GOTO na tabela SLR
        for (origem, simbolo), destino in transicoes.items():
            if (destino == Action.ACCEPT ) and (simbolo == "$"):
                # Caso simbolo seja final de sentença
                action = Action(Action.ACCEPT, "acc")
                self.table[(origem, simbolo)] = action
            elif simbolo not in non_terminals:
                # Caso simbolo seja um terminal
                action = Action(Action.SHIFT, destino)
                self.table[(origem, simbolo)] = action
            elif simbolo in non_terminals:
                # Caso simbolo seja um não terminal
                action = Action(Action.GOTO, destino)
                self.table[(origem, simbolo)] = action



        # Adiciona o REDUCE na tabela SLR
        for i, estado in enumerate(estados):
            for prod in estado:
                if prod.regex[-1].type == symbol_table.RegexToken.SLR_DOT:
                    #print(prod.regex)
                    cabeca_follow = follows[prod.name]  # O resultado disso é um set de terminais (follows da cabeca)


                    for simbolo in cabeca_follow:
                        action = Action(Action.REDUCE, [prod.name, len(prod.regex[:-1])])
                        self.table[((i, simbolo))] = action
                        #print(i, simbolo, action)