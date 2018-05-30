"""
Author: Justin Pusztay 
Filename: translator.py
Project: Research for Irina Mazilu, Ph.D.

Contains the Translator class. The Translator takes Scanner objects
and converts the infix source string to a postfix expression. 
"""

from tokens import Token
from scanner import Scanner
from Cayley.linkedstack import *

class Translator(object):
    """Translates infix expressions to postfix expressions."""

    def __init__(self, scanner):
        """Sets the initial state of the translator."""
        self._expressionSoFar = ""
        self._operatorStack = LinkedStack()
        self._scanner = scanner

    def translate(self):
        """Returns a list of tokens that represent the postfix
        form of sourceStr.  Assumes that the infix expression
        in sourceStr is syntactically correct"""
        self.postfix = list()
        for currentToken in self._scanner:
            self._expressionSoFar += str(currentToken) + " "
            if currentToken.getType() == Token.INT or \
               currentToken.getType() == Token.FLOAT or \
               currentToken.getType() == Token.VAR:
                self.postfix.append(currentToken)
            elif currentToken.getType() == Token.LPAR:
                self._operatorStack.push(currentToken)
            elif currentToken.getType() == Token.RPAR:
                topOperator = self._operatorStack.pop()
                while topOperator.getType() != Token.LPAR:
                    self.postfix.append(topOperator)
                    topOperator = self._operatorStack.pop()
            elif currentToken.getType() == Token.POWER:
                self._operatorStack.push(currentToken)
            else:
                while not self._operatorStack.isEmpty() and \
                      self._operatorStack.peek().getPrecedence() >= \
                      currentToken.getPrecedence():
                    self.postfix.append(self._operatorStack.pop())
                self._operatorStack.push(currentToken)
        while not self._operatorStack.isEmpty():
            self.postfix.append(self._operatorStack.pop())
        return self.postfix
   
    def __str__(self):
        """Returns a string containing the contents of the expression
        processed and the stack to this point."""
        result = "\n"
        if self._expressionSoFar == "":
            result += "Portion of expression processed: none\n"
        else: 
            result += "Portion of expression processed: " + \
                   self._expressionSoFar + "\n"
        if self._operatorStack.isEmpty():
            result += "The stack is empty"
        else:
            result += "Operators on the stack          : " + \
                      str(self._operatorStack)
        return result

    def translationStatus(self):
        """Returns how much of the expression was processed."""
        return str(self)

    def getStack(self):
        return self._operatorStack

def main():
    """Tester function for translators."""
    while True:
        sourceStr = input("Enter an infix expression: ")
        if sourceStr == "":
            break
        else:
            try:
                translator = Translator(Scanner(sourceStr))
                postfix = translator.translate()
                print("Postfix:", end =" ")
                for token in postfix: print(token, end=" ")
                print()
            except Exception as e:
                print("Error: ", e, translator.translationStatus())

if __name__ == '__main__': 
    main()

