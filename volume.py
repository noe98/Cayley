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
from change_me import timesteps
from change_me import node_list
from change_me import initial_state
from change_me import total_nodes
from change_me import temp_d

## # <-- indicates adjusted generations (account for last gen fluctuations)

def simulate(method, generations, links, alpha, beta, gamma, mu, r1, r2,
             trials,k,J):
    """The important one"""
    generations = generations + 1 ## #
    network = cy.CayleyTree(generations, links)
    monte = cy.MonteCarlo(network, alpha, beta, gamma, mu, r1, r2)
    run_time = time.time()
    endcol = xl.utility.xl_col_to_name(timesteps+1)

    a_tag = "%.2f" % alpha
    b_tag = "%.2f" % beta
    g_tag = "%.2f" % gamma
    m_tag = "%.2f" % mu
    r1_tag = "%.2f" % r1
    r2_tag = "%.2f" % r2
    if method == 'NN':
        name = ("NN%dGen_%dLin_%sα_%sβ_%sγ.xlsx" % (generations-1, links,
                                                    a_tag, b_tag, g_tag))
        tags = a_tag+'-'+b_tag+'-'+g_tag
    elif method == 'TL':
        name = ("TL%dGen_%dLin_%sμ_%sγ.xlsx" % (generations-1, links,
                                                m_tag, g_tag))
        tags = m_tag+'-'+g_tag
    elif method == 'EI':
        name = ("EI%dGen_%dLin_%sr1_%sr2_%sγ.xlsx" % (generations-1, links,
                                                      r1_tag, r2_tag, g_tag))
        tags = r1_tag+'-'+r2_tag+'-'+g_tag
    elif method == 'TM':
        tag_list = ()
        for s in range(len(temp_d)):
            tag_list += ("%.2f"%temp_d[s],)
        tags = ("%s_"*(len(temp_d)-1)+"%s") %tag_list
        name = ("TM%dGen_%dLin_"%(generations-1,links)+tags+".xlsx")
    else: raise ValueError("Method not recognized")
    print("\n#### RUNNING SIMULATION %s ####\n"%(name))

    workbook = xl.Workbook(name)
    #JKP: This all can be incorporated with new node feature ability
    density_list = dict() #[trial][timestep] stores overall densities
    state_collect = dict() #[trial] stores final state dictionaries
    dens_collect = dict() #[trial][generation] stores generational densities
    node_d = dict() #[trial#][pair index][node index][timestep] stores node values
    overtime = workbook.add_worksheet("Over_Time")
    overall = workbook.add_worksheet("Overall")

    for m in range(trials):
        density_list[m] = [0]*(timesteps+2)

    for m in range(trials):
        dens_collect[m] = [0]*(generations)

    for i in range(trials):
        monte.clear()
        if method == 'TM': monte.randomSpins()
        else:
            if initial_state == "empty": monte.emptyDictionary()
            elif initial_state == "random": monte.randomDictionary()
            elif initial_state == "zero": monte.zeroDictionary()

        if method == 'TM':
            iterate = len(temp_d)
            for d in range (generations+1):
                temp = temp_d[d%iterate]
                network.addMultipleNodes(network.nodesPerGen(d),temperature=temp)

        for t in range(timesteps+1):
            if method == 'NN':
                monte.simulateNN()
            elif method == 'EI':
                monte.simulateEI()
            elif method == 'TL':
                monte.simulateTL(t)
            elif method == 'TM':
                monte.simulateTemp(k,J)

        ### FOR RECORDING DATA ###
        state_collect[i] = monte.simData(monte.getTimesteps()-1) #JKP updated

        node_d[i] = list()
        for n in range(len(node_list)):
            node_d[i].append([])
            for f in range(len(node_list[n])):
                node_d[i][n].append([])
                for t in range(timesteps+1):
                    if method == 'TM':
                        node_d[i][n][f].append((monte.simData(t)[node_list[n][f]]))
                    else:
                        node_d[i][n][f].append(2*(monte.simData(t)[node_list[n][f]])-1)

        for y in range(monte.getTimesteps()): #JKP: Follows new updates
            sum_t = 0 # Sum of relevant nodes at one timestep
            for x in range(total_nodes[generations-1][links]): ## # gives adjusted, can't use len(monte.network)
                sum_t += monte.simData(y)[x] #JKP: Follows new updates
            dens_t = sum_t/total_nodes[generations-1][links] ## # Density at one timestep
            density_list[i][y] = dens_t

        if trials <= 10: # Trial-by-trial is best for small sets
            worksheet = workbook.add_worksheet("Data trial %d" % (i+1))
            worksheet.write(0,0,"Timestep")
            for x in range(total_nodes[generations-1][links]):## #
                worksheet.write(x+1,0,"Node "+str(x))
            for y in range(monte.getTimesteps()): #JKP: Follows new updates
                worksheet.write(0,y+1,str(y))
            for y in range(monte.getTimesteps()): #JKP: Follows new updates
                for x in range(total_nodes[generations-1][links]):
                    worksheet.write(x+1,y+1,monte.simData(y)[x]) #JKP: Follows new updates

            worksheet2 = workbook.add_worksheet("Density trial %d" % (i+1))
            worksheet2.write(0,0,"Timestep")
            worksheet2.write(network.generations+1,0,"Density") ## #   #JKP: update
            for x in range(network.generations): ## #  #JKP: follows update
                worksheet2.write(x+1,0,"Gen. "+str(x))
            for y in range(timesteps+1):
                worksheet2.write(0,y+1,str(y))
            for y in range(monte.getTimesteps()): #JKP: Follows new updates
                for x in range(network.generations+1): #JKP: Follows new updates
                    worksheet2.write(x+1,y+1,monte.density(x,monte.simData(y)))
                worksheet2.write(network.generations+1,y+1,density_list[i][y]) ## #

        if (trials >= 100) and ((10*i)%trials == 0):
            try:
                ti = (time.time()-run_time)
                print("Trial: "+str(i))
                print(str(ti)+" secs")
            except NameError: pass

    corr_t = dict()
    for n in range(len(node_list)):
        corr_t[n] = [0]*(timesteps+1)
        for t in range(timesteps+1):
            sum_prod = 0
            n1 = 0
            n2 = 0
            for i in range(trials):
                sum_prod += (node_d[i][n][0][t])*(node_d[i][n][1][t])
                n1 += node_d[i][n][0][t]
                n2 += node_d[i][n][1][t]
            corr_t[n][t] = (sum_prod/trials)-(n1/trials)*(n2/trials)

    for n in range(len(node_list)): # For recording correlations
        sheetname = ("Nodes_%d+%d" %(node_list[n][0],node_list[n][1]))
        chartrange = '='+sheetname+'!$B$2:$'+endcol+'$2'
        timerange = '='+sheetname+'!$B$2:$'+endcol+'$2'
        corr_sheet = workbook.add_worksheet(sheetname)
        corr_sheet.write(0,0,"Timestep")
        corr_sheet.write(1,0,"Correlation")
        corr_chart = workbook.add_chart({'type':'line'})
        corr_sheet.insert_chart('I8', corr_chart)
        corr_chart.set_title({'name':'Correlation'})
        corr_chart.set_x_axis({'name':'Timesteps'})
        corr_chart.set_y_axis({'name':'Correlation'})
        corr_chart.add_series({'values':chartrange,
                               'name':'Correlation'})
        for t in range(timesteps+1):
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
        if method == 'TM':
            av = (av+1)/2
        SD = sqrt((av)*(1-av)/total_nodes[generations-1][links])
        if method == 'TM':
            SD *= 2
        overall.write(x+1,1,str(av))
        overall.write(x+1,2,str(SD))

    overall.write(generations+1,0,"Total")
    tot_sum = 0
    for c in range(trials):
        tot_sum += density_list[c][timesteps]
    tot_av = tot_sum/trials
    if method == 'TM':
        tot_av = (tot_av+1)/2
    SD_all = sqrt((tot_av)*(1-tot_av)/(trials*total_nodes[generations-1][links]))
    if method == 'TM':
        SD_all *= 2
    overall.write(generations+1,1,tot_av)
    overall.write(generations+1,2,SD_all)

    # Average density over time
    overtime.write(0,0,"Timestep")
    data_tag = method+" "+str(generations)+" "+str(links)+" "+tags
    overtime.write(1,0,data_tag)
    chartrange = '=Over_Time!$B$2:$'+endcol+'$2'
    over_chart = workbook.add_chart({'type':'line'})
    overtime.insert_chart('I8',over_chart)
    over_chart.set_title({'name':'Density'})
    over_chart.set_x_axis({'name':'Timesteps'})
    over_chart.set_y_axis({'name':'Density'})
    over_chart.add_series({'values':('=Over_Time!$B$2:$'+endcol+'$2'),
                           'name':'=Over_Time!$A$2'})
    over_chart.add_series({'values':('=Over_Time!$B$3:$'+endcol+'$3'),
                           'name':'=Over_Time!$A$3'})
    over_chart.add_series({'values':('=Over_Time!$B$4:$'+endcol+'$4'),
                           'name':'=Over_Time!$A$4'})
    if trials <= 10:
        for t in range(trials):
            overtime.write(t+3,0,"Trial "+str(t+1))
            for m in range(timesteps+1):
                overtime.write(t+3,m+1,density_list[t][m])
        if method == 'TM':
            overtime.write(6,1,"k: "%(k))
            overtime.write(6,2,"J: "%(J))
            for i in range(generations+1):
                overtime.write(i+6+trials,0,"Generation: "+str(i))
                overtime.write(i+6+trials,1,str(temp_d[i]))
    else:
        overtime.write(6,0,"Trials: "+str(trials))
        if method == 'TM':
            overtime.write(6,1,"k: "+str(k))
            overtime.write(6,2,"J: "+str(J))
            overtime.write(8,0,"Temperatures")
            for i in range(generations+1):
                overtime.write(i+9,0,"Gen: "+str(i))
                overtime.write(i+9,1,str(temp_d[i%len(temp_d)]))
    for m in range(timesteps+1):
        t_sum = 0
        overtime.write(0,m+1,m)
        for t in range(trials):
            t_sum += density_list[t][m]
        t_av = t_sum/trials
        overtime.write(1,m+1,t_av)

    workbook.close()

def main():
    print("To change the default timesteps, initial state, temperatures, or"+\
          " nodes for comparison, change the values in the change_me.py file.")
    print("Enter 'NN', 'TL', 'EI', or 'TM' for nearest neighbors, total " +
          "lattice density, empty interval, or temperature methods.")
    method = input("Method: ").upper()
    generations = int(input("Number of generations: "))
    links = int(input("Number of links: "))
    trials = int(input("Number of trials: "))
    if method == 'NN':
        alpha = float(input("Alpha value: "))
        beta = float(input("Beta value: "))
        gamma = float(input("Value for gamma: "))
        mu = r1 = r2 = 0
        k_c = J_c = 1
    elif method == 'TL':
        mu = float(input("Mu value: "))
        gamma = float(input("Value for gamma: "))
        alpha = beta = r1 = r2 = 0
        k_c = J_c = 1
    elif method == 'EI':
        print("R1 should be less than R2 for electrostatic models.")
        r1 = float(input("R1 value: "))
        r2 = float(input("R2 value: "))
        gamma = float(input("Value for gamma: "))
        alpha = beta = mu = 0
        k_c = J_c = 1
    elif method == 'TM':
        print("Retrieving temperatures from change_me.py...")
        choose = input("Change k & J values from 1? [Y/N] ").upper()
        if choose == 'Y':
            k_c = float(input("k value: "))
            J_c = float(input("J value: "))
        else: k_c = J_c = 1
        alpha = beta = gamma = mu = r1 = r2 = 0
    else: raise ValueError("Method not recognized")
    start_time = time.time()
    simulate(method, generations, links, alpha, beta, gamma, mu, r1,r2,trials,k_c,J_c)
    print("--- %s seconds ---" % (time.time() - start_time))

def alpha_range(generations, links, beta, gamma, trials):
    """To run tests with a range of alpha values"""
    start_time = time.time()
    from change_me import alpha_list
    for a in alpha_list:
        simulate('NN', generations, links, a, beta, gamma, 0, 0, 0, trials, 1, 1)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

def beta_range(generations, links, alpha, gamma, trials):
    """To run tests with a range of beta values"""
    start_time = time.time()
    from change_me import beta_list
    for b in beta_list:
        simulate('NN', generations, links, alpha, b, gamma, 0, 0, 0, trials, 1, 1)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

def mu_range(generations, links, gamma, trials):
    """To run tests with a range of mu values"""
    start_time = time.time()
    from change_me import mu_list
    for m in mu_list:
        simulate('TL', generations, links, 0, 0, gamma, m, 0, 0, trials, 1, 1)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

def r1_range(generations, links, r2, gamma, trials):
    """To run tests with a range of r1 values"""
    start_time = time.time()
    from change_me import r1_list
    for rt1 in r1_list:
        simulate('EI', generations, links, 0, 0, gamma, 0, rt1, r2, trials, 1, 1)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

def r2_range(generations, links, r1, gamma, trials):
    """To run tests with a range of r2 values"""
    start_time = time.time()
    from change_me import r2_list
    for rt2 in r2_list:
        simulate('EI', generations, links, 0, 0, gamma, 0, r1, rt2, trials, 1, 1)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

def full(method, generations, links, trials):
    """You'll have data coming out of your ears"""
    start_time = time.time()
    if method == 'NN':
        from change_me import alpha_list
        from change_me import beta_list
        from change_me import gamma_list
        mu = r1 = r2 = 0
        for a in alpha_list:
            for b in beta_list:
                for g in gamma_list:
                    simulate('NN', generations, links, a, b, g, mu, r1, r2, trials, 1, 1)
    elif method == 'EI':
        from change_me import r1_list
        from change_me import r2_list
        from change_me import gamma_list
        alpha = beta = mu = 0
        for rt1 in r1_list:
            for rt2 in r2_list:
                for g in gamma_list:
                    if rt2 >= rt1:
                        simulate('EI',generations, links, alpha, beta, g,
                                 rt1, rt2, trials, 1, 1)
    elif method == 'TL':
        from change_me import mu_list
        from change_me import gamma_list
        alpha = beta = r1 = r2 = 0
        for m in mu_list:
            for g in gamma_list:
                simulate('TL', generations, links, alpha, beta, g, m, r1, r2, trials, 1, 1)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

def no_evaporation(method, generations, links, trials):
    """You'll have slightly unrealistic data coming out of your ears"""
    start_time = time.time()
    if method == 'NN':
        from change_me import alpha_list
        from change_me import beta_list
        mu = r1 = r2 = 0
        for a in alpha_list:
            for b in beta_list:
                simulate('NN', generations, links, a, b, 0, mu, r1, r2, trials, 1, 1)
    elif method == 'EI':
        from change_me import r1_list
        from change_me import r2_list
        alpha = beta = mu = 0
        for rt1 in r1_list:
            for rt2 in r2_list:
                if rt2 >= rt1:
                    simulate('EI',generations, links, alpha, beta, 0, mu, rt1, rt2, trials, 1, 1)
    elif method == 'TL':
        from change_me import mu_list
        alpha = beta = r1 = r2 = 0
        for m in mu_list:
            simulate('TL', generations, links, alpha, beta, 0, m, r1, r2, trials)
    print("--- runtime is %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()


## Things to look at/fix:
## Clean up formatting
## Make this able to call the lattice class
## Make sure last gen is clean
## Change progress bar for multiple parameters and trial 0
## Steady-state analysis for more timesteps?
## Make sure I'm doing standard deviation correctly
