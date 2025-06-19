from .utils import get_file_lines
from typing import List, Tuple
from model.dfa import DFA
from model.symbol_table import Token, Lexeme, SymbolTable


def parse_source_code_from_file(file_path: str, dfas: List[DFA], symbol_table : SymbolTable) -> List[Token]:
    """
    Reads the content of a source code file and returns it as a string.

    Args:
        file_path (str): The path to the source code file.
        dfas (List[DFA]): A list of DFA objects to be used in parsing.

    Returns:
        List[Token]: A list of Token objects representing the parsed source code.
        
    """
    lines = get_file_lines(file_path)
    single_line = ""
    for line in lines:
        single_line += "\n" + line
    
    tokens = _get_tokens(single_line, dfas, symbol_table)
    return tokens

def _get_tokens(source_code : str, dfas : List[DFA], symbol_table : SymbolTable) -> List[Token]:
    """
    O automato principal da análise léxica é o dfas[0], que é o DFA que aceita a linguagem de todos os lexemas válidos.
    
    Recebe o código fonte como string e retorna uma lista de tokens.
    Cada token é um objeto Token que contém o lexema e o tipo do token.
    Se o lexema não for reconhecido, é adicionado um token de erro com o lexema e o tipo "ERRO".
    
    """
    
    tokens = []

    
    def _add_token(lexeme_obj: Lexeme, dfas: List[DFA], symbol_table: SymbolTable, tokens: List[Token], forced_type: str = None) -> None:
        """
        Define o tipo do token para o lexema atual, cria o token e o adiciona à lista de tokens.
        """
        token_type = forced_type if forced_type else _get_lexeme_type(lexeme_obj, dfas, symbol_table)
        token = Token()
        token.lexeme = lexeme_obj.get()
        token.tokentype = token_type
        tokens.append(token)
        
        symbol_table.insert(lexeme_obj, token_type)
    
    lexeme_obj = Lexeme()
    i = 0
    while i != len(source_code):
        
        # Enquanto o lexema for vazio, e houver espaço ou nova linha, continue até achar não ser espaço ou nova linha
        if ((lexeme_obj.get() == "") and (source_code[i] == " " or source_code[i] == "\n")):
            i += 1
            continue
        
        # Adiciona o caractere atual ao lexema
        lexeme_obj.increase(source_code[i])
        print(f"Lexema atual: {lexeme_obj.get()}")
        # Se o lexema não for mais válido no DFA principal, verifica se é um erro ou define sua categoria
        if not dfas[0].isValidInput(lexeme_obj.get()):
            
            # Se o lexema não é mais reconhecido no "big automato" e o char atual não for espaço, nova linha ou ponto e vírgula, é um erro
            if ((source_code[i] != " ") and (source_code[i] != "\n") and (source_code[i] != ";")):  # Ponto e vírgula só pode ser usado para final de sentença
                # Forma o lexema de erro
                while i + 1 < len(source_code) and source_code[i + 1] not in (" ", "\n"):
                    i += 1
                    lexeme_obj.increase(source_code[i])
                # Cria o token de erro
                _add_token(lexeme_obj, dfas, symbol_table, tokens, forced_type="ERRO")
                lexeme_obj = Lexeme()
                i += 1
                continue

            # Caso não erro
            # Retrocede o char que não é mais válido
            i -= 1
            lexeme_obj.decrease()
            
            # Checa na TS e nos DFAs para qual tipo de token o lexema pertence
            _add_token(lexeme_obj, dfas, symbol_table, tokens)
            
            lexeme_obj = Lexeme()

        print(f">> Big automato aceita o lexema: '{lexeme_obj.get()}' index {i}")

        i += 1
        
    # Se o lexema final não for vazio, adiciona o token correspondente
    if lexeme_obj.get() != "":
        _add_token(lexeme_obj, dfas, symbol_table, tokens)
        
    return tokens

def _get_lexeme_type(lexeme: Lexeme, dfas: List[DFA], symbol_table : SymbolTable) -> str:
    """
    Recebe um lexema e verifica se ele é válido em algum dos DFAs.
    Se for, retorna o nome do DFA correspondente.
    
    Checa na tabela de símbolos se o lexema já foi inserido.
    Se sim, retorna o nome do DFA correspondente.
    Se não, insere o lexema na tabela de símbolos e retorna o nome do DFA correspondente.
    """
    symbol_table_value = symbol_table.lookup(lexeme)
    if symbol_table_value:
        return symbol_table_value
    
    for i in range(1, len(dfas)):
        if dfas[i].isValidInput(lexeme.get()):
            return dfas[i].name