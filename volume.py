#!/usr/bin/env python
"""
Authors: Justin Pusztay, Sho Gibbs, Will Hanstedt
Filename: volume.py
Project: Research for Irina Mazilu, Ph.D.
Adapted from cayleymain.py module by Justin Pusztay et al.

Runs Cayley tree simulations in bulk according to the methods laid out in
montecarlo.py.
"""

import Cayley as cy
import Cayley.graphics as cg
import xlsxwriter as xl
import time
from math import sqrt

total_nodes = [[1,None,None,None,None], #total_nodes[gens][links]
               [None,2,3,4,5],
               [None,None,5,10,17],
               [None,None,7,22,53],
               [None,None,9,46,161],
               [None,None,11,94,485]]

alpha_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
beta_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
gamma_list = [0, 0.05, 0.1, 0.15, 0.2]
mu_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
r1_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
r2_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

timesteps = 50 #change this if you want
node_list = [[0,1],[0,4],[1,6]] #change this if you want


## # <-- indicates adjusted generations (account for last gen fluctuations)

def simulate(method, generations, links, alpha, beta, gamma, mu, r1, r2, trials):
    """The important one"""
    generations = generations + 1 ## #
    network = cy.CayleyTree(generations, links)
    monte = cy.MonteCarlo(network, alpha, beta, gamma, mu, r1, r2)

    a_tag = "%.2f" % alpha
    b_tag = "%.2f" % beta
    g_tag = "%.2f" % gamma
    m_tag = "%.2f" % mu
    r1_tag = "%.2f" % r1
    r2_tag = "%.2f" % r2
    if method == 'NN':
        name = ("NN%dGen_%dLin_%sα_%sβ_%sγ.xlsx" % (generations-1, links,
                                                    a_tag, b_tag, g_tag))
    elif method == 'TL':
        name = ("TL%dGen_%dLin_%sμ_%sγ.xlsx" % (generations-1, links,
                                                m_tag, g_tag))
    elif method == 'EI':
        name = ("EI%dGen_%dLin_%sr1_%sr2_%sγ.xlsx" % (generations-1, links,
                                                      r1_tag, r2_tag, g_tag))
    else: raise ValueError("Method not recognized")
    
    workbook = xl.Workbook(name)
    #JKP: This all can be incorporated with new node feature ability
    density_list = dict() #[trial][timestep] stores overall densities
    state_collect = dict() #[trial] stores final state dictionaries
    dens_collect = dict() #[trial][generation] stores generational densities
    node_d = dict() #[trial#][pair index][node index][timestep] stores node values
    overtime = workbook.add_worksheet("Over Time")
    overall = workbook.add_worksheet("Overall")

    for k in range(trials):
        density_list[k] = [0]*(timesteps+2)

    for k in range(trials):
        dens_collect[k] = [0]*(generations)
       
    for i in range(trials):
        monte.clear()
        monte.emptyDictionary()
        for j in range(timesteps+1):
            if method == 'NN':
                monte.simulateNN()
            elif method == 'EI':
                monte.simulateEI()
            elif method == 'TL':
                monte.simulateTL(j)

        ### FOR RECORDING DATA ###
        #state_collect[i] = monte.sim_data[(len(monte.sim_data)-1)]
        state_collect[i] = monte.simData(monte.getTimesteps()-1) #JKP updated
        #JKP: Follows new encapsulation and defensive programming

        node_d[i] = list()
        for n in range(len(node_list)):
            node_d[i].append([])
            for j in range(len(node_list[n])):
                node_d[i][n].append([])
                for t in range(timesteps):
                    #node_d[i][n][j].append(2*(monte.sim_data[t][node_list[n][j]])-1)
                    node_d[i][n][j].append(2*(monte.simData(t)[node_list[n][j]])-1)
                    #JKP: Follows new updates and defensive programming
        #for y in range(len(monte.sim_data)):
        for y in range(monte.getTimesteps()): #JKP: Follows new updates
            sum_t = 0 # Sum of relevant nodes at one timestep
            for x in range(total_nodes[generations-1][links]): ## # gives adjusted, can't use len(monte.network)
                #sum_t += monte.sim_data[y][x]
                sum_t += monte.simData(y)[x] #JKP: Follows new updates
            dens_t = sum_t/total_nodes[generations-1][links] ## # Density at one timestep
            density_list[i][y] = dens_t

        if trials <= 10: # Trial-by-trial is best for small sets
            worksheet = workbook.add_worksheet("Data trial %d" % (i+1))
            worksheet.write(0,0,"Timestep")
            for x in range(total_nodes[generations-1][links]):## #
                worksheet.write(x+1,0,"Node "+str(x))
            #for y in range(len(monte.sim_data)):
            for y in range(monte.getTimesteps()): #JKP: Follows new updates
                worksheet.write(0,y+1,str(y))
            #for y in range(len(monte.sim_data)):
            for y in range(monte.getTimesteps()): #JKP: Follows new updates
                for x in range(total_nodes[generations-1][links]):
                    #worksheet.write(x+1,y+1,monte.sim_data[y][x])
                    worksheet.write(x+1,y+1,monte.simData(y)[x]) #JKP: Follows new updates

            worksheet2 = workbook.add_worksheet("Density trial %d" % (i+1))
            worksheet2.write(0,0,"Timestep")
            #worksheet2.write(monte.network.generations+1,0,"Density") ## #
            worksheet2.write(network.generations+1,0,"Density") ## #   #JKP: update
            #for x in range(monte.network.generations): ## #
            for x in range(network.generations): ## #  #JKP: follows update
                worksheet2.write(x+1,0,"Gen. "+str(x))
            for y in range(timesteps+1):
                worksheet2.write(0,y+1,str(y))
            #for y in range(len(monte.sim_data)):
            for y in range(monte.getTimesteps()): #JKP: Follows new updates
                #for x in range(monte.network.generations+1): ## # double-check line below
                for x in range(network.generations+1): #JKP: Follows new updates
                    worksheet2.write(x+1,y+1,monte.density(x,monte.simData(y)))
                #worksheet2.write(monte.network.generations+1,y+1,density_list[i][y]) ## #
                worksheet2.write(network.generations+1,y+1,density_list[i][y]) ## #
    corr_t = dict()
    for n in range(len(node_list)):
        corr_t[n] = [0]*timesteps
        for t in range(timesteps):
            sum_prod = 0
            n1 = 0
            n2 = 0
            for i in range(trials):
                sum_prod += (node_d[i][n][0][t])*(node_d[i][n][1][t])
                n1 += node_d[i][n][0][t]
                n2 += node_d[i][n][1][t]
            corr_t[n][t] = (sum_prod/trials)-(n1/trials)*(n2/trials)

    for n in range(len(node_list)):
        corr_sheet = workbook.add_worksheet("Nodes %d+%d" %(node_list[n][0],
                                                            node_list[n][1]))
        corr_sheet.write(0,0,"Timestep")
        corr_sheet.write(1,0,"Correlation")
        for t in range(timesteps):
            corr_sheet.write(0,t+1,t)
            corr_sheet.write(1,t+1,corr_t[n][t])


    ### FOR RECORDING OVERALL DATA ###
    overall.write(0,0,"Generation") # For steady-state analysis
    for x in range(generations):
        overall.write(x+1,0,"Gen. "+str(x))
    overall.write(0,1,"Average")
    overall.write(0,2,"Std Dev")

    for x in range(generations):
        if x == 0:
            for y in range(trials):
                dens_collect[y][x] = monte.density(x,state_collect[y])
        else:
            for y in range(trials):
                dens_collect[y][x] = monte.density(x,state_collect[y])/ \
                                     ((links)*(links-1)**(x-1))
    
    if trials <= 10: # Densities per gen for individual trials
        for y in range(trials):
            overall.write(0,y+4,"Trial "+str(y+1))
            overall.write(generations+1,y+4,density_list[y][timesteps])
        for x in range(generations):
            for y in range(trials):
                overall.write(x+1,y+4,dens_collect[y][x])

    for x in range(generations): # Average density per generation
        list_gen = [] # Temporary variable
        for y in range(trials):
            list_gen.append(dens_collect[y][x])
        av = sum(list_gen)/(trials)
        SD = sqrt((av)*(1-av)/total_nodes[generations-1][links])
        overall.write(x+1,1,str(av))
        overall.write(x+1,2,str(SD))

    overall.write(generations+1,0,"Total")
    tot_sum = 0
    for c in range(trials):
        tot_sum += density_list[c][timesteps]
    tot_av = tot_sum/trials
    SD_all = sqrt((tot_av)*(1-tot_av)/(trials*total_nodes[generations-1][links]))
    overall.write(generations+1,1,tot_av)
    overall.write(generations+1,2,SD_all)

    # Average density over time
    overtime.write(0,0,"Timestep")
    overtime.write(1,0,"Average")
    if trials <= 10:
        for t in range(trials):
            overtime.write(t+3,0,"Trial "+str(t+1))
            for k in range(timesteps+1):
                overtime.write(t+3,k+1,density_list[t][k])
    else: overtime.write(3,0,"Trials: "+str(trials))
    for k in range(timesteps+1):
        t_sum = 0
        overtime.write(0,k+1,k)
        for t in range(trials):
            t_sum += density_list[t][k]
        t_av = t_sum/trials
        overtime.write(1,k+1,t_av)
    
    workbook.close #JKP: Are you missiong a paranthesis?
        
def main():
    print("Enter 'NN', 'TL', 'EI' for nearest neighbors, total lattice " + \
          "density, or empty interval methods.")
    method = input("Method: ").upper()
    generations = int(input("Number of generations: "))
    links = int(input("Number of links: "))
    trials = int(input("Number of trials: "))
    if method == 'NN':
        alpha = float(input("Alpha value: "))
        beta = float(input("Beta value: "))
        gamma = float(input("Value for gamma: "))
        mu = r1 = r2 = 0
    elif method == 'TL':
        mu = float(input("Mu value: "))
        gamma = float(input("Value for gamma: "))
        alpha = beta = r1 = r2 = 0
    elif method == 'EI':
        print("R1 should be less than R2 for electrostatic models.")
        r1 = float(input("R1 value: "))
        r2 = float(input("R2 value: "))
        gamma = float(input("Value for gamma: "))
        alpha = beta = mu = 0
    else: raise ValueError("Method not recognized")
    start_time = time.time()
    simulate(method, generations, links, alpha, beta, gamma, mu, r1, r2, trials)
    print("--- %s seconds ---" % (time.time() - start_time))

def alpha_range(generations, links, beta, gamma, trials):
    """To run tests with a range of alpha values"""
    for a in alpha_list:
        simulate('NN', generations, links, a, beta, gamma, 0, 0, 0, trials)

def beta_range(generations, links, alpha, gamma, trials):
    """To run tests with a range of beta values"""
    for b in beta_list:
        simulate('NN', generations, links, alpha, b, gamma, 0, 0, 0, trials)        

def mu_range(generations, links, gamma, trials):
    """To run tests with a range of mu values"""
    for m in mu_list:
        simulate('TL', generations, links, 0, 0, gamma, m, 0, 0, trials)

def r1_range(generations, links, r2, gamma, trials):
    """To run tests with a range of r1 values"""
    for rt1 in r1_list:
        simulate('EI', generations, links, 0, 0, gamma, 0, rt1, r2, trials)

def r2_range(generations, links, r1, gamma, trials):
    """To run tests with a range of r2 values"""
    for rt2 in r2_list:
        simulate('EI', generations, links, 0, 0, gamma, 0, r1, rt2, trials)

def full(method, generations, links, trials):
    """You'll have data coming out of your ears"""
    start_time = time.time()
    if method == 'NN':
        mu = r1 = r2 = 0
        for a in alpha_list:
            for b in beta_list:
                for g in gamma_list:
                    simulate('NN', generations, links, a, b, g, mu, r1, r2, trials)
    elif method == 'EI':
        alpha = beta = mu = 0
        for rt1 in r1_list:
            for rt2 in r2_list:
                for g in gamma_list:
                    if rt2 >= rt1:
                        simulate('EI',generations, links, alpha, beta, g,
                                 rt1, rt2, trials)
    elif method == 'TL':
        alpha = beta = r1 = r2 = 0
        for m in mu_list:
            for g in gamma_list:
                simulate('TL', generations, links, alpha, beta, g, m, r1, r2, trials)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

def no_evaporation(method, generations, links, trials):
    """You'll have slightly unrealistic data coming out of your ears"""
    start_time = time.time()
    if method == 'NN':
        mu = r1 = r2 = 0
        for a in alpha_list:
            for b in beta_list:
                simulate('NN', generations, links, a, b, 0, mu, r1, r2, trials)
    elif method == 'EI':
        alpha = beta = mu = 0
        for rt1 in r1_list:
            for rt2 in r2_list:
                if rt2 >= rt1:
                    simulate('EI',generations, links, alpha, beta, 0, mu, rt1, rt2, trials)
    elif method == 'TL':
        alpha = beta = r1 = r2 = 0
        for m in mu_list:
            simulate('TL', generations, links, alpha, beta, 0, m, r1, r2, trials)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))
    
def timestep(number_of_timesteps):
    timesteps = number_of_timesteps

if __name__ == "__main__":
    main()

    
## Things to look at/fix:
## Clean up formatting
## Make this able to call the lattice class
## Different initial states
