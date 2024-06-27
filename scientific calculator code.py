import math
import re

# Stack implementation using List
class Stack:
    def __init__(self):
        """Initialize an empty stack."""
        self.items = []

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0

    def push(self, item):
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self):
        """Pop an item from the stack. Returns None if empty."""
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def peek(self):
        """Peek at the top item of the stack without removing it. Returns None if empty."""
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def size(self):
        """Return the size of the stack."""
        return len(self.items)

# Infix to Postfix conversion
def infix_to_postfix(infix_expression):
    """
    Converts an infix expression to postfix notation using a stack.
    Handles basic arithmetic and trigonometric functions.
    """
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    functions = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'log10', 'sqrt', 'exp', 'factorial', 'round', 'floor', 'ceil'}
    postfix_expression = []
    operator_stack = Stack()

    tokens = re.findall(r"(\bexp\b|\bsin\b|\bcos\b|\btan\b|\basin\b|\bacos\b|\batan\b|\blog\b|\blog10\b|\bsqrt\b|\bfactorial\b|\bround\b|\bfloor\b|\bceil\b|\d+\.?\d*|[-+*/^()]|\w+)", infix_expression)

    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            postfix_expression.append(token)
        elif token in functions:
            operator_stack.push(token)
        elif token == '(':
            operator_stack.push(token)
        elif token == ')':
            while operator_stack.peek() != '(':
                postfix_expression.append(operator_stack.pop())
            operator_stack.pop()  # Remove the '('
            if not operator_stack.is_empty() and operator_stack.peek() in functions:
                postfix_expression.append(operator_stack.pop())
        else:
            while (not operator_stack.is_empty() and
                   operator_stack.peek() != '(' and
                   precedence.get(operator_stack.peek(), 0) >= precedence.get(token, 0)):
                postfix_expression.append(operator_stack.pop())
            operator_stack.push(token)

    while not operator_stack.is_empty():
        postfix_expression.append(operator_stack.pop())

    return ' '.join(postfix_expression)

# Evaluate Postfix expression
def evaluate_postfix(postfix_expression):
    """
    Evaluates a postfix expression using a stack.
    Supports arithmetic, trigonometric, logarithmic, and other functions.
    """
    operand_stack = Stack()

    for token in postfix_expression.split():
        if token.replace('.', '', 1).isdigit():
            operand_stack.push(float(token))
        elif token in ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'asin', 'acos', 'atan', 'log10', 'exp2']:
            operand = operand_stack.pop()
            if token == 'sin':
                result = math.sin(math.radians(operand))
            elif token == 'cos':
                result = math.cos(math.radians(operand))
            elif token == 'tan':
                result = math.tan(math.radians(operand))
            elif token == 'log':
                result = math.log(operand)
            elif token == 'sqrt':
                result = math.sqrt(operand)
            elif token == 'exp':
                result = math.exp(operand)
            elif token == 'asin':
                result = math.degrees(math.asin(operand))
            elif token == 'acos':
                result = math.degrees(math.acos(operand))
            elif token == 'atan':
                result = math.degrees(math.atan(operand))
            elif token == 'log10':
                result = math.log10(operand)
            elif token == 'exp2':
                result = 2 ** operand
            operand_stack.push(result)
        elif token == 'factorial':
            operand = operand_stack.pop()
            result = math.factorial(int(operand))
            operand_stack.push(result)
        elif token == 'round':
            operand = operand_stack.pop()
            result = round(operand)
            operand_stack.push(result)
        elif token == 'floor':
            operand = operand_stack.pop()
            result = math.floor(operand)
            operand_stack.push(result)
        elif token == 'ceil':
            operand = operand_stack.pop()
            result = math.ceil(operand)
            operand_stack.push(result)
        elif token in ['+', '-', '*', '/', '^']:
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                if operand2 != 0:
                    result = operand1 / operand2
                else:
                    raise ZeroDivisionError("Cannot divide by zero!")
            elif token == '^':
                result = operand1 ** operand2
            operand_stack.push(result)

    return operand_stack.pop()

# Additional mathematical utility functions

def integrate_polynomial(coefficients, lower_bound, upper_bound):
    """
    Numerically integrates a polynomial between lower_bound and upper_bound.
    Coefficients are provided in descending order.
    """
    def polynomial(x):
        return sum(coef * (x ** i) for i, coef in enumerate(reversed(coefficients)))

    steps = 1000  # Number of steps for numerical integration
    step_size = (upper_bound - lower_bound) / steps
    area = 0.0

    for step in range(steps):
        x = lower_bound + step * step_size
        area += polynomial(x) * step_size

    return area

def differentiate_polynomial(coefficients):
    """
    Differentiates a polynomial given by coefficients in descending order.
    Returns the coefficients of the derivative.
    """
    return [coef * (len(coefficients) - i - 1) for i, coef in enumerate(coefficients[:-1])]

# Trigonometric utility functions for enhanced expression support

def degree_to_radian(angle):
    """Convert angle from degrees to radians."""
    return angle * (math.pi / 180)

def radian_to_degree(angle):
    """Convert angle from radians to degrees."""
    return angle * (180 / math.pi)

# Error handling improvements and validations

def validate_expression(expression):
    """
    Validates the infix expression for balanced parentheses and allowed characters.
    """
    stack = Stack()
    allowed_chars = "0123456789+-*/^(). "

    for char in expression:
        if char not in allowed_chars and not char.isalpha():
            raise ValueError(f"Invalid character in expression: {char}")
        if char == '(':
            stack.push(char)
        elif char == ')':
            if stack.is_empty():
                raise ValueError("Unmatched closing parenthesis")
            stack.pop()

    if not stack.is_empty():
        raise ValueError("Unmatched opening parenthesis")

    return True

# Example Usage and Test Cases

if __name__ == "__main__":
    examples = [
        "3 + 5 * 2",
        "sin(30) + cos(60)",
        "10 + (3 * 4) ^ 2 - sqrt(81)",
        "exp(1) + log10(100)",
        "factorial(5) / (2 * 2)"
    ]

    for infix in examples:
        try:
            print(f"Infix: {infix}")
            validate_expression(infix)
            postfix = infix_to_postfix(infix)
            print(f"Postfix: {postfix}")
            result = evaluate_postfix(postfix)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error processing expression '{infix}': {e}\n")

    # Polynomial integration example
    poly_coeffs = [1, 0, -4]  # Represents x^2 - 4
    area = integrate_polynomial(poly_coeffs, 0, 2)
    print(f"Area under polynomial {poly_coeffs} from 0 to 2: {area}")

    # Polynomial differentiation example
    derived_coeffs = differentiate_polynomial(poly_coeffs)
    print(f"Derivative of polynomial {poly_coeffs}: {derived_coeffs}")

    # Angle conversion example
    angle_deg = 90
    angle_rad = degree_to_radian(angle_deg)
    print(f"{angle_deg} degrees is {angle_rad} radians")
    print(f"{angle_rad} radians is {radian_to_degree(angle_rad)} degrees")
