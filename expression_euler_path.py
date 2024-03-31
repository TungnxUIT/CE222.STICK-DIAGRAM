import queue
import networkx as nx


def precedence(operator):
    if operator == '+':
        return 1
    elif operator == '*':
        return 2
    else:
        return 0

def apply_operator(operand1, operand2, operator, q):
    expression = str(operand1) + str(operator) + str(operand2)
    q.append(expression)
    if operator == '+':
        return str(operand1) + str(operator) + str(operand2)
    else: return str(operand1) + str(operator) + str(operand2)

def count_max_degree(expression):
    max_count = 0
    count = 0
    for char in expression:
        if char == '(':
            count = 0
        elif char == ')':
            max_count = max(max_count, count)
            count = 0
        elif char == '+':
            count += 1
    return max(max_count, count) + 2

def evaluate_expression(expression, q):
    operand_stack = []
    operator_stack = []
    index = 0

    while index < len(expression):
        token = expression[index]
        if token.isalpha():
            operand_stack.append((token))
            index += 1
        elif token in '+-*/^':
            while (len(operator_stack) != 0 and precedence(operator_stack[-1]) >= precedence(token)):
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = apply_operator(operand1, operand2, operator, q)
                operand_stack.append(result)
            operator_stack.append(token)
            index += 1
        elif token == '(':
            operator_stack.append(token)
            index += 1
        elif token == ')':
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = apply_operator(operand1, operand2, operator, q)
                operand_stack.append(result)
            operator_stack.pop()  # pop the '('
            index += 1
        else:
            # Ignore spaces
            index += 1

    while len(operator_stack) != 0:
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = apply_operator(operand1, operand2, operator, q)
        operand_stack.append(result)

    return operand_stack.pop()

def subtract_expressions(expression1, expression2):
    i = 0
    j = 0
    result = ''
    while i < len(expression1):
        if(expression1[i] != expression2[j]):
            result += expression1[i]
            i += 1
        else:
            i += 1
            j += 1
        if j == len(expression2): break
    while i < len(expression1):
        result += expression1[i]
        i += 1
    
    return result
def intersection_expressions(expression1, expression2):
    i = 0
    j = 0
    result =''
    while i < len(expression1):
        if(expression1[i] == expression2[j]):
            result += expression1[i]
            i += 1
            j += 1
        else: i += 1
        if j == len(expression2): break
#    if not result: return 0
    return result


def create_node(g, node):
    node1 = node + 'S'
    node2 = node + 'D'
    g.add_node(node1)
    g.add_node(node2)
    g.add_edge(node1, node2)


def add_edge_parallel_1(g, node1, node2):
    n1 = node1 + 'S'
    n2 = node1 + 'D'
    n3 = node2 + 'S'
    n4 = node2 + 'D'
    g.add_edge(n1, n3)
    g.add_edge(n2, n4)
    

def add_edge_serial_1(g, node1, node2):
    n1 = node1 + 'S'
    n2 = node1 + 'D'
    n3 = node2 + 'S'
    n4 = node2 + 'D'
    g.add_edge(n3, n2)
    return

def add_edge_serial_2(g, node, inter_arr):
    n1 = node + 'S'
    n2 = node + 'D'
    i = j = 0
    node_connect1, node_degree1, i = lowest_degree_arr_node(g, 'D', i, inter_arr, '')
    node_connect2, node_degree2, j = lowest_degree_arr_node(g, 'D', j, inter_arr, node_connect1)
    g.add_edge(n1, node_connect1)
    g.add_edge(n1, node_connect2)

def add_edge_parallel_2(g, node):
    n1 = node + 'S'
    n2 = node + 'D'
    node1 = lowest_degree(g, 'S', node, node)
    node2 = lowest_degree(g, 'D', node, node)
    node1_degree = g.degree(node1)
    node2_degree = g.degree(node2)
    if node1_degree < node2_degree:
        s = 1
        g.add_edge(n1, node1)
    else:
        s = 2
        g.add_edge(n2, node2)
    if s == 1:
        node1 = node1[0]
        node_connect = lowest_degree(g, 'D', node, node1)
        g.add_edge(n2, node_connect)
    elif s == 2:
        node2 = node2[0]
        node_connect = lowest_degree(g, 'S', node, node2)
        g.add_edge(n1, node_connect)

def add_edge_parallel_3(g, inter_arr):
    i = 0
    j = 0
    n1 = n2 = n3 = n4 = ''
    n1_degree = n2_degree = n3_degree = n4_degree = 0
    n1, n1_degree, i = lowest_degree_arr_node(g, 'S', i, inter_arr, '')
    t1 = i
    n2, n2_degree, i = lowest_degree_arr_node(g, 'S', i, inter_arr, '')
    n3, n3_degree, j = lowest_degree_arr_node(g, 'D', j, inter_arr, '')
    n4, n4_degree, j = lowest_degree_arr_node(g, 'D', j, inter_arr, '')
    if n1_degree + n2_degree < n3_degree + n4_degree :
        sel = 0
        g.add_edge(n1, n2)      #S->S
    else:
        sel = 1
        g.add_edge(n3, n4)      #D->D
    if sel == 1 :   #connect S -> S
        except_node = n4[0]
        node_connect, node_degree, t1 = lowest_degree_arr_node(g, 'S', t1, inter_arr, except_node)
        g.add_edge(n1, node_connect)
    else:           #connect d->D
        except_node = n2[0]
        node_connect, node_degree, t1 = lowest_degree_arr_node(g, 'D', t1, inter_arr, except_node)
        g.add_edge(n3, node_connect)
    return
def add_edge_serial_3(g, inter_arr):
    i = 0
    min_degree1 = 100
    min_degree2 = 100
    while 1:
        if inter_arr[i] == 0:
            i += 1
            break
        n1_degree = g.degree(inter_arr[i] + 'S')
        n1 = inter_arr[i] + 'S'
        if n1_degree < min_degree1:
            min_node1 = n1
            min_degree1 = n1_degree
        i += 1
    if i < len(inter_arr):
        while 1:
            if inter_arr[i] == 0: break
            n2_degree = g.degree(inter_arr[i] + 'D')
            n2 = inter_arr[i] + 'D'
            if n2_degree < min_degree2:
                min_node2 = n2
                min_degree2 = n2_degree
            i += 1
        g.add_edge(min_node1, min_node2)

def lowest_degree_arr_node(g, k, i, inter_arr, except_node):
    t = i
    min_degree1 = 100
    min_degree2 = 100
    while 1:
        if inter_arr[t] == 0:
            t += 1
            break
        n1_degree = g.degree(inter_arr[t] + k)
        n1 = inter_arr[t] + k
        if (n1_degree < min_degree1) and (n1 != except_node):
            min_node1 = n1
            min_degree1 = n1_degree
        t += 1
    return min_node1, min_degree1, t

def lowest_degree(g, k, except_node1, except_node2):
    degrees = dict(g.degree())
    if except_node1 != '':
        degrees.pop(except_node1 + 'S', None)
        degrees.pop(except_node1 + 'D', None)
    if except_node2 != '':
        degrees.pop(except_node2 + 'S', None)
        degrees.pop(except_node2 + 'D', None)
    filtered_degrees = {node: degree for node, degree in degrees.items() if node[-1] == k}
    lowest_degree_node = min(filtered_degrees, key=degrees.get)
    return lowest_degree_node

def create_graph(g, q, i, expression):
    inter_arr = []
    t = i - 1
    expre = expression
    while t >= 0:
        element = q[t]
        inter = intersection_expressions(expre, element)
        if len(inter) > 0:
            for char in inter:
                if char.isalpha():
                    inter_arr.append(char)
            inter_arr.append(0)
        remain = subtract_expressions(expre, element)
        if len(remain) > 0:
            expre = remain
        t -= 1
    if expre == expression:
        sel = 0
        for token in expression:
            if token.isalpha():
                create_node(g, token)
                if sel == 0:
                   sel = 1
                   node1 = token
                else:
                    node2 = token
                   
            elif token in '+*':
                operator = precedence(token)
                
        if operator == 1:
            add_edge_parallel_1(g, node1, node2)
        else:
            add_edge_serial_1(g, node1, node2)

    else:
        node = ''
        for token in expre:
            
            if token in '+*':
                operator = precedence(token)
            elif token.isalpha():
                node = token
                create_node(g, token)
        if operator == 1:
            if len(node) > 0:
                add_edge_parallel_2(g, node)
            else:
                add_edge_parallel_3(g, inter_arr)
        else:
            if len(node):
                add_edge_serial_2(g, node, inter_arr)
            else:
                add_edge_serial_3(g, inter_arr)
    return g

def initial_graph(g, expression):
    q = []
    evaluate_expression(expression, q)
    i = 0
    while i < len(q):
        create_graph(g, q, i, q[i])
        i += 1
    return g


def is_valid_next_node(v, path, G):
    # Kiểm tra xem đỉnh v đã được thêm vào path chưa
    if v in path:
        return False
    #Kiểm tra các node S D có nằm cạnh nhau không
    last_node = path[-1]
    if last_node[0] != v[0] :
        if last_node[1] == 'S':
            x = last_node[0] + 'D'
            if x in path:
                return True
            else: return False
        if last_node[1] == 'D':
            x = last_node[0] + 'S'
            if x in path:
                return True
            else: return False

    # Kiểm tra xem đỉnh v có kề với đỉnh cuối cùng của path không
    if not path or v in G.neighbors(path[-1]):
        return True
    return False


def hamiltonian_dfs(G, start, path=[]):
    path = path + [start]
    if len(path) == len(G.nodes()):
        return path
    for v in G.neighbors(start):
        if is_valid_next_node(v, path, G):
            new_path = hamiltonian_dfs(G, v, path)
            if new_path:
                return new_path
    return None

def find_hamilton_path(g):
    path = []
    for node in g.nodes():
        path = hamiltonian_dfs(g, node)
        if path :
            break
        path = []
    if len(path) > 0:
        return path
    else: return None

def euler_path(g):
    euler_path_nmos = find_hamilton_path(g)
    if not euler_path_nmos:
        return None
    euler_path_pmos = [None] * len(euler_path_nmos)
    i = 0
    s = False
    while i < len(euler_path_nmos) - 1:
        if s == True:
            euler_path_pmos[i] = euler_path_nmos[i+1]
            euler_path_pmos[i+1] = euler_path_nmos[i]
        else:
            euler_path_pmos[i] = euler_path_nmos[i]
            euler_path_pmos[i+1] = euler_path_nmos[i+1]
        s = not s
        i += 2
    return euler_path_nmos, euler_path_pmos

# Test the function
#'''
g = nx.Graph()
#expression = input()
expression = "A*(B+C)+D"
g = initial_graph(g, expression)
euler_path_nmos, euler_path_pmos = euler_path(g)
print("NMOS: ", euler_path_nmos)
print("PMOS: ", euler_path_pmos)


