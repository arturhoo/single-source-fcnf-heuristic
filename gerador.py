# -*- coding: utf-8 -*-
from solver import solve
from cPickle import dump
from os import path, makedirs
import argparse as ap
import random as rand
import networkx as nx


def gera_demandas(graph, n, u):
    base = graph.number_of_nodes() + 1
    for i in range(base, base + n):
        graph.add_node(i, {'demand': rand.randrange(1, u + 1)})


def gera_transbordos(graph, n):
    base = graph.number_of_nodes() + 1
    for i in range(base, base + n):
        graph.add_node(i, {'demand': 0})


def gera_oferta(graph):
    base = graph.number_of_nodes() + 1
    demanda_total = 0
    for i_node in graph.nodes():
        demanda_total += graph.node[i_node]['demand']
    graph.add_node(base, {'demand': - demanda_total})


def gera_arcos(graph, n, u, c):
    n_vertices = graph.number_of_nodes()
    n_arestas_adicionadas = 0
    while n_arestas_adicionadas < n:
        origem = rand.randrange(1, n_vertices + 1)
        destino = rand.randrange(1, n_vertices + 1)
        while (destino == origem):
            destino = rand.randrange(1, n_vertices + 1)
        if not graph.has_edge(origem, destino):
            n_arestas_adicionadas += 1
            cap = rand.randrange(u / 2 + 1, u + 1)  # evita grande dispersão
                                                    # de valores através do
                                                    # lowerbound u / 2 + 1
            custo = rand.randrange(0, c + 1)
            graph.add_edge(origem, destino, \
                          {'capacity': cap, 'weight': custo, 'fluxo': 0})


def confere_integralidade_parametros(n_dem, n_tr, n_edge,
                                     u_dem, u_cap, u_cost):
    min_dem = 1
    if (n_dem < min_dem):
        raise Exception('O número de nós de demanda é menor do que o mínimo')

    max_edge = (n_dem + n_tr + 1) * (n_dem + n_tr)  # arranjo dos nós em pares
    if (n_edge > max_edge):
        raise Exception('O número de arestas é maior do que o máximo')

    min_u = 1
    if (u_dem < min_u):
        raise Exception('''O limite superior para a demanda é
                        menor do que o mínimo ''')

    min_cap = 1
    while (u_cap < min_cap):
        raise Exception('Valor máximo de capacidade menor que o mínimo')

    min_cost = 0
    while (u_cost < min_cost):
        raise Exception('Valor máximo de custos menor que o mínimo')


def formata_saida_glpk(graph):
    saida = 'set Nodes := '
    for node in graph.nodes():
        saida += str(node) + ' '
    saida += ';\n'

    saida += 'set Arcs := '
    for edge in graph.edges():
        saida += str(edge) + ' '
    saida += ';\n'

    saida += '\n\n'

    saida += 'param b :=\n'
    for node in graph.nodes():
        saida += str(node) + '\t\t' + str(graph.node[node]['demand']) + '\n'

    saida += ';\n\n'

    saida += 'param:\t\tu\t\tc :=\n'
    for edge in graph.edges():
        saida += str(edge[0]) + ',' + str(edge[1]) + '\t\t' + \
                  str(graph.edge[edge[0]][edge[1]]['capacity']) + '\t\t' + \
                  str(graph.edge[edge[0]][edge[1]]['weight']) + '\n'

    saida += ';\n\nend;\n'

    return saida


def gera_grafo_viavel(n_dem, n_tr, n_edge, u_dem, u_cap, u_cost):
    graph = nx.DiGraph()

    while(True):
        try:
            gera_demandas(graph, n_dem, u_dem)
            gera_transbordos(graph, n_tr)
            gera_oferta(graph)
            gera_arcos(graph, n_edge, u_cap, u_cost)
            solve(nx.DiGraph(graph))
        except Exception:
            graph = nx.DiGraph()
            continue
        break

    return graph

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Gerador Single Source FCNF')
    parser.add_argument('n_dem', help='Número de nós de demanda')
    parser.add_argument('n_tr', help='Número de nós de transbordo')
    parser.add_argument('dens', help='Densidade do grafo')
    parser.add_argument('u_dem', help='Valor máximo para demandas')
    parser.add_argument('u_cap', help='Valor máximo para capacidade nos arcos')
    parser.add_argument('u_cost', help='Valor máximo para custo nos arcos')
    args = vars(parser.parse_args())

    n_dem = int(args['n_dem'])
    n_tr = int(args['n_tr'])
    n_edge = int(float(args['dens']) * (n_dem + n_tr + 1) * (n_dem + n_tr))
    u_dem = int(args['u_dem'])
    u_cap = int(args['u_cap'])
    u_cost = int(args['u_cost'])
    graph = gera_grafo_viavel(n_dem, n_tr, n_edge,
                              u_dem, u_cap, u_cost)

    output = formata_saida_glpk(graph)
    density = nx.density(graph)
    size = n_dem + n_tr + 1
    file_name = 's' + str(size) + \
                'd' + str(int(round(density, 3) * 100)) + \
                'u' + str(u_dem)

    glpk_dir = 'instancias/glpk/'
    if not path.exists(glpk_dir):
        makedirs(glpk_dir)
    glpk_out = open(glpk_dir + file_name, 'w')
    glpk_out.write(output)
    glpk_out.close()

    py_dir = 'instancias/py/'
    if not path.exists(py_dir):
        makedirs(py_dir)
    py_out = open('instancias/py/py' + file_name, 'w')
    dump(graph, py_out)
    py_out.close()
