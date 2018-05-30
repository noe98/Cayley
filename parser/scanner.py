"""
File: scanner.py
Project: Research for Irina Mazilu, Ph.D.

A scanner for processing languages.
"""

from tokens import Token

class Scanner(object):
    """A scanner for simple languages."""

    EOE = ';'        # end-of-expression
    TAB = '\t'       # tab

    def __init__(self, sourceStr):
        self._sourceStr = sourceStr
        self._getFirstToken()

    def hasNextToken(self):
        """Returns True if there is a next token,
        or False otherwise."""
        return self._currentToken != None

    def nextToken(self):
        """Returns the next token.
        Precondition: hashNext returns True.
        Raises: Exception if hasNext returns False."""
        if not self.hasNextToken():
            raise Exception("There are no more tokens")            
        temp = self._currentToken
        self._getNextToken()
        return temp

    def __iter__(self):
        """Returns an iterator on self."""
        while self.hasNextToken():
            yield self.nextToken()

    def _getFirstToken(self):
        """Sets the index to the first letter in the expression.
         In this implentation the first number of the equation."""
        self._index = 0
        self._currentChar = self._sourceStr[0] #current character in source string
        self._getNextToken()
        #print(self._currentChar)
    
    def _getNextToken(self):
        """Finds the next letter or token in the language."""
        self._skipWhiteSpace()
        if self._currentChar.isdigit():
            self._currentToken = Token(self._getInteger())
            #print(self._currentToken)
        elif self._currentChar == Scanner.EOE:
            self._currentToken = None
        else:
            self._currentToken = Token(self._currentChar)
            self._nextChar()
            #print(self._currentToken)
    
    def _nextChar(self):
        """Increments the index in the source string."""
        if self._index >= len(self._sourceStr) - 1:
            self._currentChar = Scanner.EOE
        else:
            self._index += 1
            self._currentChar = self._sourceStr[self._index]
    
    def _skipWhiteSpace(self):
        """Skips the whitespace in the language."""
        while self._currentChar in (' ', Scanner.TAB):
            self._nextChar()
    
    def _getInteger(self):
        """Find and recognizes the integer or float from the source string."""
        num = str()
        while self._currentChar.isdigit() or self._currentChar == '.':
            if self._currentChar == '.' and num.count('.') < 1:
                num = num + '.'
                self._nextChar()
            elif self._currentChar.isdigit():
                num = num + self._currentChar
                self._nextChar()
            else:
                raise ValueError("Improper use of decimal")
        return float(num)
      

def test():
    """A simple tester program."""
    while True:
        sourceStr = input("Enter an expression: ")
        if sourceStr == "": break
        print("Token strings:")
        scanner = Scanner(sourceStr)
        for token in scanner:
            print(token)

if __name__ == '__main__': 
    test()

