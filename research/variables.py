"""
@author: Justin Pusztay
Filename: variables.py
Project: Research for Irina Mazilu, Ph.D.

Contains the Variables class. Holds the most common data values for
running simulations on graphs. Gives the ability to create data and then
to change the values for the data within the object. 
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['Variables','total_node_matrix']

import numpy as np


def sizeCayley(gen,edges):
    """
    Returns the number of nodes in a Cayley Tree. 
    """
    size = 1
    for x in range(1,gen+1):
        size += (edges * (edges - 1)**(x - 1))
    return size

def total_node_matrix(m,n):
    """
    The rows in this matrix represent the generations, the columns represent
    the number of edges in Cayley Tree.

    To retrieve the number of nodes in a specific Cayley Tree, index as you
    would a numpy array. 
    """
    matrix = np.zeros((m+1,n+1))
    for row in range(m+1):
        for column in range(n+1):
            matrix[row,column] = sizeCayley(row,column)
    return matrix
           
class Variables(object):
    """
    Creates a variable object that will store the variable values
    for the simulation.
    """

    def __init__(self):
        """
        Creates all of the variables that are set to their most common values.
        To retrive variable names call a method on the variables object, that
        shares the name of the variable you want.

        Also there are set methods to change the variable. 
        """
        self.__timesteps = 50
        self.__nodeList = [(0,1),(1,2),(2,3),(21,106)]
        self.__initialState = "empty"
        self.__alpha_list = np.arange(0.0, 1.1, 0.1)
        self.__beta_list = self.__alpha_list
        self.__mu_list = self.__alpha_list
        self.__gamma_list = np.arange(0.0,0.25,0.05)
        self.__r1_list = self.__alpha_list
        self.__r2_list = self.__alpha_list
        self.__a_d_lists = list(range(0,11))
        self.__issue_list = np.arange(0.4,0.8,0.2)
        self.__temp_d = {0: 0.01, 1: 0.02}
        self.__senate_corr = ["Franken Sanders","Sanders Merkley"]
        self.__radius_of_connection = 0.07

    # Methods that allow access of data
    def timesteps(self):
        return self.__timesteps

    def nodeList(self):
        return self.__nodeList

    def initialState(self):
        return self.__initialState

    def alphaList(self):
        return self.__alpha_list

    def betaList(self):
        return self.__beta_list

    def muList(self):
        return self.__mu_list

    def gammaList(self):
        return self.__gamma_list

    def r1List(self):
        return self.__r1_list

    def r2List(self):
        return self.__r2_list

    def aList(self):
        return self.__a_d_lists

    def bList(self):
        return self.__a_d_lists

    def cList(self):
        return self.__a_d_lists

    def dList(self):
        return self.__a_d_lists

    def issueList(self):
        return self.__issue_list

    def tempD(self):
        return self.__temp_d

    def senateCorr(self):
        return self.__senate_corr

    def radiusConnection(self):
        return self.__radius_of_connection

    # Methods to change data for each variable.
    def setTimesteps(self, timesteps):
        self.__timesteps = timesteps

    def setNodeList(self, nodeList):
        self.__nodeList = nodeList

    def setInitialState(self,initialState):
        self.__initialState = initialState

    def setAlphaList(self,alphaList):
        self.__alpha_list = alphaList

    def setBetaList(self,betaList):
        self.__beta_list = betaList

    def setMuList(self,muList):
        self.__mu_list = muList

    def setGammaList(self,gammaList):
        self.__gamma_list = gammaList

    def setr1List(self, r1List):
        self.__r1_list = r1List

    def setr2List(self, r2List):
        self.__r2_list = r2List

    def setaList(self,aList):
        self.__a_d_lists = aList

    def setIssueList(self,IssueList):
        self.__issue_list = IssueList

    def setTempD(self,tempd):
        self.__temp_d=  tempd

    def setSenateCorr(self,senate):
        self.__senate_corr = senate

    def setRadiusConnection(self,radius):
        self.__radius_of_connection = radius

    
    
