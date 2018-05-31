"""
Adapted from cayleymain module by Justin Pusztay et al.
Project: Nanoparticle deposition

Hopefully this will run more than one simulation at a time, so that I can
gather data quickly. We'll see what happens.
"""

# N.B. Because I'm lazy, don't run this with α, β, or γ values that go beyond
# two decimal place. Or if you want to, change how the file name is saved. 

import Cayley as cy
import Cayley.graphics as cg
import xlsxwriter as xl
import time
from math import sqrt

alpha_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
beta_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
gamma_list = [0.05, 0.1, 0.15, 0.2]


def main(generations, links, alpha, beta, gamma, trials):
    ## The important one
    network = cy.CayleyTree(generations, links)
    monte = cy.MonteCarlo(network, alpha, beta, gamma)
    a_tag = "%.2f" % alpha
    b_tag = "%.2f" % beta
    g_tag = "%.2f" % gamma
    name = ("%dGen_%dLin_%sα_%sβ_%sγ.xlsx" % (generations, links, a_tag, b_tag, g_tag))
    workbook = xl.Workbook(name)
    density_list = {}
    worksheet3 = workbook.add_worksheet("Overall")
    for j in range(generations+1):
        density_list[j] = []    #First index is generation, 
                                #second is maybe trial number?    
    for i in range(trials):
        monte.emptyDictionary()
        monte.list_cache = None
        for j in range(len(monte.network)):
            monte.simulate()
        
        worksheet = workbook.add_worksheet("Data trial %d" % (i))
        worksheet.write(0,0,"Timestep")
        for x in range(len(monte.state_d)):
            worksheet.write(x+1,0,"Node "+str(x))
        for y in range(len(monte.state_d)):
            worksheet.write(0,y+1,str(y))
        for y in range(len(monte.list_cache)):
            for x in range(monte.network.nodeNumber()):
                worksheet.write(x+1,y+1,monte.list_cache[y][x])

        worksheet2 = workbook.add_worksheet("Density trial %d" % (i))
        worksheet2.write(0,0,"Timestep")
        for x in range(monte.network.generations+1):
            worksheet2.write(x+1,0,"Gen. "+str(x))
        for y in range(len(monte.state_d)):
            worksheet2.write(0,y+1,str(y))
        for y in range(len(monte.list_cache)):
            for x in range(monte.network.generations+1):
                worksheet2.write(x+1,y+1,monte.densityCalculator(x,monte.list_cache[y]))

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
    
    workbook.close
        
def monkey():
    ## Just the main method, will run automatically.
    ## Yes, I know that the other one is called main().
    ## Deal with it.
    generations = int(input("Number of generations: "))
    links = int(input("Number of links: "))
    alpha = float(input("Alpha value: "))
    beta = float(input("Beta value: "))
    gamma = float(input("Value for gamma: "))
    trials = int(input("Number of trials: "))
    start_time = time.time()
    main(generations, links, alpha, beta, gamma, trials)
    print("--- %s seconds ---" % (time.time() - start_time))

def alpha_range(generations, links, beta, gamma, trials):
    ## To run tests with a range of alpha values
    for a in alpha_list:
        main(generations, links, a, beta, gamma, trials)

def beta_range(generations, links, alpha, gamma, trials):
    ## To run tests with a range of beta values
    for b in beta_list:
        main(generations, links, alpha, b, gamma, trials)        

def much_data(generations, links, trials):
    start_time = time.time()
    for a in alpha_list:
        for b in beta_list:
            for g in gamma_list:
                main(generations, links, a, b, g, trials)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))
    

if __name__ == "__main__":
    monkey()

    
## Things to look at/fix:
##  Number of nodes per gen (cayleytree)
##  Impossible trees?
