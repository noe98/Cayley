import Cayley as cy
from makegame import *
import gambit

def main():
    issue = float(input("What is the issue rating? "))
    name1 = input("What is the first senator? ")
    name2 = input("What is the second senator? ")
    agent1 = getRating(name1)
    agent2 = getRating(name2)
    a = float(input("What is 'a' value?  "))
    b = float(input("What is 'b' value?  "))
    c = float(input("What is 'c' value?  "))
    d = float(input("What is 'd' value?  "))
    lyst = list()
    lyst.append(agent1)
    lyst.append(agent2)
    network = cy.Graph()
    senate()
    for x in lyst:
        if issue < 0.5 and x < 0.5:
            print(payoff_matrix1(a,b,c,d,name1,name2))
        elif issue < 0.5 and x > 0.5:
            print(payoff_matrix2(a,b,c,d,name1,name2))
        elif issue > 0.5 and x<0.5:
            print(payoff_matrix3(a,b,c,d,name1,name2))
        elif issue > 0.5 and x >0.5:
            print(payoff_matrix4(a,b,c,d,name1,name2))

if __name__ == "__main__":
    main()

