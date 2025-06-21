# Closure - forma os estados.
# A entrada é a gramatica. Na primeira iteração, deve colocar os '.' na gramatica
# Depois disso, avaliar se o '.' esta antes de um tokentype - Se estiver char + ref, entao true
# Expandir sempre do regex original colocando pontinho

from model.symbol_table import TokenType, RegexToken
import core.regex_parser as regex_parser
from typing import List, Dict, Set
    
# Sempre vamos obter o closure de 1 linha apenas
def define_closure(input_state: TokenType, tokenTypes: list[TokenType]):
    # ex: primeira entrada: input_state: [<TokenType(name='E', regex='REF(T)REF(E')')
    # Conjunto obtido
    closureSet = []

    # Se o elemento de entrada input_state for o primeiro da gramática, é um caso especial
    if input_state == tokenTypes[0]:
        print("debug : é o primeiro")

        symbol_list = list()
        # Selecionar o primeiro simbolo da produção que não seja SLR_DOT
        symbol_list.append(input_state.regex[1].value)  #ex: T

        #input_state.regex.insert(0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, "."))
        closureSet.append(input_state)

        for rule in tokenTypes:
            if rule.name in symbol_list:
                rule.regex.insert(0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, "."))
                closureSet.append(rule)
                # Adicona os simbolos não terminais que serão buscados  
                if rule.regex[0].type == "REF":
                    symbol_list.append(rule.regex[0].value)
           
    # Caso contrário, o conjunto closure começa com o proprio elemento
    # A regra já vem com um ponto SLR_DOT(.)
    else:

        closureSet.append(input_state)
        # Verificar a posição do SLR_DOT(.)
        regex_list = input_state.regex
    
        
        for i in range(len(regex_list)):
            if regex_list[i].type == "SLR_DOT":
                # Se o SLR_DOT está no final, sai do loop
                if i == (len(regex_list) - 1):
                    break
                if regex_list[i+1].type == "REF":
                    symbol_list = list()
                    # O simbolo em análise deve ser aquele que tinha o ponto
                    symbol_list.append(regex_list[i+1].value)
                    for rule in tokenTypes:
                        if rule.name in symbol_list:
                            #rule.regex.insert(0, regex_parser.RegexToken(regex_parser.RegexToken.SLR_DOT, "."))
                            closureSet.append(rule)
                            # Adicona os simbolos não terminais que serão buscados    
                        if rule.regex[0].type == "REF":
                            symbol_list.append(rule.regex[0].value)

                else:
                    return closureSet

    # Retorna o estado final
    return closureSet