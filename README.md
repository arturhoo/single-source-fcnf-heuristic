# Heurística para o problema Single Source Fixed Charge Network Flow

## Heurística

Enquanto existir nó de demanda não satisfeito:

1. Menor caminho Dijkstra entre o nó de oferta e esse nó de demanda;
2. Calcular fluxo com valor mínimo(demanda do nó, menor limite superior do
caminho);
3. Atualize:
    1. Os limites superiores das arestas do caminho, subtraindo o fluxo que já
    passa por essas. Caso se torne nulo, defina custo infinito;
    2. Os custos não infinitos das arestar do caminho, tornando-os nulo, pois já
     foram pagos pela passagem do fluxo estabelecido;
    3. As demandas do nó de oferta e demanda. Caso a demanda do nó de demanda se
     torne nula, essa demanda está satisfeita;
    4. Os fluxos das arestas do caminho, incrementando-os com o valor do fluxo
    calculado em `2`;


## Gerador

O descritor lê o arquivo `input` na pasta corrente. Este arquivo deve possuir
uma sequência de descritores de instâncias, conforme a seguir:

* A primeira linha contém o número de descritores `N`
* Os descritores são apresentados em sequência com as seguintes linhas:
    1. Número de instâncias para esse descritor `I[i], i = 0...N-1`
    2. Número de nós de demanda
    3. Número de nós de transbordo
    4. Número de arestas
    5. Valor máximo para as demandas
    6. Valor máximo para as capacidades dos arcos
    7. Valor máximo para os custos dos arcos

Para cada instância é gerado um arquivo `instanciaXY`, em que `X` é o valor do
descritor de `0` a `N-1` e `Y`   é a ordem da instância do descrito de `0` a `I[X]-1`.

### Instâncias geradas

Foram geradas 18 instâncias:

* pequenas: 5 nós
    * 3 não densas: 8 arestas
    * 3 densas: 13 arestas
* médias: 10 nós
    * 3 não densas: 40 arestas
    * 3 densas: 60 arestas
* grandes: 15 nós
    * 3 não densas: 70 arestas
    * 3 densas: 150 arestas


## Implementação

A implementação foi feita em Python e pode ser encontrada no arquivo
`solver.py`. A implementação depende do pacote
[networkx](http://networkx.lanl.gov/index.html).

Notar que nela está presente
uma instância de exemplo que pode ser executada pelo comando:

    $ python solver.py

Gerando resultado:

    (1, 2) -> Fluxo: 10
    (1, 4) -> Fluxo: 3
    (1, 5) -> Fluxo: 7
    (2, 3) -> Fluxo: 5
    (4, 2) -> Fluxo: 0
    (4, 3) -> Fluxo: 2
    (5, 4) -> Fluxo: 7

Que para esse caso, corresponde a solução ótima.

