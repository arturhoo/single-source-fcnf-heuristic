## Heurística para o problema Single Source Fixed Charge Network Flow

### Heurística

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

### Implementação

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

