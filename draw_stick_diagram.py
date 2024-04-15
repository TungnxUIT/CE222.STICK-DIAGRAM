import matplotlib.pyplot as plt
from itertools import combinations
from invertation import *
from expression_euler_path import *
expression = input()
g_nmos, g_pmos, euler_path_nmos, euler_path_pmos, source_nodes_nmos, out_nodes_nmos,source_nodes_pmos, out_nodes_pmos = Create_All(expression)
logic_elements = []
seen = set()
for node in euler_path_nmos:
    if node[0] not in seen:
        logic_elements.append(node[0])
        seen.add(node[0])
def draw_stick_diagram(g_nmos, g_pmos, euler_path_nmos,euler_path_pmos,logic_elements):
    fig, ax = plt.subplots();  
    ax.set_aspect('equal')
    ax.plot([-2.5, 12], [6, 6], 'b-', linewidth=2) 
    ax.text(12.5, 6, 'Vdd', verticalalignment='center', fontsize=12)
    ax.plot([-2.5, 12], [-1, -1], 'b-', linewidth=2) 
    ax.text(12.5, -1, 'Gnd', verticalalignment='center', fontsize=12)
    ax.plot([-1.5, 11], [5, 5], 'y-', linewidth=2)
    ax.plot([-1.5, 11], [0, 0], 'g-', linewidth=2)
    for element in logic_elements:
        x = 1.5 + logic_elements.index(element) * 2
        count = logic_elements.index(element)*2
        ax.plot([x, x], [-0.5, 5.5], 'r-')
        ax.text(x, 5.6, element, horizontalalignment='center', fontsize=10, color='black')
    coordinates_pmos = {}
    for pmos in euler_path_pmos:
        x = 1 + euler_path_pmos.index(pmos)
        ax.text(x,5.1,pmos,horizontalalignment='center', fontsize=10, color='red')
        coordinates_pmos[pmos] = (x, 5)
    count = 0.2
    for edge in g_pmos.edges:
        node1, node2 = edge
        if node1 in coordinates_pmos and node2 in coordinates_pmos:
            x1, y1 = coordinates_pmos[node1]
            x2, y2 = coordinates_pmos[node2]
            if(abs(x2-x1) > 1):
                ax.plot([x1, x1], [y1, y1-count], 'b-', linewidth=1)
                ax.plot([x2, x2], [y2, y2-count], 'b-', linewidth=1) 
                ax.plot([x1, x2], [y1-count, y2-count], 'b-', linewidth=1) 
                ax.scatter(x1, y1, color='black', marker='x', s=50)
                ax.scatter(x2, y2, color='black', marker='x', s=50)
        count += 0.2 
    coordinates_nmos = {}
    for nmos in euler_path_nmos:
        x = 1 + euler_path_nmos.index(nmos)
        ax.text(x,0.1,nmos,horizontalalignment='center', fontsize=10, color='red')
        coordinates_nmos[nmos] = (x, 0)
    count = 0.2
    for edge in g_nmos.edges:
        node1, node2 = edge
        if node1 in coordinates_nmos and node2 in coordinates_nmos:
            x1, y1 = coordinates_nmos[node1]
            x2, y2 = coordinates_nmos[node2]
            if(abs(x2-x1) > 1):
                ax.plot([x1, x1], [y1, y1+count], 'b-', linewidth=1)
                ax.plot([x2, x2], [y2, y2+count], 'b-', linewidth=1) 
                ax.plot([x1, x2], [y1+count, y2+count], 'b-', linewidth=1) 
                ax.scatter(x1, y1, color='black', marker='x', s=50)
                ax.scatter(x2, y2, color='black', marker='x', s=50)
        count += 0.2 
    if len(set(source_nodes_pmos)) > 1:    
         for node1, node2 in combinations(set(source_nodes_pmos), 2):
            x1,y1 = coordinates_pmos[node1]
            x2,y2 = coordinates_pmos[node2]
            if(abs(x2-x1) == 1):
                x3 = (x1 + x2) /2
                ax.plot([x3,x3],[5,6],'b', linewidth=1)
                ax.scatter(x3, 5, color='black', marker='x', s=50)
    else: 
        for node in set(source_nodes_pmos):
            if node in coordinates_pmos:
                x1,y1 = coordinates_pmos[node]
                ax.plot([x1,x1],[5,6],'b', linewidth=1)
                ax.scatter(x1, 5, color='black', marker='x', s=50)
    if len(set(source_nodes_nmos)) > 1:    
         for node1, node2 in combinations(set(source_nodes_nmos), 2):
            x1,y1 = coordinates_nmos[node1]
            x2,y2 = coordinates_nmos[node2]
            if(abs(x2-x1) == 1):
                x3 = (x1 + x2) /2
                ax.plot([x3,x3],[0,-1],'b', linewidth=1)
                ax.scatter(x3, 0, color='black', marker='x', s=50)
    else: 
        for node in set(source_nodes_nmos):
            if node in coordinates_nmos:
                x1,y1 = coordinates_nmos[node]
                ax.plot([x1,x1],[0,-1],'b', linewidth=1)
                ax.scatter(x1, 0, color='black', marker='x', s=50)
    ax.text(12,2.5,'Y',horizontalalignment='center', fontsize=15, color='red')
    if len(set(out_nodes_pmos)) > 1:    
         for node1, node2 in combinations(set(out_nodes_pmos), 2):
            x1,y1 = coordinates_pmos[node1]
            x2,y2 = coordinates_pmos[node2]
            if(abs(x2-x1) == 1):
                x3 = (x1 + x2) /2
                y3 = (y1 + y2) /2
                ax.plot([x3,x3],[y3-2.5,y3],'b', linewidth=1)
                ax.plot([x3,12],[y3-2.5,2.5],'b', linewidth=1)
                ax.scatter(x3, y3, color='black', marker='x', s=50)
            else: 
                for node_pmos in set(out_nodes_pmos):
                    if node_pmos in coordinates_pmos: 
                        x1,y1 = coordinates_pmos[node_pmos]
                        ax.plot([x1,x1],[y1-2.5,y1],'b', linewidth=1)
                        ax.plot([x1,12],[y1-2.5,2.5],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
    else: 
        for node_pmos in set(out_nodes_pmos):
            if node_pmos in coordinates_pmos: 
                x1,y1 = coordinates_pmos[node_pmos]
                ax.plot([x1,x1],[y1-2.5,5],'b', linewidth=1)
                ax.plot([x1,12],[y1-2.5,2.5],'b', linewidth=1)
                ax.scatter(x1, 5, color='black', marker='x', s=50)
    if len(set(out_nodes_nmos)) > 1:    
         for node1, node2 in combinations(set(out_nodes_nmos), 2):
            x1,y1 = coordinates_nmos[node1]
            x2,y2 = coordinates_nmos[node2]
            if(abs(x2-x1) == 1):
                x3 = (x1 + x2) /2
                y3 = (y1 + y2) /2
                ax.plot([x3,x3],[y3+2.5,y3],'b', linewidth=1)
                ax.plot([x3,12],[y3+2.5,2.5],'b', linewidth=1)
                ax.scatter(x3, y3, color='black', marker='x', s=50)
            else: 
                for node_nmos in set(out_nodes_nmos):
                    if node_nmos in coordinates_nmos:
                        x1,y1 = coordinates_nmos[node_nmos]
                        ax.plot([x1,x1],[y1+2.5,y1],'b', linewidth=1)
                        ax.plot([x1,12],[y1+2.5,2.5],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
    else: 
        for node_nmos in set(out_nodes_nmos):
            if node_nmos in coordinates_nmos:
                x1,y1 = coordinates_nmos[node_nmos]
                ax.plot([x1,x1],[y1+2.5,y1],'b', linewidth=1)
                ax.plot([x1,12],[y1+2.5,2.5],'b', linewidth=1)
                ax.scatter(x1, y1, color='black', marker='x', s=50)
    ax.axis('off')
    plt.show()


