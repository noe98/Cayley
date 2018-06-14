"""
Authors: Justin Pusztay
Filename: probability.py
Project: Research for Irina Mazilu, Ph.D.

Contains the Probability class. The class creates a probability function object,
which can have variables with values plugged into them. It also can evaluate an
equation by translating the function to postfix notation and evaluating it there.
"""


__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['evaluator']

from Cayley.parser.scanner import Scanner
from Cayley.parser.translator import Translator
from Cayley.parser.evaluator import Evaluator


def evaluator(function,**kwargs):
    """Plugs in values for the variables and then evaluates the expression."""
    variables = findVariables(function)
    variables.update(kwargs)
    for var in variables:
        function = function.replace(var,str(variables[var]))
    try:
        scanner = Scanner(function)
        translator = Translator(scanner)
        postfix = translator.translate()
        evaluator = Evaluator(postfix)
        return evaluator.evaluate()
    except Exception as e:
        print("Error:", e, translator.translationStatus())

def findVariables(function):
    """Finds the variables in the probability function."""
    variables = dict()
    for char in function:
        if char.lower() in "abcdefghigjklmnopqrstuvwxyz":
            variables[char] = None
    return variables

#Example of how the Probility object can be used
def main():
    a = evaluator("z^y+x",x=1,y=2,z=10)
    print(a)

if __name__ == "__main__":
    main()
      
