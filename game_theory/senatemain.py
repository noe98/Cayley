import Cayley as cy
import Cayley.game_theory as cg
from Cayley.change_me import timesteps
import csv

def main():
    print("Enter 'Linear', 'Limited', or 'Complete' for model type.")
    model = input('Model: ').lower()
    const = float(input("Input proportionality constant for beta and phi: "))
    if model == 'limited':
        radius = float(input("Radius of connection: "))
    else: radius = 0
    network = cg.Senate(model, const, radius)

    issue = float(input("What is the issue rating? "))
    polarity = issue-0.5
    const = float(input("Input proportionality constant for alpha and gamma: "))
    senate = cy.MonteCarlo(network, 1/(const*abs(polarity)), 0, 1/(const*abs(polarity)))

    print("\n" + "Enter Excel file name \n"
          + "Example: monteCarloData")
    filename = str(input("Filename: "))
    full_filename = filename + ".xlsx"
    senate.senateDictionary(issue)
    for i in range(timesteps):
        senate.simulateVote()
    senate.sendExcel(full_filename)

if __name__ == '__main__':
    main()
