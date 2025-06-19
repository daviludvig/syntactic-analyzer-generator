from core.regex_parser import RegexToken
from typing import List, Tuple

'''
Este algoritmo recebe como input uma lista de caracteres e operadores como a retornada pelo regex parser,
e a retorna reescrita em notação polonesa invertida usando o algoritmo de Shunting-Yard.
'''

# Define precedência dos operadores
precedence = {
    RegexToken.STAR: 3,
    RegexToken.PLUS: 3,
    RegexToken.QUESTION: 3,
    RegexToken.CONCAT: 2,
    RegexToken.OR: 1,
}

# Define associatividade à direita dos operadores
right_associative = {
    RegexToken.STAR,
    RegexToken.PLUS,
    RegexToken.QUESTION,
}

def shunting_yard(tokens: List[RegexToken]) -> List[RegexToken]:
    output = []
    stack = []  # Pilha para guardar operadores e parênteses temporariamente

    # Para cada token do regex
    for token in tokens:
        tok_type = token.type

        # Se o tipo for CHAR, vai diretamente para o output
        if tok_type == RegexToken.CHAR:
            output.append(token)

        # Se o tipo for *, +, ?, . ou |, vamos fazer checagens 
        elif tok_type in {RegexToken.STAR, RegexToken.PLUS, RegexToken.QUESTION,
                          RegexToken.CONCAT, RegexToken.OR}:
            
            # Enquanto há algo na pilha e o seu topo não é '('
            while stack:
                top_type = stack[-1].type
                if top_type == RegexToken.LPAREN:
                    break
                
                # Se o topo da pilha tiver precedência sobre o token atual,
                # ou a mesma precedência mas o token atual é associativo à esquerda,
                # o topo da pilha vai para o output
                if (precedence[top_type] > precedence[tok_type] or
                    (precedence[top_type] == precedence[tok_type] and
                     tok_type not in right_associative)):
                    output.append(stack.pop())
                else:
                    break
            
            # Finalmente adiciona o token atual ao output
            stack.append(token)

        # Se o tipo for '(' ele vai para a pilha
        elif tok_type == RegexToken.LPAREN:
            stack.append(token)

        # Se o tipo for ')' vamos tirar da pilha e colocar no output até encontrar o '(' correspondente
        elif tok_type == RegexToken.RPAREN:
            while stack and stack[-1].type != RegexToken.LPAREN:
                output.append(stack.pop())
            if not stack:
                raise ValueError("Parênteses não correspondem.")
            stack.pop()  # Remove o '('

    # Após processar tudo, tiramos da pilha e adicionamos ao output todos os tokens remanescentes
    while stack:
        if stack[-1].type in {RegexToken.LPAREN, RegexToken.RPAREN}:
            raise ValueError("Parênteses não correspondem.")  # Se sobrarem parênteses, isto é um erro.
        output.append(stack.pop())

    return output