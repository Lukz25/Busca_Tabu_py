
import networkx as ntx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random

def exibir_grafo_completo(dg):
    pos = ntx.shell_layout(dg)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,10))

    ntx.draw(dg, pos, node_color=list(range(dg.number_of_nodes())), node_size=600, cmap=plt.cm.Blues, with_labels=True, ax=ax1)
    ax1.set_title(f"Grafo com {dg.number_of_edges()} arestas")
    ax1.axis('off')


    dados = []
    for u, v, data in dg.edges(data=True):
        dados.append([f"{u}---{v}", data['dist'], data['traf']])

    table = ax2.table(
        cellText = dados,
        colLabels=['Aresta', 'Distância (Km)', 'Tráfego (%)'],
        loc='center',
        cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    ax2.axis('off')

    plt.tight_layout()
    plt.show()


def exibir_caminho(dg, caminho):
    fig = plt.figure(figsize=(16, 7))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2.5, 1])

    ax1 = plt.subplot(gs[0])  
    ax2 = plt.subplot(gs[1])  

    pos = ntx.shell_layout(dg)

    ntx.draw_networkx_nodes(dg, pos, node_color='lightblue', 
                        node_size=500, ax=ax1)

    ntx.draw_networkx_edges(dg, pos, edge_color='lightgray', 
                        width=1.5, ax=ax1)

    if caminho:

        dist_total = sum(float(dg[u][v]['dist']) for u, v in zip(caminho, caminho[1:]))*100
        traf_total = sum(float(dg[u][v]['traf']) for u, v in zip(caminho, caminho[1:]))*100

        caminho_arestas = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
        ntx.draw_networkx_edges(dg, pos, edgelist=caminho_arestas, 
                            edge_color='red', width=4, ax=ax1)
        
        ntx.draw_networkx_nodes(dg, pos, nodelist=caminho, 
                            node_color='red', node_size=550, ax=ax1)
        
        ntx.draw_networkx_nodes(dg, pos, nodelist=[caminho[0]], 
                            node_color='green', node_size=650, ax=ax1)
        
        ntx.draw_networkx_nodes(dg, pos, nodelist=[caminho[len(caminho)-1]], 
                            node_color='gold', node_size=650, ax=ax1)

    ntx.draw_networkx_labels(dg, pos, font_size=9, ax=ax1)

    edge_labels = {(u, v): f"{dg[u][v]['dist']*100} km" for u, v in dg.edges()}
    ntx.draw_networkx_edge_labels(dg, pos, edge_labels=edge_labels, 
                                font_size=6, ax=ax1)

    titulo = f'Menor Caminho: {caminho[0]} → {caminho[len(caminho)-1]} (Distância: {dist_total:.2f} Km)'

    ax1.set_title(titulo, fontsize=12, fontweight='bold')
    ax1.axis('off')

    if caminho:
        
        dados_tabela = []
        for i in range(len(caminho)-1):
            u = caminho[i]
            v = caminho[i+1]
            dados_tabela.append([
                f"{u}→{v}", 
                dg[u][v]['dist']*100, 
                dg[u][v]['traf']*100
            ])
        
        dados_tabela.append(['TOTAL', f'{dist_total:.2f}', f'{traf_total:.2f}'])
        
        table = ax2.table(
            cellText=dados_tabela,
            colLabels=['Aresta', 'Distância (km)', 'Tráfego (%)'],
            loc='center',
            cellLoc='center',
            colWidths=[0.25, 0.35, 0.35]
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(0.8, 1.3)
        
        for (i, j), cell in table.get_celld().items():
            if i == 0:  
                cell.set_facecolor('#4472C4')
                cell.set_text_props(color='white', fontweight='bold')
            elif i == len(dados_tabela) - 1:  
                cell.set_facecolor('#FFC000')
                cell.set_text_props(fontweight='bold')
            elif j == 0:  
                cell.set_facecolor('#E2EFDA')
            else:
                cell.set_facecolor('#F2F2F2' if i % 2 == 0 else 'white')
        
        ax2.axis('off')
        ax2.set_title("Detalhes do Caminho", fontsize=12, fontweight='bold', pad=20)

    else:
        ax2.text(0.5, 0.5, "Sem caminho\ndisponível", 
                ha='center', va='center', fontsize=14, color='red')
        ax2.axis('off')

    plt.suptitle(f"Análise do Grafo - Menor Caminho de {caminho[0]} para {caminho[len(caminho)-1]}", 
                fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.show()

def funcao_custo(dg, caminho):
    total_dist = sum(float(dg[u][v]['dist']) for u, v in zip(caminho, caminho[1:]))*100
    total_traf = sum(float(dg[u][v]['traf']) for u, v in zip(caminho, caminho[1:]))*100

    custo = (0.5*total_traf)+(0.5*total_dist)

    return custo

def melhor_vizinho(dg, caminhos):
    melhor = caminhos[0]
    melhor_valor = funcao_custo(dg, melhor)

    for i in range(1, len(caminhos)):
        vizinho = caminhos[i]
        valor_vizinho = funcao_custo(dg, caminhos[i])

        if(valor_vizinho < melhor_valor):
            melhor_valor = valor_vizinho
            melhor = vizinho 

    return melhor 

MAX_VERTICES=20

vertices = list(range(MAX_VERTICES))

dg = ntx.Graph()
dg.add_nodes_from(vertices)

for i in range(MAX_VERTICES*2):
    indice1 = random.randint(0,MAX_VERTICES-1)
    indice2 = random.randint(0,MAX_VERTICES-1)

    if indice1 != indice2:
        dg.add_edge(vertices[indice1], vertices[indice2], dist=random.randint(0,100)/100, traf=random.randint(0,100)/100)

origem = random.randint(0, MAX_VERTICES-1)
destino = 0

while True:
    destino = random.randint(1, MAX_VERTICES-1)

    if(destino != origem and ntx.has_path(dg, origem, destino)):
        break

caminhos = list(ntx.all_simple_paths(dg, origem, destino))

melhor = melhor_vizinho(dg, caminhos)
valor_melhor = funcao_custo(dg, melhor)

print(f'Pontuação melhor caminho: {valor_melhor}')   
exibir_caminho(dg, melhor)
