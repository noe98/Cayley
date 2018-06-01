"""
Adapted from cayleymain module by Justin Pusztay et al.
Project: Nanoparticle deposition

Hopefully this will run more than one simulation at a time, so that I can
gather data quickly. We'll see what happens.
"""

# N.B. Because I'm lazy, don't run this with parameters that go beyond
# two decimal places. Or if you want to, change how the file name is saved. 

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

timesteps = 25

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
        name = ("NN%dGen_%dLin_%sα_%sβ_%sγ.xlsx" % (generations-1, links, a_tag, b_tag, g_tag))
    elif method == 'TL':
        name = ("TL%dGen_%dLin_%sμ_%sγ.xlsx" % (generations-1, links, m_tag, g_tag))
    elif method == 'EI':
        name = ("EI%dGen_%dLin_%sr1_%sr2_%sγ.xlsx" % (generations-1, links, r1_tag, r2_tag, g_tag))
    else: raise ValueError("Method not recognized")
    workbook = xl.Workbook(name)
    density_list = {}
    other_density_list = {} #key is trial#, index is timestep, gives density
    worksheet4 = workbook.add_worksheet("Over Time")
    worksheet3 = workbook.add_worksheet("Overall")
    
    for j in range(generations+1):
        density_list[j] = []    #First index is generation, 
                                #second is maybe trial number?    
    for i in range(trials):
        other_density_list[i] = [0]*(timesteps+2)
        monte.emptyDictionary()
        monte.list_cache = None
        for j in range(timesteps+1):
            if method == 'NN':
                monte.simulateNN()
            elif method == 'EI':
                monte.simulateEI()
            elif method == 'TL':
                monte.simulateTL(j)
        
        worksheet = workbook.add_worksheet("Data trial %d" % (i))
        worksheet.write(0,0,"Timestep")
        for x in range(total_nodes[generations-1][links]):## #
            worksheet.write(x+1,0,"Node "+str(x))
        for y in range(len(monte.state_d)):
            worksheet.write(0,y+1,str(y))
        for y in range(len(monte.list_cache)):
            for x in range(total_nodes[generations-1][links]):
                worksheet.write(x+1,y+1,monte.list_cache[y][x])

        worksheet2 = workbook.add_worksheet("Density trial %d" % (i))
        worksheet2.write(0,0,"Timestep")
        worksheet2.write(monte.network.generations+1,0,"Total") ## #
        worksheet2.write(monte.network.generations+2,0,"Density") ## #       
        for x in range(monte.network.generations): ## #
            worksheet2.write(x+1,0,"Gen. "+str(x))
        for y in range(timesteps+1):
            worksheet2.write(0,y+1,str(y))
        for y in range(len(monte.list_cache)):
            for x in range(monte.network.generations+1): ## #
                worksheet2.write(x+1,y+1,monte.densityCalculator(x,monte.list_cache[y]))
        for y in range(len(monte.list_cache)):
            sum_t = 0
            for x in range(total_nodes[generations-1][links]): ## #
                sum_t += monte.list_cache[y][x]
            dens_t = sum_t/total_nodes[generations-1][links] ## #
            worksheet2.write(monte.network.generations+1,y+1,sum_t) ## #
            worksheet2.write(monte.network.generations+2,y+1,dens_t) ## #
            ## worksheet4.write(i+2,y+1,dens_t)
            other_density_list[i][y] = dens_t
        
        for k in range(generations+1):
            density_list[k].append(monte.densityCalculator(k,monte.list_cache[len(monte.list_cache)-1]))

##    worksheet3 = workbook.add_worksheet("Overall")
    worksheet3.write(0,0,"Trial")
    for x in range(generations+1):
        worksheet3.write(x+1,0,"Gen. "+str(x))
    for y in range(trials):
        worksheet3.write(0,y+1,"No. "+str(y))
    worksheet3.write(generations+2,0,"Total")
    worksheet3.write(0,trials+1,"Average")
    worksheet3.write(0,trials+2,"Density")
    worksheet3.write(0,trials+3,"Std Dev")
    for x in range(generations+1):
        for y in range(trials):
            worksheet3.write(x+1,y+1,str(density_list[x][y]))
    node_list = []      # Note: it may be a nice idea to rearrange
    for x in range(generations+1):      #node_list, no_nodes, etc. so that
        sum_gen = sum(density_list[x])  #they are calculated early on.
        av = sum_gen/(trials)
        if x == 0:
            no_nodes = 1
        else:
            no_nodes = (monte.network.links*(monte.network.links-1)**(x-1))
        SD = sqrt((av/no_nodes)*(1-av/no_nodes)/(trials*no_nodes))
        worksheet3.write(x+1,trials+1,str(av))
        worksheet3.write(x+1,trials+2,str(av/no_nodes))
        worksheet3.write(x+1,trials+3,str(SD))
        node_list.append(no_nodes)
    all_list = []
    for y in range(trials):
        trial_list = []
        for x in range(generations+1):
            trial_list.append(density_list[x][y])
        trial_sum = sum(trial_list)
        all_list.append(trial_sum)
        tot_av = sum(all_list)/trials
        tot_dens = tot_av/sum(node_list)
        worksheet3.write(generations+2,y+1,str(trial_sum))
    worksheet3.write(generations+2,trials+1,str(tot_av))
    worksheet3.write(generations+2,trials+2,str(tot_dens))
    SD_all = sqrt((tot_dens)*(1-tot_dens)/(trials*sum(node_list)))
    worksheet3.write(generations+2,trials+3,str(SD_all))

    worksheet4.write(0,0,"Timestep")
    worksheet4.write(1,0,"Average")
    #for t in range(trials):
        #worksheet4.write(t+2,0,"Trial "+str(t))
    for k in range(timesteps+1):
        t_sum = 0
        worksheet4.write(0,k+1,k)
        for t in range(trials):
            t_sum += other_density_list[t][k]
        t_av = t_sum/trials
        worksheet4.write(1,k+1,t_av)
    
    workbook.close
        
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
                        simulate('EI',generations, links, alpha, beta, g, rt1, rt2, trials)
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
## Make sure all simulate() calls have correct args
## Finish range functions
## Find issue with EI
