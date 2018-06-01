"""
Adapted from cayleymain module by Justin Pusztay et al.
Project: Nanoparticle deposition

Hopefully this will run more than one simulation at a time, so that I can
gather data quickly. We'll see what happens.
"""
#WILL NOT RUN#JUST TO KEEP CODE
import Cayley as cy
import Cayley.graphics as cg
import xlsxwriter as xl
import time
from math import sqrt

alpha_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
beta_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
gamma_list = [0.0, 0.05, 0.1, 0.15, 0.2]


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

        
        worksheet2 = workbook.add_worksheet("Den %d" % (i))#sho
        worksheet2.write(0,0,"Timestep")
        worksheet2.write(monte.network.generations+2,0,"total")#sho
        worksheet2.write(monte.network.generations+3,0,"density")#sho
        f=1#sho
        for x in range(1,monte.network.generations+1):#sho
            f= f+ monte.network.links*(monte.network.links-1)**(x-1)#sho
        for x in range(monte.network.generations+1):
            worksheet2.write(x+1,0,"Gen. "+str(x))
        for y in range(len(monte.state_d)):
            worksheet2.write(0,y+1,str(y))
        for y in range(len(monte.list_cache)):
            w=0#sho
            for x in range(monte.network.generations+1):
                worksheet2.write(x+1,y+1,monte.densityCalculator(x,monte.list_cache[y]))
                w = w+monte.densityCalculator(x,monte.list_cache[y])#sho
            worksheet2.write(monte.network.generations+2,y+1,w)#sho
            worksheet2.write(monte.network.generations+3,y+1,w/f)#sho

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
#deleted stuff I dont touch
