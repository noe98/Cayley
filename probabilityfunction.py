from scanner import Scanner
from translator import Translator
from evaluator import Evaluator

def probability(function):
    if type(function) != str:
        raise TypeError("Function must inputed as a string")
    return function

def parser(function):
    scanner = Scanner(function)
    translator = Translator(scanner)
    postfix = translator.translate()
    evaluator = Evaluator(postfix)
    return evaluator.evaluate()
        
def main():
    #probability(3))
    print(parser("3*(0.51-2"))

if __name__ == "__main__":
    main()
