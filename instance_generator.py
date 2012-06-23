# -*- coding: utf-8 -*-
import networkx as nx
import random as rand


def generate_demands(graph, n, u):
    base = graph.number_of_nodes() + 1
    for i in range(base, base + n):
        graph.add_node(i, {'demand': rand.randrange(1, u + 1)})


def generate_transships(graph, n):
    base = graph.number_of_nodes() + 1
    for i in range(base, base + n):
        graph.add_node(i, {'demand': 0})


def generate_source(graph):
    base = graph.number_of_nodes() + 1
    total_demand = 0
    for i_node in graph.nodes():
        total_demand += graph.node[i_node]['demand']
    graph.add_node(base, {'demand': - total_demand})


def generate_edges(graph, n, u, c):
    n_nodes = graph.number_of_nodes()
    e_added = 0
    while e_added < n:
        origin = rand.randrange(1, n_nodes + 1)
        destiny = rand.randrange(1, n_nodes + 1)
        while (destiny == origin):
            destiny = rand.randrange(1, n_nodes + 1)
        if not graph.has_edge(origin, destiny):
            e_added += 1
            cap = rand.randrange(u / 2 + 1, u + 1)  # evita grande dispersão de valores através do lowerbound u / 2 + 1
            cost = rand.randrange(0, c + 1)
            graph.add_edge(origin, destiny, {'capacity': cap, 'cost': cost})


def format_output(graph):
    output = 'set Nodes := '
    for node in graph.nodes():
        output += str(node) + ' '
    output += ';\n'

    output += 'set Arcs := '
    for edge in graph.edges():
        output += str(edge) + ' '
    output += ';\n'

    output += '\n\n'

    output += 'param b :=\n'
    for node in graph.nodes():
        output += str(node) + '\t\t' + str(graph.node[node]['demand']) + '\n'

    output += ';\n\n'

    output += 'param:\t\tu\t\tc :=\n'
    for edge in graph.edges():
        output += str(edge[0]) + ',' + str(edge[1]) + '\t\t' + str(graph.edge[edge[0]][edge[1]]['capacity']) + '\t\t' + str(graph.edge[edge[0]][edge[1]]['cost']) + '\n'

    output += ';\n\nend;\n'

    return output


if __name__ == '__main__':
    f = open('input', 'r')
    n_descr = int(f.readline())  # Número de descritores de instâncias
    for i in range(0, n_descr):
        error = ''

        n_inst = int(f.readline())  # Número de instâncias geradas para este descritor

        n_dem = int(f.readline())
        min_dem = 1
        if (n_dem < min_dem):
            error += 'O número de nós de demanda é menor do que o mínimo.\n'

        n_tr = int(f.readline())

        n_edge = int(f.readline())
        max_edge = (n_dem + n_tr + 1) * (n_dem + n_tr)  # arranjo dos nós em pares
        if (n_edge > max_edge):
            error += 'O número de arestas é maior do que o máximo.\n'

        u_dem = int(f.readline())
        min_u = 1
        if (u_dem < min_u):
            error += 'O limite superior para a demanda é menor do que o mínimo.\n'

        u_cap = int(f.readline())
        min_cap = 1
        while (u_cap < min_cap):
            error += 'Valor máximo de capacidade menor que o mínimo.\n'

        u_cost = int(f.readline())
        min_cost = 0
        while (u_cost < min_cost):
            error += 'Valor máximo de custos menor que o mínimo.\n'

        for j in range(0, n_inst):
            graph = nx.DiGraph()
            out = open('instancia' + str(i) + str(j), 'w')
            if error == '':
                generate_demands(graph, n_dem, u_dem)
                generate_transships(graph, n_tr)
                generate_source(graph)
                generate_edges(graph, n_edge, u_cap, u_cost)
                output = format_output(graph)
            else:
                output = error

            out.write(output)
            out.close()

    f.close()
