import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node('PV1')
G.add_node('PV2')
G.add_node('PV3')
G.add_node('PV4')
G.add_node('PV5')
G.add_node('PV6')
G.add_node('PV7')
G.add_node('PV8')
G.add_node('PV9')
G.add_node('PV10')

G.add_edge('PV1', 'PV4')
G.add_edge('PV1', 'PV2')
G.add_edge('PV1', 'PV3')
G.add_edge('PV4', 'PV5')
G.add_edge('PV3', 'PV5')
G.add_edge('PV3', 'PV2')
G.add_edge('PV3', 'PV6')
G.add_edge('PV2', 'PV6')
G.add_edge('PV2', 'PV7')
G.add_edge('PV3', 'PV8')
G.add_edge('PV4', 'PV9')
G.add_edge('PV5', 'PV10')
G.add_edge('PV10', 'PV6')

G['PV1']['PV4']['distancia'] = 12.60
G['PV1']['PV2']['distancia'] = 52.20
G['PV1']['PV3']['distancia'] = 139.60
G['PV4']['PV5']['distancia'] = 5.90
G['PV3']['PV5']['distancia'] = 36.80
G['PV3']['PV2']['distancia'] = 82.90
G['PV3']['PV6']['distancia'] = 5.60
G['PV2']['PV6']['distancia'] = 19.60
G['PV2']['PV7']['distancia'] = 20.60
G['PV3']['PV8']['distancia'] = 100.80
G['PV4']['PV9']['distancia'] = 63.70
G['PV5']['PV10']['distancia'] = 50.50
G['PV10']['PV6']['distancia'] = 54.50


tabela_heuristica = [
    ['PV1', "Boa"],
    ['PV2', "Média"],
    ['PV3', "Ruim"],
    ['PV4', "Ruim"],
    ['PV5', "Boa"],
    ['PV6', "Boa"],
    ['PV7', "Média"],
    ['PV8', "Boa"],
    ['PV9', "Média"],
    ['PV10', "Boa"]
]

print('Adicionando a distância dos PVs')
for edge in G.edges():
    u = edge[0]
    v = edge[1]
    print('A distância de ', edge, 'é', G[u][v]['distancia'])
print()

def dfs(grafo):
    def dfs_recursiva(grafo, vertice):
        visitados.add(vertice)
        print(vertice)
        for vizinho in grafo[vertice]:
            if vizinho not in visitados:
                dfs_recursiva(grafo, vizinho)

    visitados = set()
    for vertice in grafo:
        if not vertice in visitados:
            dfs_recursiva(grafo, vertice)

def bfs(graph, start_node):
    visited = set()
    queue = [start_node]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            print(node)
            visited.add(node)
            neighbors = list(graph.neighbors(node))  # Obtenha os vizinhos do nó
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)

def greedy_search(graph, start_node, goal_node):
    visited = set()
    current_node = start_node
    path_cost = 0

    while len(visited) < len(graph.nodes):
        print(current_node, end=' -> ')
        visited.add(current_node)
        neighbors = list(graph.neighbors(current_node))

        # Use a heurística para escolher o próximo nó
        min_cost = float('inf')
        next_node = None

        for neighbor in neighbors:
            if neighbor not in visited:
                cost = graph[current_node][neighbor]['distancia']
                if cost < min_cost:
                    min_cost = cost
                    next_node = neighbor

        if next_node == goal_node:
            print(goal_node, end='')
            break

        if next_node == None:
            print("Não existe caminho possível")
            return

        current_node = next_node
        path_cost += min_cost

    print("\nDistância percorrida:", path_cost)

def a_star_search(graph, start_node, goal_node):
    open_set = set()
    open_set.add(start_node)
    came_from = {}

    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0

    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start_node] = 0

    while open_set:
        current_node = min(open_set, key=lambda node: f_score[node])

        if current_node == goal_node:
            return reconstruct_path(came_from, current_node)

        open_set.remove(current_node)

        for neighbor in graph.neighbors(current_node):
            tentative_g_score = g_score[current_node] + graph[current_node][neighbor]['distancia']

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(g_score[neighbor], neighbor)

                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None

def heuristic(peso, pv):
    condicao = buscar_valor(tabela_heuristica,pv)
    if condicao == "Boa" and peso < 50:
        return 0
    if condicao == "Boa" and peso >= 50 and peso < 100:
        return 50
    if condicao == "Boa" and peso > 100:
        return 100
    if condicao == "Média" and peso < 50:
        return 50
    if condicao == "Média" and peso >= 50 and peso < 100:
        return 100
    if condicao == "Média" and peso > 100:
        return 150
    if condicao == "Ruim" and peso < 50:
        return 100
    if condicao == "Ruim" and peso >= 50 and peso < 100:
        return 150
    if condicao == "Ruim" and peso > 100:
        return 200

def reconstruct_path(came_from, current_node):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.insert(0, current_node)
    return path

def mostrarCaminho(path):
    if path:
        return "Caminho encontrado:", ' -> '.join(path)
    else:
        return "Caminho não encontrado."

def buscar_valor(matriz, valor):
    for linha, linha_lista in enumerate(matriz):
        for coluna, elemento in enumerate(linha_lista):
            if elemento == valor:
                return matriz[linha][1]
    return f'O valor {valor} não foi encontrado na matriz.'