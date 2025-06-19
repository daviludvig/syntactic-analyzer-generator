from __future__ import annotations
from .dfa import DFA
from typing import List, Dict, Union


class Token:
    def __init__(self, lexeme: Lexeme = None, tokentype: Union[TokenType,str] = None):
        self.lexeme = lexeme
        self.tokentype = tokentype
        
    def __repr__(self):
        return f"<Token(lexeme={self.lexeme}, tokentype={self.tokentype})>"
    
    def __str__(self):
        return (f"<{self.lexeme}, {self.tokentype.name if isinstance(self.tokentype, TokenType) else self.tokentype}>")

class TokenType:
    def __init__(self, name: str, regex: List[RegexToken], dfa: DFA = None):
        self.name = name
        self.regex = regex
        self.dfa = dfa
        
    def __repr__(self):
        regex_str = "".join(str(tok) for tok in self.regex)
        return f"<TokenType(name='{self.name}', regex='{regex_str}')>"
    
    def __str__(self):
        regex_str = "".join(str(tok) for tok in self.regex)
        dfa_str = f"DFA states: {len(self.dfa.states)}" if self.dfa else "No DFA"
        return (
            f"TokenType:\n"
            f"  Name  : {self.name}\n"
            f"  Regex : {regex_str}\n"
            f"  {dfa_str}"
        )

class RegexToken:
    CHAR = 'CHAR'
    STAR = '*'
    PLUS = '+'
    QUESTION = '?'
    OR = '|'
    LPAREN = '('
    RPAREN = ')'
    CONCAT = '.'  # Caso especial: inseriremos este operador mesmo que não apareça explicitamente na regex
    CHAR_CLASS = 'CLASS'

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})" if self.value else self.type

class Lexeme:
    def __init__(self):
        self.lexeme : str = ""
        
    def __repr__(self):
        return f"<Lexeme('{self.lexeme}')>"
    
    def __str__(self):
        return self.lexeme
    
    def __eq__(self, other):
        if isinstance(other, Lexeme):
            return self.lexeme == other.lexeme
        return False

    def __hash__(self):
        return hash(self.lexeme)
    
    def get(self) -> str:
        """Retorna o lexema atual"""
        return self.lexeme

    def increase(self, char: str) -> None:
        """Adiciona um caractere ao lexema"""
        self.lexeme += char   
    
    def decrease(self) -> None:
        """Remove o último caractere do lexema"""
        if self.lexeme:
            self.lexeme = self.lexeme[:-1] 


class SymbolTable:
    def __init__(self):
        # Inicializa com palavras reservadas
        self.table : Dict[Lexeme, TokenType] = {}

    def insert(self, lexeme: Lexeme, token_type: str):
        """Insere um novo símbolo se não existir"""
        if lexeme not in self.table:
            self.table[lexeme] = token_type

    def lookup(self, lexeme: Lexeme) -> str:
        """Retorna o tipo de token do lexema"""
        return self.table.get(lexeme, None)

    def contains(self, lexeme: Lexeme) -> bool:
        """Verifica se o lexema já está na tabela"""
        return lexeme in self.table

    def export(self, filename: str = "tabela_simbolos.csv"):
        """Exporta a tabela para CSV"""
        with open(filename, "w") as f:
            f.write("Lexema,Tipo\n")
            for lexeme, tipo in self.table.items():
                f.write(f"{lexeme},{tipo}\n")

    def __repr__(self):
        return f"<SymbolTable(size={len(self.table)})>"

    def __str__(self):
        output = ["Tabela de Símbolos:"]
        if not self.table:
            return "\n".join(output)
        
        max_len = max(len(lexeme.get()) for lexeme in self.table) + 1
    
        for lexeme, token_type in self.table.items():
            output.append(f"  {lexeme.get():<{max_len}} <=> {token_type}")
    
        return "\n".join(output)