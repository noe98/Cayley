"""
Authors: Justin Pusztay
Filename: probability.py
Project: Research for Irina Mazilu, Ph.D.

Contains the Probability class. The class creates a probability function object,
which can have variables with values plugged into them. It also can evaluate an
equation by translating the function to postfix notation and evaluating it there.
"""


__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['Probability']

from Cayley.parser.scanner import Scanner
from Cayley.parser.translator import Translator
from Cayley.parser.evaluator import Evaluator

class Probability(object):
    
    def __init__(self,function):
        """The probability function must be a string. The variables will be
        automatically detected. To have parser work, all operations must be
        written out according to the grammar."""
        self.function = function
        self.originalFunction = function
        if type(self.function) != str:
            raise TypeError("Function must inputed as a string")
        self.findVariables()

    def parser(self):
        """Plugs in values for the variables and then evaluates the expression."""
        for var in self.variables:
            self.function = self.function.replace(var,str(self.variables[var]))
        try:
            scanner = Scanner(self.function)
            translator = Translator(scanner)
            postfix = translator.translate()
            evaluator = Evaluator(postfix)
            return evaluator.evaluate()
        except Exception as e:
            print("Error:", e, translator.translationStatus())

    def findVariables(self):
        """Finds the variables in the probability function."""
        self.variables = dict()
        for char in self.function:
            if char.lower() in "abcdefghigjklmnopqrstuvwxyz":
                self.variables[char] = None

    def setVariable(self,var,value):
        """Sets a specific value for the variable."""
        var = str(var)
        value = float(value)
        if var in self.variables:
            self.variables[var] = value
        else:
            raise Exception("Variable not in probability function")

    def getFunction(self):
        return self.originalFunction

#Example of how the Probility object can be used
def main():
    a = Probability("3*x*(1+0.2*y)")
    print("Original Function: ",a.getFunction())
    a.setVariable('x',1.2)
    a.setVariable('y',0.2)
    print(a.parser())

if __name__ == "__main__":
    main()
      
