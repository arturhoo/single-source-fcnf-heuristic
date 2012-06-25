# -*- coding: utf-8 -*-
import networkx as nx
import argparse as ap
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
    no_de_oferta = None
    lista_nos_de_demanda = []
    no_de_oferta = carregue_no_de_oferta(DG)
    lista_nos_de_demanda = carregue_nos_de_demanda(DG)
    while len(lista_nos_de_demanda) > 0:
        no_de_demanda = lista_nos_de_demanda[0]
        dijkstra_path = nx.dijkstra_path(DG,
                                         source=no_de_oferta,
                                         target=no_de_demanda)
        limite_superior = limite_superior_caminho(DG, dijkstra_path)
        valor_fluxo = min(limite_superior, DG.node[no_de_demanda]['demand'])
        atualize1(DG, valor_fluxo, dijkstra_path)

        atualize2(DG, dijkstra_path)

        atualize3(DG, valor_fluxo,
                  dijkstra_path, no_de_oferta,
                  lista_nos_de_demanda)

        atualize4(DG, valor_fluxo, dijkstra_path)


if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Single Source FCNF Heuristic')
    parser.add_argument('-f', '--file', help='arquivo de entrada', required=True)
    args = vars(parser.parse_args())

    DG = nx.DiGraph()
    try:
        DG = load(open(args['file'], 'r'))
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        sys.exit()

    DG_copy = nx.DiGraph(DG)
    start = time()
    solve(DG)
    elapsed = (time() - start)
    print 'Tempo execução: %f' % (elapsed)
    # Imprima a solução
    edges = DG.edges(data=True)
    objective = 0
    for edge in edges:
        if edge[2]['fluxo'] > 0:
            objective += DG_copy[edge[0]][edge[1]]['weight']
        # print '(%d, %d) -> Fluxo: %f' % (edge[0], edge[1], edge[2]['weight'])
    print 'Objective: %d' % (objective)
