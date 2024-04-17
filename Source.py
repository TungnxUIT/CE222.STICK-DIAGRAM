from expression_euler_path import *
from draw_stick_diagram import *

expression = "A*(B+C)+D*E"
g_nmos, g_pmos, euler_path_nmos, euler_path_pmos, source_nodes_nmos, out_nodes_nmos,source_nodes_pmos, out_nodes_pmos = Create_All(expression)
logic_elements = []
seen = set()
for node in euler_path_nmos:
    if node[0] not in seen:
        logic_elements.append(node[0])
        seen.add(node[0])

print("Euler path PMOS: ", euler_path_pmos)
print("Euler path NMOS: ", euler_path_nmos)
print("pMOS edges: ",g_pmos.edges())   
print("NMOS edges: ",g_nmos.edges()) 
print("Node connect Source PMOS (VCC):")
print(source_nodes_pmos)
print("Node connect Source NMOS (GND):")
print(source_nodes_nmos)
print("Node connect Output PMOS (OUT):")
print(out_nodes_pmos)
print("Node connect Output NMOS (OUT):")
print(out_nodes_nmos)
draw_stick_diagram(g_nmos, g_pmos, euler_path_nmos,euler_path_pmos,logic_elements, source_nodes_nmos, source_nodes_pmos, out_nodes_nmos, out_nodes_pmos)