# syntactic-analyzer-generator
A Python-based framework for generating SLR(1) parsers from context-free grammars. Built as part of a university project for the Formal Languages and Compilers course at UFSC, this tool includes implementations of FIRST and FOLLOW sets, canonical collection construction, and SLR parsing table generation.


## Levantamento prévio 17/06
- Input deve aceitar formatos
  - id :== [a-zA-Z]([a-zA-Z]|[0-9])*
  - num :== [0-9]+
  - nome :== <id> | <id> <num>
- [Implementação SLR(1) geeks for geeks](https://www.geeksforgeeks.org/compiler-design-slr1-parser-using-python/)
- **Não precisa ser fatorada nem não recursiva**


### Alterações no T1
- Tabela de símbolos. 
    - Se o lexema já está na TS, retorna <lexema, categoria>
        - Ex. <for, PR>
    - Caso contrário, adiciona o lexema na TS e retorna no tipo <categoria, linha da tabela>
        - Ex. <id, 10>
- Adicionar suporte a encadeamento de categorias na entrada.
    - Exemplo: nome :== <id> | <id> <num>
    - Não parece ser dificil desde que tenha ordem na entrada do documento.
    - Perde mais dois elementos de gramática `<` e `>`.


### Algoritmos

[Retirados daqui](https://presencial.moodle.ufsc.br/pluginfile.php/1130230/mod_resource/content/6/Aho%20-%20Compilers%20-%20Principles%2C%20Techniques%2C%20and%20Tools%202e.pdf)

#### First e Follow seção 4.4.2
##### First

Pág 244

Computar o First(X)

1. Se X é terminal, então First(X) = {X}.
2. Se X é não-terminal e X -> Y1Y2...Yn é uma produção, Então 
   - Se Y1 é terminal, então First(X) = {Y1}.
   - Se Y1 é não-terminal, então First(X) = First(Y1) - {&}.
   - Se Y1 pode derivar &, então adiciona First(Y2) - {&} a First(X), e assim por diante até encontrar um Yk que não deriva & ou até n.
   - Se Y1, Y2, ..., Yn-1 podem derivar & e se Yn pode derivar em & então adiciona & a First(X).
3. Se X -> & é uma produção, então adiciona & a First(X).

##### Follow

Pag 244

Computar o Follow(X)

1. Se X é o símbolo inicial, então adiciona $ a Follow(X).
2. Se A -> αXβ é uma produção, então adiciona First(β) (menos &).
3. Se A -> αXβ e β pode derivar em &, então adiciona Follow(A) a Follow(X), faça o mesmo se A -> αX.
    - **Considerar ordem para evitar recursividade ciclica infinita**


#### Closure fig 4.32

Pág 268

```
SetOfItems closure(I) {
    J = I;
    repeat
        for (each item A -> α . B β in J)
            for (each production B -> γ of G)
                if (B -> . γ is not in J)
                    add B -> . γ to J;
    until no more items can be added to J on one round;
    return J;
}
```

Uma forma conveniente de implementar a função closure (fecho) é utilizar um vetor booleano chamado added, indexado pelos não-terminais da gramática G.

Esse vetor serve para controlar quais não-terminais já foram processados durante a construção do fecho, evitando que o mesmo conjunto de itens seja adicionado repetidamente, o que pode causar loops infinitos ou desperdício de processamento.

Como funciona:

    Inicialmente, todos os valores de added são falsos.

    Quando encontramos um item da forma [A → α·Bβ], ou seja, com o ponto antes de um não-terminal B, precisamos incluir no fecho todos os itens da forma [B → ·γ], para cada produção B → γ da gramática.

    Mas antes de adicionar esses itens, verificamos se added[B] já está definido como true:

        Se não estiver (ou seja, added[B] == false), então adicionamos os itens [B → ·γ] ao conjunto e marcamos added[B] = true.

        Se já estiver true, significa que esse não-terminal já foi expandido, e não precisamos repetir o processo para ele.

#### Coleção canônica fig 4.33

Pag 269

```
void items (G') {
    C = closure({[S' -> . S]});
    repeat
        for (each set of items I in C)
            for (each grammar symbol X)
                if (goto(I, X) is not empty and not in C)
                    add goto(I, X) to C;
    until no new sets of items can be added to C on one round;
}
```

#### LR Parsing fig 4.36

Pág 274

```
let a be the first symbol of w$;
while(1) {
    let s be the state on top of the stack;
    if (action[s, a] = shift t) {
        push t onto the stack;
        let a be the next input symbol;
    } else if (action[s, a] = reduce A -> β) {
        pop |β| symbols from the stack;
        let state t now be on top of the stack;
        push goto(t, A) onto the stack;
        output the production A -> β;
    } else if (action[s, a] = accept) break;
    else call error-recovery routine;
}
```

Entrada: w$ (onde $ é o símbolo de fim de entrada)
Entrada: Tabela LR-parsing com funções action e goto para a gramática G.

Saída: Se w pertence a L(G), os passos de redução do parse bottom-up para w.

Método: Inicialmente o parser tem s0 na sua stack, sendo s0 o estado inicial e w$ na entrada

#### Construção da tabela do analisador SLR alg 4.38

#### Função goto
Pág 269

A segunda função útil na construção de um analisador LR(0) é a função GOTO(I, X), onde:

    I é um conjunto de itens (ou seja, um estado do autômato LR),

    X é um símbolo da gramática (pode ser terminal ou não terminal).

A função GOTO(I, X) é definida como o fecho (ou closure) do conjunto de todos os itens da forma:

    [A → αX·β]

tal que existe em I um item [A → α·Xβ].

Ou seja, partimos de todos os itens do conjunto I onde o ponto (·) está imediatamente antes do símbolo X, e "movemos o ponto" para depois de X. O conjunto resultante desses novos itens passa, então, pelo processo de closure, que expande o conjunto considerando as produções iniciadas a partir do símbolo que vem após o ponto, se for um não terminal.



Exemplo

Se I é o conjunto de itens: 
```
I = {
    [E' -> E.],
    [E -> E .+ T],
}
```

Então goto(I, +) seria calculado da seguinte forma:

```
E -> E + .T
T -> .T * F
T -> .F
F -> .(E)
F -> .id
```

Para computá-lo, avança o pontinho (·) para a direita dos símbolos.
No caso, a primeira sentença não tem nada depois. Na segunda, o ponto está antes do símbolo +, então avançamos o ponto para a direita do +, e adicionamos o item [E -> E + .T] ao conjunto.

Nesse caso, o ponto está à esquerda de um não-terminal T, então precisamos adicionar todos os itens que começam com T, ou seja, os itens [T -> .T * F], [T -> .F], [F -> .(E)], e [F -> .id].