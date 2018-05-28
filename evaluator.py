"""
Author: Justin Pusztay
File: evaluator.py
Project: Research for Irina Mazilu, Ph.D.

Contains the Evaluator class, which evaluates a postfix expression.  
"""

from tokens import Token
from scanner import Scanner
from linkedstack import LinkedStack

class Evaluator(object):
    """Evaluator for postfix expressions.
    Assumes that the input is a syntactically correct
    sequence of tokens."""
   
    def __init__(self, scanner):
        """Sets the initial state of the evaluator."""
        self._operandStack = LinkedStack()
        self._scanner = scanner

    def evaluate(self):
        """Returns the value of the postfix expression."""
        for currentToken in self._scanner:
            if currentToken.getType() == Token.INT:
                self._operandStack.push(currentToken)
            elif currentToken.getType() == Token.FLOAT:
                self._operandStack.push(currentToken)
            elif currentToken.isOperator(): 
                right = self._operandStack.pop()
                left = self._operandStack.pop()
                result = Token(self._computeValue(currentToken,
                                                  left.getValue(),
                                                  right.getValue()))
                self._operandStack.push(result)
        result = self._operandStack.pop()
        return result.getValue();   

    def _computeValue(self, op, value1, value2):
        """Utility routine to compute a value."""
        result = 0
        theType = op.getType()
        if theType == Token.PLUS:
            result = value1 + value2
        elif theType == Token.MINUS:
            result = value1 - value2
        elif theType == Token.MUL:
            result = value1 * value2
        elif theType == Token.POWER:
            result = value1 ** value2
        elif theType == Token.MOD:
            if value2 == 0:
                raise ZeroDivisionError("Attempt to divide by 0")
            else:
                result = value1%value2
        elif theType == Token.DIV:
            if value2 == 0:
                raise ZeroDivisionError("Attempt to divide by 0")
            else:
                result = value1 // value2
        return result

def main():
    """Tester function for the evaluator."""
    while True:
        sourceStr = input("Enter a postfix expression: ")
        if sourceStr == "": break
        try:
            evaluator = Evaluator(Scanner(sourceStr))
            print("The value is", evaluator.evaluate())
        except Exception as e:
            print("Exception:", str(e))

if __name__ == '__main__': 
    main()
            


