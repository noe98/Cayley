# Stochastic Absorption Rates Modeled on Networks
Research by Justin Pusztay, Matt Lubas, and Griffin Noe, for research with Dr. Irina Mazilu at Washington and Lee University.

## Overview

Cayley provides a framework for agent-based modeling on networks. These models can be from a wide range of disiplines including statistical physics, game theory, or various social sciences. Monte Carlo methods are also provided for any desire to incorporate randomness into the models.

It provides:
* Graph data structures that allows nodes to hold many different types of data, called features.
* General network structures such as cayley tree and lattice.
* Framework for running game theory models on networks.
* Monte Carlo methods to run on networks.

This framework is inspired from the modeling of particle attachment in statistical physics, which has many different applications ranging from drug encapsulations, thin films interference, voter models, epidemic models, social models, and community dynamics.

### Prerequisites
The entire model and processing is completed on Python3. 
You can download python at the following link:
https://www.python.org/

To use this framework the following packages are needed:
```
networkx
matplotlib
numpy
random (Built into Python)
xlsxwriter
math (Built into Python)
```

To install these packages on Terminal for  Mac OSX/ Linux, or Command Prompt on Windows, pip must be installed on your computer (link: https://pip.pypa.io/en/stable/installing/). Once installed, copy and paste the following lines:

```
pip install networkx
pip install matplotlib
pip install numpy
pip install xlsxwriter
```


### Installing

Git must be installed on your computer (link: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

To download the Repository, open Terminal/ Command Prompt to the desired location, and run the following line:

```
git clone https://github.com/noe98/Cayley
```
If you are having trouble navigating around Terminal, you can use the following as a resource. https://www.tbi.univie.ac.at/~ronny/Leere/270038/tutorial/node8.html

### Small Example
```
>>> import Cayley as cy
>>> g = cy.Graph()
>>> names = ["Justin","Joe","Bob","Maria","Helen","Abby"]
>>> for name in names:
         g.add(name)
>>> g.linkCreator("Helen","Justin")
>>> g.linkCreator("Bob","Maria")
>>> g.linkCreator("Helen","Abby")
>>> g.addMultipleNodes(names, hair_color = 'black') #adds a feature
```
## Built With

* Python 3 [https://www.python.org/]


## Authors

See also the list of [contributors](https://github.com/noe98/Cayley) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

