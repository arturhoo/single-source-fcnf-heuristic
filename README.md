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

O gerador constroi grafos aleatórios com base nos seguintes parâmetros:

* Número de nós de demanda
* Número de nós de transbordo
* Densidade
* Valor máximo para as demandas
* Valor máximo para as capacidades dos arcos
* Valor máximo para os custos dos arcos

E deve ser executado da seguinte forma:

    $ python gerador.py [-h] n_dem n_tr dens u_dem u_cap u_cost

onde:

    positional arguments:
      n_dem       Número de nós de demanda
      n_tr        Número de nós de transbordo
      dens        Densidade do grafo
      u_dem       Valor máximo para demandas
      u_cap       Valor máximo para capacidade nos arcos
      u_cost      Valor máximo para custo nos arcos

    optional arguments:
      -h, --help  show this help message and exit

Para cada instância são gerados dois arquivos, com o mesmo nome mas presentes em diferentes pastas. O formato do nome, `sXXdXXuXX`, representa as propriedades do grafo gerado, onde `sXX` representa o tamanho do grafo, `dXX` a densidade e `uXX` o valor máximo para as demandas. O primeiro arquivo serve de entrada para o `glpk` e está presente na pasta `instancias/glpk/`; o segundo está presente na pasta `instancias/py/` e é a representação serializada do grafo do tipo `networkx.Digraph` que pode ser utilizada no `solver.py` como demonstrado abaixo:

```python
from cPickle import load
from solver import solve
DG = load(open('instancias/py/s10d50u10', 'r'))
solve(DG)
```


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

Caso deseje rodar com uma instância já existente, que deve ser  uma
serialização de um grafo  direcionado do pacote `networkx`, basta especificar o
caminho como no comando abaixo:

    $ python solver.py -f instancia

