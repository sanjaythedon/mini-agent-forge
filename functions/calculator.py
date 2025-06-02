
def tokenize(expression):
    """
    Returns each tokens seperately from the expression as a list
    '2+2*5' -> ['2', '+', '2', '*', '5']
    """
    tokens = []
    num = ''
    for char in expression:
        if char.isdigit():
            num += char
        else:
            if num:
                tokens.append(num)
                num = ''
            if char in '+-*/()':
                tokens.append(char)
    if num:
        tokens.append(num)
    return tokens

def to_reverse_polish_notation(tokens):
    """
    Converts the list to Reverse Polish Notation
    ['2', '+', '2', '*', '5'] -> ['2', '2', '5', '*', '+']
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []
    
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in '+-*/':
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Pop '('
    
    while stack:
        output.append(stack.pop())
    
    return output

def evaluate_postfix(postfix):
    """
    Evaluates the Reverse Polish Notation expression
    ['2', '2', '5', '*', '+'] -> 12
    """
    stack = []
    
    for token in postfix:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a // b)  # Integer division, or use a / b for float division
    
    return stack[0]

def evaluate_expression(expression):
    """
    Aggregates all functions to evaluate the expression
    '2+2*5' -> 12
    """
    tokens = tokenize(expression)
    postfix = to_reverse_polish_notation(tokens)
    result = evaluate_postfix(postfix)
    return result

if __name__ == "__main__":  
    # Test it
    expr = '(3+4)*(2+5)'
    print(evaluate_expression(expr))  # Output: 12
