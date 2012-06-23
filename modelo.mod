/* Conjuntos */
set Nodes;
set Arcs within {Nodes, Nodes};

/* Matrizes e vetores */
param b {Nodes}; /* vetor de demandas */
param c {Arcs}; /* matriz de custos fixos das arestas */
param u {Arcs}; /* matriz de limites superiores das arestas */ 

/* Variáveis de decisão */
var x {Arcs}, integer; /* fluxo em cada aresta */
var y {Arcs}, binary; /* variável para indicar se fluxo existe em uma aresta */

/* Função objetivo */
minimize objective: sum {(i,j) in Arcs} c[i,j] * y[i,j]; /* minimizar a soma de custos fixos */

/* Restrições */
s.t. flow_balance {i in Nodes}:
	sum {j in Nodes: (j,i) in Arcs} x[j,i] -
	sum {j in Nodes: (i,j) in Arcs} x[i,j] = b[i]; 
s.t. capacity {(i,j) in Arcs}:
	x[i,j] <= u[i,j] * y[i,j];
s.t. domain {(i, j) in Arcs}:
	x[i,j] >= 0;

solve; display x;

end;

# fonte: http://msor.victoria.ac.nz/twiki/pub/Courses/OPRE456_2012T1/Private/mincostnetworkflow.mod
