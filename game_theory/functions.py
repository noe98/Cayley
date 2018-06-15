"""
Filename: functions.py

Provides key functions to setting up a game between senators.
"""

import csv
import Cayley as cy
import numpy as np
import random

#For personal reference when using the CSV
name_of_data_from_csv = ['rank_from_low', 'rank_from_high',
                         'percentile', 'ideology', 'id',
                         'bioguide_id', 'state', 'district', 'name']

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['senate','payoff_matrix1','payoff_matrix2','payoff_matrix3',
           'payoff_matrix4','randomStart','game']

def senate(network,csv_name = 'senatedata.csv'):
    """
    Takes a network and adds each senator to it. It puts their last name
    as the name of the node. Adds ideological score and state as features.

    Notes
    -----
    -> An empty graph network object is best recommended for this function. Since
       it is empty, this function will populate it with senators as nodes.
    -> The idelogical score for all senators are from
       https://www.govtrack.us/congress/members/report-cards/2017/senate/ideology
       These scores are added as a feature to each seantor node.
    -> The state the senator is from is also a feature of the node.
    -> This function takes an existing network, with whatever nodes it has
       and adds a senator to it.
    -> You can create a network with other nodes and the senate to it.
    -> This function currently adds no connections to the nodes.
    -> Name of features:
         'ideology'
         'state'

    Parameters
    ----------
    network: Cayley network object
       A graph object (prefered) or lattice or cayley tree.

    csv_name: str default='senatedata.csv'
       CSV file that stores the data of the senate. A copy can be obtained at the
       following link: 
       https://www.govtrack.us/congress/members/report-cards/2017/senate/ideology
       It must be stored in same folder as this code.
       
    Examples
    --------
    >>> import Cayley as cy
    >>> import Cayley.game_theory as cgt
    >>> g = cy.Graph()
    >>> cgt.senate(g)
    """
    with open(csv_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[8] != 'name':
                network.add(row[8],ideology = row[3],state = row[6])

def payoff_matrix1(network,a,b,c,d,agent1,agent2):
    """
    Calculates the payoff matrix when the issue value is less than 0.5 and
    the main agent playing the game has an idealogical score of less than 0.5.

    Parameters
    ----------
    network: Cayley network object
       A graph object (prefered) or lattice or cayley tree.
    a: float
       This is a constant that goes into calculating the values in the matrix.
    b: float
       This is a constant that goes into calculating the values in the matrix.
    c: float
       This is a constant that goes into calculating the values in the matrix.
    d: float
       This is a constant that goes into calculating the values in the matrix.
    agent1: str
       A string that contains the exact last name of the senator that appears
       in the network must be used. Proper capitalization must be used.
    agent2: str
       A string that contains the exact last name of the senator that appears
       in the network must be used. Proper capitalization must be used.
       
    Notes
    -----
    -> The agent listed first will be the vertical strategy. If this is not correct,
       the results will not be as intended!
    -> Agent listed second will be the horizontal strategy.
    -> The numpy package needs to be installed in order for function to work.
    -> The matrix returned is a numpy matrix object. This allows us to use their
       interface to do many linear algebra operations as well as array operations. 
    -> Conditions of issue rating and agent idealogial score must be checked
       before the funciton is executed.

    Returns
    -------
    A numpy matrix

    Raises
    ------
    KeyError:
       When the ideology feature was not added to the entire network.

    Examples
    --------
    >>> import Cayley as cy
    >>> import Cayley.game_theory as cgt
    >>> g = cy.Graph()
    >>> cgt.senate(g)
    >>> cgt.payoff_matrix1(0.5,1.2,3.3,1.0,"Cruz","Sanders")
    """
    try:
        a1 = float(network.getNodeFeature('ideology')[agent1])
        a2 = float(network.getNodeFeature('ideology')[agent2])
        matrix1 = np.matrix([[a*abs(a1-a2),b*abs(a1-a2)],
                             [c*abs(a1-a2),d*abs(a1-a2)]],dtype = float)
        return matrix1
    except KeyError:
        return "Ideology feature not added to the entire network."
    
def payoff_matrix2(network,a,b,c,d,agent1,agent2):
    """
    Calculates the payoff matrix when the issue value is less than 0.5 and
    the main agent playing the game has an idealogical score of greater than 0.5.

    Parameters
    ----------
    network: Cayley network object
       A graph object (prefered) or lattice or cayley tree.
    a: float
       This is a constant that goes into calculating the values in the matrix.
    b: float
       This is a constant that goes into calculating the values in the matrix.
    c: float
       This is a constant that goes into calculating the values in the matrix.
    d: float
       This is a constant that goes into calculating the values in the matrix.
    agent1: str
       A string that contains the exact last name of the senator that appears
       in the network must be used. Proper capitalization must be used.
    agent2: str
       A string that contains the exact last name of the senator that appears
       in the network muyst be used. Proper capitalization must be used.
       
    Notes
    -----
    -> The agent listed first will be the vertical strategy. If this is not correct,
       the results will not be correct!
    -> Agent listed second will be the horizontal strategy.
    -> The numpy package needs to be installed in order for function to work.
    -> The matrix returned is a numpy matrix object. This allows us to use their
       interface to do many linear algebra operations as well as array operations.
    -> Conditions of issue rating and agent idealogial score must be checked
       before the funciton is executed.

    Returns
    -------
    A numpy matrix

    Raises
    ------
    KeyError:
       When the ideology feature was not added to the entire network.

    Examples
    --------
    >>> import Cayley as cy
    >>> import Cayley.game_theory as cgt
    >>> g = cy.Graph()
    >>> cgt.senate(g)
    >>> cgt.payoff_matrix2(0.5,1.2,3.3,1.0,"Cruz","Sanders")
    """
    try:
        a1 = float(network.getNodeFeature('ideology')[agent1])
        a2 = float(network.getNodeFeature('ideology')[agent2])
        matrix2 = np.matrix([[d*abs(a1-a2),c*abs(a1-a2)],
                             [b*abs(a1-a2),a*abs(a1-a2)]],dtype = float)
        return matrix2
    except KeyError:
        return "Ideology feature not added to the entire network."
    
def payoff_matrix3(network,a,b,c,d,agent1,agent2):
    """
    Calculates the payoff matrix when the issue value is greater than 0.5 and
    the main agent playing the game has an idealogical score of less than 0.5.

    Parameters
    ----------
    network: Cayley network object
       A graph object (prefered) or lattice or cayley tree.
    a: float
       This is a constant that goes into calculating the values in the matrix.
    b: float
       This is a constant that goes into calculating the values in the matrix.
    c: float
       This is a constant that goes into calculating the values in the matrix.
    d: float
       This is a constant that goes into calculating the values in the matrix.
    agent1: str
       A string that contains the exact last name of the senator that appears
       in the network must be used. Proper capitalization must be used.
    agent2: str
       A string that contains the exact last name of the senator that appears
       in the network must be used. Proper capitalization must be used.
       
    Notes
    -----
    -> The agent listed first will be the vertical strategy. If this is not correct,
       the results will not be correct!
    -> Agent listed second will be the horizontal strategy.
    -> The numpy package needs to be installed in order for function to work.
    -> The matrix returned is a numpy matrix object. This allows us to use their
       interface to do many linear algebra operations as well as array operations. 
    -> Conditions of issue rating and agent idealogial score must be checked
       before the funciton is executed.

    Returns
    -------
    A numpy matrix

    Raises
    ------
    KeyError:
       When the ideology feature was not added to the entire network.

    Examples
    --------
    >>> import Cayley as cy
    >>> import Cayley.game_theory as cgt
    >>> g = cy.Graph()
    >>> cgt.senate(g)
    >>> cgt.payoff_matrix3(0.5,1.2,3.3,1.0,"Cruz","Sanders")
    """
    try:
        a1 = float(network.getNodeFeature('ideology')[agent1])
        a2 = float(network.getNodeFeature('ideology')[agent2])
        matrix3 = np.matrix([[d*abs(a1-a2),c*abs(a1-a2)],
                             [b*abs(a1-a2),a*abs(a1-a2)]],dtype = float)
        return matrix3
    except KeyError:
        return "Ideology feature not added to the entire network."

def payoff_matrix4(network,a,b,c,d,agent1,agent2):
    """
    Calculates the payoff matrix when the issue value is greater than 0.5 and
    the main agent playing the game has an idealogical score of greater than 0.5.

    Parameters
    ----------
    network: Cayley network object
       A graph object (prefered) or lattice or cayley tree.
    a: float
       This is a constant that goes into calculating the values in the matrix.
    b: float
       This is a constant that goes into calculating the values in the matrix.
    c: float
       This is a constant that goes into calculating the values in the matrix.
    d: float
       This is a constant that goes into calculating the values in the matrix.
    agent1: str
       A string that contains the exact last name of the senator that appears
       in the network must be used. Proper capitalization must be used.
    agent2: str
       A string that contains the exact last name of the senator that appears
       in the network must be used. Proper capitalization must be used.
       
    Notes
    -----
    -> The agent listed first will be the vertical strategy. If this is not correct,
       the results will not be correct!
    -> Agent listed second will be the horizontal strategy.
    -> The numpy package needs to be installed in order for function to work.
    -> The matrix returned is a numpy matrix object. This allows us to use their
       interface to do many linear algebra operations as well as array operations.
    -> Conditions of issue rating and agent idealogial score must be checked
       before the funciton is executed.

    Returns
    -------
    A numpy matrix

    Raises
    ------
    KeyError:
       When the ideology feature was not added to the entire network.

    Examples
    --------
    >>> import Cayley as cy
    >>> import Cayley.game_theory as cgt
    >>> g = cy.Graph()
    >>> cgt.senate(g)
    >>> cgt.payoff_matrix4(0.5,1.2,3.3,1.0,"Cruz","Sanders")
    """
    try:
        a1 = float(network.getNodeFeature('ideology')[agent1])
        a2 = float(network.getNodeFeature('ideology')[agent2])
        matrix4 = np.matrix([[a*abs(a1-a2),b*abs(a1-a2)],
                             [c*abs(a1-a2),d*abs(a1-a2)]],dtype = float)
        return matrix4
    except KeyError:
        return "Ideology feature not added to the entire network."

def randomStart(network):
    """
    Randomly chooses the strategy of the agent. A zero will represent no
    and a one will represent yes. Will add the strategy as a feature to
    each senator node.

    Notes
    -----
    -> The name of the feature is 'strategy'

    Parameters
    ----------
    network: Cayley network object
       A graph object (prefered) or lattice or cayley tree.

    Examples
    --------
    >>> import Cayley as cy
    >>> import Cayley.game_theory as cgt
    >>> g = cy.Graph()
    >>> senate(g)
    >>> cgt.randomStart(g)
    """
    for node in network:
        network.add(node, strategy = random.randint(0,1))

def game(network,payoff_matrix,agent1,agent2):
    """
    Plays a game between agents. Agent 1 is playing the vertical strategy and agent
    2 is playing the horizontal strategy. The function adds the real reward
    and the imagined reward as features to the senator node that is agent 1.

    Parameters
    ----------
    network: Cayley network object
       A graph object (prefered) or lattice or cayley tree.
    payoff_matrix: numpy matrix object
       A numpy matrix must be used otherwise the code will not run!
    agent1: str
       Name of agent 1 as it appears in the network.
    agent2: str
       Name of agent 2 as it appears in the network.

    Returns
    -------
    Tuple with the real reward of agent 1 as the first element and the imagined
    reward as the second element. Both are floats.

    Raises
    ------
    KeyError:
       Raises when a strategy feature has not been assigned to the entire network.

    Notes
    -----
    -> The payoff matrix must be determined before with the conditions of the
       issue value and agent 1 ideological value. But it will take any matrix.
    -> The agent listed first will be the vertical strategy. If this is not correct,
       the results will not be correct!
    -> Agent listed second will be the horizontal strategy.
    -> The agents listed in the function arguemnts do effect calculations,
       since the real and imagined rewards are only added to the agent1 argument.
    -> The real reward and imagined rewards are added as features to the senator
       nodes, listed as agent1, under the names:
            'real_reward'
            'imagined_reward'

    Examples
    --------
    >>> import Cayley as cy
    >>> import Cayley.game_theory as cgt
    >>> g = cy.Graph()
    >>> cgt.senate(g)
    >>> matrix = cgt.payoff_matrix4(0.5,1.2,3.3,1.0,"Cruz","Sanders")
    >>> game(matrix,"Cruz","Sanders")
    """
    try:
        strategy_d = network.getNodeFeature('strategy')
        agent1_strategy = strategy_d[agent1]
        agent2_strategy = strategy_d[agent2]
        real_payoff = payoff_matrix[1-agent2_strategy,1-agent1_strategy]
        network.add(agent1,real_reward = real_payoff)
        imagined_payoff = payoff_matrix[1-agent2_strategy,agent1_strategy]
        network.add(agent1,imagined_reward = imagined_payoff)
        return (real_payoff,imagined_payoff)
    except KeyError:
        return "Strategy feature is not built into entire network"


