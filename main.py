import Grafo as Gr

input()
print('Busca em profundidade:')
Gr.dfs(Gr.G)
print()

input()
print('Busca em largura:')
Gr.bfs(Gr.G, 'PV1')
print()

print('Busca Gulosa')
origem = input("Digite o PV de origem: ")
destino = input("Digite o PV de destino: ")
Gr.greedy_search(Gr.G, origem, destino)
print()

print("Caminho A* ")
origem = input("Digite o PV de origem: ")
destino = input("Digite o PV de destino: ")
print(Gr.mostrarCaminho(Gr.a_star_search(Gr.G, origem, destino)))

print('Plotando o grafo como imagem...')

edge_labels = {(u, v): d['distancia'] for u, v, d in Gr.G.edges(data=True)}

pos = Gr.nx.spring_layout(Gr.G)

Gr.plt.figure(figsize=(8, 6))
Gr.nx.draw(Gr.G, pos, with_labels=True, node_size=500, node_color='blue', font_size=10, font_color='black')
Gr.nx.draw_networkx_edge_labels(Gr.G, pos, edge_labels=edge_labels, font_size=10)
Gr.plt.axis('off')
Gr.plt.show()
