# Stochastic Absorption Rates Modeled on Networks
Research by Justin Pusztay, Matt Lubas, and Griffin Noe, for research with Dr. Irina Mazilu at Washington and Lee University.

## Getting Started

The code on Github provides a framework for agent-based modeling on networks. The model follows concepts from statistical physics where particles can attach and de-attach from nodes based on a probability function. The modeling of particle attachment has many different applications from drug encapsulations, thin films interference, voter models, epidemic models, social models, community dynamics and more. This code creates networks and allows for users to run monte carlo simulations on those networks according to various probabilty functions. 

We create an interface for a network and allow implentations to be a Cayley Tree, Lattice, or a build-your-own network. The creation of the Cayley Tree and Lattice are dependent on the demensions requested, the network implentation is automated. 

Cayley Tree (also known as Bethe Lattice) and Lattice are examples of different network structures to represent occupation of nodes (each circle) depending on the status of their neighbors (the circles connected by lines). 
Each Cayley Tree has a specified number of generations and number of connections. The number of generations (starting with 0) is the beginning of the Cayley Tree, and represents the number of connections away from the central node. The connections represent the number of edges each node has (except for the last generation of nodes).

Each Lattice can be represented by a grid that can be written as a length x width x height by counting the number of nodes in that direction. 

![alt text](https://upload.wikimedia.org/wikipedia/commons/e/e7/Reseau_de_Bethe.svg) 

An example of a Cayley Tree marking each generation in color with 3 connections.

### Prerequisites
The entire model and processing is completed on Python3. 
You can download python at the following link:
https://www.python.org/

To run the entire CayleyTree with graphics, excel output, GUI, and monte carlo simulation,the following import packages are needed:

networkx
matplotlib
numpy
random
xlsxwriter
math

To install these packages on Terminal for  Mac OSX/ Linux, or Command Prompt on Windows, copy and paste the following lines:

```
pip install networkx
pip install matplotlib
pip install numpy
pip install xlsxwriter
```

### Installing

To download the Repository, open Terminal/ Command Prompt to the desired location, and run the following line:

```
git clone https://github.com/noe98/Cayley
```
If you are having trouble navigating around Terminal, you can use the following as a resource. https://www.tbi.univie.ac.at/~ronny/Leere/270038/tutorial/node8.html


Once dowloaded, run cayleymain.py or latticemain.py depending on the structure you desire. If you desire to build your own network, please look at graphmain.py to see an example of the implentation of the interface. 

Using this, a TUI will pop, up, and you can decide the number of generations and connections you want for a Cayley Tree, or the dimensions of the lattice graphics. 

By simulating using the variables alpha, beta, and gamma for the following equations, the code can demonstrate the occupation/ emptiness of nodes over large periods of time.

![alt text](https://raw.githubusercontent.com/noe98/Cayley/Photos/nearestneighbors.png)


![alt text](https://raw.githubusercontent.com/noe98/Cayley/Photos/particleattachment.png)


## Built With

* Python 3 [https://www.python.org/]


## Authors

See also the list of [contributors](https://github.com/noe98/Cayley) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

