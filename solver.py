# -*- coding: utf-8 -*-

import networkx as nx
import argparse as ap
import random as rand
import sys
from time import time
from cPickle import load


def carregue_nos_de_demanda(DG):
    l = []
    for no in DG.nodes():
        if DG.node[no]['demand'] > 0:
            l.append(no)
    return l


def carregue_no_de_oferta(DG):
    for no in DG.nodes():
        if DG.node[no]['demand'] < 0:
            return no


def limite_superior_caminho(DG, lista):
    menor_capacidade = DG[lista[0]][lista[1]]['capacity']
    for (idx, item) in enumerate(lista):
        capacidade_atual = DG[lista[idx]][lista[idx + 1]]['capacity']
        menor_capacidade = min(capacidade_atual, menor_capacidade)
        if idx == len(lista) - 2:
            break
    return menor_capacidade


# Atualiza as capacidades de acordo com o valor do novo fluxo
def atualize1(DG, valor_fluxo, lista):
    for (idx, item) in enumerate(lista):
        DG[lista[idx]][lista[idx + 1]]['capacity'] -= valor_fluxo
        # Coloca custo infinito no arco ao inves de eliminá-lo
        if DG[lista[idx]][lista[idx + 1]]['capacity'] == 0:
            DG[lista[idx]][lista[idx + 1]]['weight'] = float('inf')
        if idx == len(lista) - 2:
            break


# Já que passa fluxo, torne nulo o custo do arco
def atualize2(DG, lista):
    for (idx, item) in enumerate(lista):
        try:
            # Se esse arco não foi completamente utilizado
            # torne nulo seu custo
            if DG[lista[idx]][lista[idx + 1]]['weight'] != float('inf'):
                DG[lista[idx]][lista[idx + 1]]['weight'] = 0
        except KeyError:
            pass
        if idx == len(lista) - 2:
            break


# Atualize as demandas
def atualize3(DG, valor_fluxo, lista, no_de_oferta, lista_nos_de_demanda):
    DG.node[no_de_oferta]['demand'] += valor_fluxo
    DG.node[lista[len(lista) - 1]]['demand'] -= valor_fluxo
    # Se a demanda no no foi satisfeita elimine esse no da lista de demandas
    if DG.node[lista[len(lista) - 1]]['demand'] == 0:
        lista_nos_de_demanda.remove(lista[len(lista) - 1])


# Insira a variável fluxo nos arcos em questão
def atualize4(DG, valor_fluxo, lista):
    for (idx, item) in enumerate(lista):
        DG[lista[idx]][lista[idx + 1]]['fluxo'] += valor_fluxo
        if idx == len(lista) - 2:
            break


def solve(DG):
    attempts = 0
    max_iter = 100
    achou_solucao = False

    while attempts < max_iter and not achou_solucao:
        # print attempts
        grafo = nx.DiGraph(DG)
        no_de_oferta = None
        lista_nos_de_demanda = []
        no_de_oferta = carregue_no_de_oferta(grafo)
        lista_nos_de_demanda = carregue_nos_de_demanda(grafo)
        invalid = False
        while len(lista_nos_de_demanda) > 0 and (not invalid):
            curr_demand = rand.randrange(0, len(lista_nos_de_demanda))
            # print "demand = " + str(lista_nos_de_demanda[curr_demand])
            no_de_demanda = lista_nos_de_demanda[curr_demand]
            dijkstra_path = nx.dijkstra_path(grafo,
                                             source=no_de_oferta,
                                             target=no_de_demanda)
            limite_superior = limite_superior_caminho(grafo, dijkstra_path)
            valor_fluxo = min(limite_superior, \
                              grafo.node[no_de_demanda]['demand'])
            if valor_fluxo == 0:
                invalid = True
            else:
                atualize1(grafo, valor_fluxo, dijkstra_path)

                atualize2(grafo, dijkstra_path)

                atualize3(grafo, valor_fluxo,
                          dijkstra_path, no_de_oferta,
                          lista_nos_de_demanda)

                atualize4(grafo, valor_fluxo, dijkstra_path)
        if not invalid:
            # print 'found solution'
            achou_solucao = True
            return grafo
        else:
            attempts += 1

    if not achou_solucao:
        raise Exception('Instância inviável')


if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Single Source FCNF Heuristic')
    parser.add_argument('-f', '--file', help='arquivo de entrada')
    args = vars(parser.parse_args())

    DG = nx.DiGraph()
    if args['file']:
        try:
            DG = load(open(args['file'], 'r'))
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            sys.exit()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            sys.exit()
    else:
        DG.add_nodes_from([(1, {'demand': -20}),
                           (2, {'demand': 5}),
                           (3, {'demand': 7}),
                           (4, {'demand': 8}),
                           (5, {'demand': 0})])
        DG.add_edges_from([(1, 2, {'capacity': 10, 'weight': 8, 'fluxo': 0}),
                           (1, 4, {'capacity': 3,  'weight': 2, 'fluxo': 0}),
                           (1, 5, {'capacity': 10, 'weight': 7, 'fluxo': 0}),
                           (2, 3, {'capacity': 5,  'weight': 3, 'fluxo': 0}),
                           (4, 2, {'capacity': 8,  'weight': 6, 'fluxo': 0}),
                           (4, 3, {'capacity': 9,  'weight': 4, 'fluxo': 0}),
                           (5, 4, {'capacity': 7,  'weight': 5, 'fluxo': 0})])

    DG_copy = nx.DiGraph(DG)
    start = time()
    DG = solve(DG)
    elapsed = (time() - start)
    # Imprima a solução
    edges = DG.edges(data=True)
    objective = 0
    for edge in edges:
        if edge[2]['fluxo'] > 0:
            objective += DG_copy[edge[0]][edge[1]]['weight']
        print '(%d, %d) -> Fluxo: %d' % (edge[0],
                                         edge[1],
                                         int(edge[2]['fluxo']))
    print 'Tempo execução: %f' % (elapsed)
    print 'Objective: %d' % (objective)
