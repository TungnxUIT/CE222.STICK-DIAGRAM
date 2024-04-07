def precedence_inv(operator):
    if operator == '+':
        return 1
    elif operator == '*':
        return 2
    else:
        return 0

def apply_operator_inv(operand1, operand2, operator):
    expression = str(operand1) + str(operator) + str(operand2)
    #q.append(expression)
    if operator == '+':
        return str(operand1) + '*' + str(operand2)
    else: return str(operand1) + '+' + str(operand2)


def evaluate_expression_inv(expression, q):
    operand_stack = []
    operator_stack = []
    index = 0

    while index < len(expression):
        token = expression[index]
        if token.isalpha():
            operand_stack.append((token))
            index += 1
        elif token in '+-*/^':
            while (len(operator_stack) != 0 and precedence_inv(operator_stack[-1]) >= precedence_inv(token)):
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = apply_operator_inv(operand1, operand2, operator)
                q.append(result)
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
                result = apply_operator_inv(operand1, operand2, operator)
                q.append(result)
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
        result = apply_operator_inv(operand1, operand2, operator)
        q.append(result)
        operand_stack.append(result)

    return operand_stack.pop()


