from __future__ import annotations
from . import utils
from model.symbol_table import TokenType, RegexToken

SEPARATOR = ':=='

# Expandir uma representação condensada de caracteres
def expand_char_class(char_class: str) -> list:
    # Exemplo: [a-zA-Z0-9] → ['a', ..., 'z', 'A', ..., 'Z', '0', ..., '9']
    chars = []
    i = 0
    while i < len(char_class):
        if i + 2 < len(char_class) and char_class[i+1] == '-':
            start = char_class[i]
            end = char_class[i+2]
            chars.extend(chr(c) for c in range(ord(start), ord(end)+1))
            i += 3
        else:
            chars.append(char_class[i])
            i += 1
    return chars

def tokenize_regex(regex: str) -> list[RegexToken]:
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]

        if c in {'*', '+', '?', '|', '(', ')'}:
            tokens.append(RegexToken(c))
            i += 1

        elif c == '<':
            j = i + 1
            while j < len(regex) and regex[j] != '>':
                j += 1
            if j == len(regex):
                raise ValueError("Referência de token não fechada com '>'.")
            ref_name = regex[i+1:j]
            tokens.append(RegexToken(RegexToken.REF, ref_name))
            i = j + 1

        elif c == "'":
            # Tratar aspas simples como delimitador de string
            j = i + 1
            while j < len(regex) and regex[j] != "'":
                j += 1
            if j == len(regex):
                raise ValueError("Aspas simples não fechadas.")
            string_value = regex[i+1:j]
            tokens.append(RegexToken(RegexToken.CHAR, string_value))
            i = j + 1

        elif c == '[':
            j = i + 1
            while j < len(regex) and regex[j] != ']':
                j += 1
            if j == len(regex):
                raise ValueError("Classe de caracteres não foi fechada.")
            char_class = regex[i+1:j]
            expanded = expand_char_class(char_class)
            # Representar como um agrupamento de OR: [a-zA-Z] → (a|b|...|Z)
            if len(expanded) == 1:
                tokens.append(RegexToken(RegexToken.CHAR, expanded[0]))
            else:
                tokens.append(RegexToken(RegexToken.LPAREN))
                for idx, ch in enumerate(expanded):
                    tokens.append(RegexToken(RegexToken.CHAR, ch))
                    if idx < len(expanded) - 1:
                        tokens.append(RegexToken(RegexToken.OR))
                tokens.append(RegexToken(RegexToken.RPAREN))
            i = j + 1

        elif c == '\\':
            # Tratar caractere de escape: \* ou \( etc
            if i + 1 < len(regex):
                tokens.append(RegexToken(RegexToken.CHAR, regex[i+1]))
                i += 2
            else:
                raise ValueError("Caractere de escape ao final de um padrão.")

        else:
            building_char = c
            i += 1
            while i < len(regex) and regex[i] not in {'*', '+', '?', '|', '(', ')', '<', '>', '[', "'"}:
                c = regex[i]
                if c == ' ' or c == '\n':
                    break
                building_char += c
                i += 1
                
            # Adiciona o caractere ou sequência de caracteres como um token CHAR
            if building_char:
                tokens.append(RegexToken(RegexToken.CHAR, building_char.strip()))
            i+= 1  # Avança para o próximo caractere
            
    return tokens

# Operador de concatenação definido explicitamente a partir da regex, quando há um caractere ou ')' à esquerda, e um caractere ou '(' à direita
def insert_concatenation(tokens: list[RegexToken]) -> list[RegexToken]:
    result = []
    for i in range(len(tokens)):
        result.append(tokens[i])
        if i + 1 < len(tokens):
            curr_type = tokens[i].type
            next_type = tokens[i + 1].type

            # Insere CONCAT se
            # o token atual é CHAR, ), *, + ou ?
            # o próximo token é CHAR ou (
            if (curr_type in {RegexToken.CHAR, RegexToken.RPAREN, RegexToken.STAR, RegexToken.PLUS, RegexToken.QUESTION} and
                next_type in {RegexToken.CHAR, RegexToken.LPAREN}):
                result.append(RegexToken(RegexToken.CONCAT))
    return result

def get_regex_from_lines(lines: list[str]) -> list[TokenType]:
    regex_list = []
    tokentype_list = []
    
    for line in lines:
        if SEPARATOR not in line:
            raise ValueError(f"Linha mal formatada: {line}")
        categoria, regex = map(str.strip, line.split(SEPARATOR, 1))
        regex_list.append((categoria, regex))
        
    for i, (categoria, regex) in enumerate(regex_list):
        tokens_without_concat = tokenize_regex(regex)
        tokentype = TokenType(name=categoria, regex=tokens_without_concat, dfa=None)  # DFA será construído posteriormente
        tokentype_list.append(tokentype)
        
    return tokentype_list

def get_regex_from_file(file_path: str) -> list[TokenType]:
    """
    Lê expressões regulares de um arquivo no formato:
    TOKEN:== REGEX
    e retorna uma lista de tuplas: TOKEN, list[RegexToken]
    """
    lines = utils.get_file_lines(file_path)
    if not lines:
        raise ValueError(f"O arquivo {file_path} está vazio ou não contém uma regex válida.")
    return get_regex_from_lines(lines)

def resolve_references_add_concats(tokentypes_without_concat: list[TokenType]) -> list[TokenType]:
    token_map = {t.name: t for t in tokentypes_without_concat}

    def expand_token_list(tokens: list[RegexToken], visited: set[str]) -> list[RegexToken]:
        resolved = []
        for token in tokens:
            if token.type == RegexToken.REF:
                ref_name = token.value
                if ref_name not in token_map:
                    raise ValueError(f"Referência <{ref_name}> não encontrada.")
                if ref_name in visited:
                    raise ValueError(f"Referência cíclica detectada: {' → '.join(visited)} → {ref_name}")
                
                # Expande recursivamente a referência
                sub_tokens = expand_token_list(token_map[ref_name].regex, visited | {ref_name})
                resolved.append(RegexToken(RegexToken.LPAREN))
                resolved.extend(sub_tokens)
                resolved.append(RegexToken(RegexToken.RPAREN))
            else:
                resolved.append(token)
        return resolved

    resolved_tokentypes = []
    for tokentype in tokentypes_without_concat:
        expanded_tokens = expand_token_list(tokentype.regex, {tokentype.name})
        with_concats = insert_concatenation(expanded_tokens)
        resolved_token = tokentype.copy()
        resolved_token.regex = with_concats
        resolved_tokentypes.append(resolved_token)

    return resolved_tokentypes
