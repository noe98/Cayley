"""
Author: Will Hanstedt
Filename: latticevol.py
Project: Research for Irina Mazilu, Ph.D.

A file to run large numbers of trials for the lattice type network.
"""

import Cayley as cy
import Cayley.graphics as cg
import Cayley.research as cr
import xlsxwriter as xl
import time
from math import sqrt
timesteps = cr.variable('timesteps',int)
initial_state = cr.variable('initial_state',str)
node_list = cr.variable('node_list',list,int)
temp_d = cr.variable('temp_d',dict,float)


def simulate(method, model, length, width, height, alpha, beta, gamma, mu, r1, r2,trials,k,J):
    """The important one"""
    length_tag = length
    width_tag = width
    height_tag = height
    if model == 'full':
        length += 2
        width += 2
        height += 2
    elif model == 'flat':
        length += 2
        width += 2
    elif model == 'linear':
        length += 2

    network = cy.Lattice(length,width,height)
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
        name = ("NN%dx%dx%d_%sα_%sβ_%sγ.xlsx" % (length_tag, width_tag, height_tag,
                                                 a_tag, b_tag, g_tag))
        tags = a_tag+'-'+b_tag+'-'+g_tag
    elif method == 'TL':
        name = ("TL%dx%dx%d_%sμ_%sγ.xlsx" % (length_tag, width_tag, height_tag,
                                                m_tag, g_tag))
        tags = m_tag+'-'+g_tag
    elif method == 'EI':
        name = ("EI%dx%dx%d_%sr1_%sr2_%sγ.xlsx" % (length_tag, width_tag, height_tag,
                                                      r1_tag, r2_tag, g_tag))
        tags = r1_tag+'-'+r2_tag+'-'+g_tag
    elif method == 'TM':
        tag_list = ()
        for s in range(len(temp_d)):
            tag_list += ("%.2f"%temp_d[s],)
        tags = ("%s_"*(len(temp_d)-1)+"%s") %tag_list
        name = ("TM%dx%dx%d_"%(length_tag,width_tag,height_tag)+tags+".xlsx")
    else: raise ValueError("Method not recognized")
    print("\n#### RUNNING SIMULATION %s ####\n"%(name))

    workbook = xl.Workbook(name)
    #JKP: This all can be incorporated with new node feature ability
    density_list = dict() #[trial][timestep] stores overall densities
    state_collect = dict() #[trial] stores final state dictionaries
    node_d = dict() #[trial#][pair index][node index][timestep] stores node values
    overtime = workbook.add_worksheet("Over_Time")

    for m in range(trials):
        density_list[m] = [0]*(timesteps+2)

    for i in range(trials):
        monte.clear()
        if method == 'TM': monte.randomSpins()
        else:
            if initial_state == "empty": monte.emptyDictionary()
            elif initial_state == "random": monte.randomDictionary()

        if method == 'TM':
            iterate = len(temp_d)
            for d in network.getNodes():
                temp = temp_d[d%iterate]
                network.add(d,temperature=temp)

        for t in range(timesteps+1):
            if method == 'NN':
                monte.simulateNN()
            elif method == 'EI':
                monte.simulateEI()
            elif method == 'TL':
                monte.simulateTL(t)
            elif method == 'TM':
                monte.simulateTemp()

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
            if model == 'full':
                coor_d = network.getNodeFeature('coords')
                for x in network: ## # gives adjusted, can't use len(monte.network)
                    if not (0 in coor_d[x] or coor_d[x][0] == length-1 or\
                            coor_d[x][1] == width-1 or coor_d[x][2] == height-1):
                        sum_t += monte.simData(y)[x] #JKP: Follows new updates
            elif model == 'flat':
                coor_d = network.getNodeFeature('coords')
                for x in network:
                    c = coor_d[x]
                    if not (0 in c[0:2] or c[0] == length-1 or c[1] == width-1):
                        sum_t += monte.simData(y)[x]
            elif model == 'linear':
                coor_d = network.getNodeFeature('coords')
                for x in network:
                    if not(coor_d[x][0] == 0 or coor_d[x][0] == length-1):
                        sum_t += monte.simData(y)[x]
            elif model == 'loop':
                for x in network:
                    sum_t += monte.simData(y)[x]
            dens_t = sum_t/((length_tag)*(width_tag)*(height_tag)) ## # Density at one timestep
            density_list[i][y] = dens_t

        if trials <= 10: # Trial-by-trial is best for small sets
            if model == 'loop':
                worksheet = workbook.add_worksheet("Data trial %d" % (i+1))
                worksheet.write(0,0,"Timestep")
                for x in network:## #
                    worksheet.write(x+1,0,"Node "+str(x))
                for y in range(monte.getTimesteps()): #JKP: Follows new updates
                    worksheet.write(0,y+1,str(y))
                for y in range(monte.getTimesteps()): #JKP: Follows new updates
                    for x in network:
                        worksheet.write(x+1,y+1,monte.simData(y)[x]) #JKP: Follows new updates

        if (trials >= 100) and ((10*i)%trials == 0):
            try:
                ti = (time.time()-run_time)
                print("Trial: "+str(i))
                print(str(ti)+" secs")
            except NameError: pass

    corr_t = dict()
    prod_t = dict() ### Next three dicts are temporary, for diagnosis
    n0_t = dict()
    n1_t = dict()
    for n in range(len(node_list)):
        corr_t[n] = [0]*(timesteps+1)
        prod_t[n] = [0]*(timesteps+1)
        n0_t[n] = [0]*(timesteps+1)
        n1_t[n] = [0]*(timesteps+1)
        for t in range(timesteps+1):
            sum_prod = 0
            n1 = 0
            n2 = 0
            for i in range(trials):
                sum_prod += (node_d[i][n][0][t])*(node_d[i][n][1][t])
                n1 += node_d[i][n][0][t]
                n2 += node_d[i][n][1][t]
            corr_t[n][t] = (sum_prod/trials)-(n1/trials)*(n2/trials)
            prod_t[n][t] = (sum_prod/trials)
            n0_t[n][t] = (n1/trials)
            n1_t[n][t] = (n2/trials)

    for n in range(len(node_list)): # For recording correlations
        sheetname = ("Nodes_%d+%d" %(node_list[n][0],node_list[n][1]))
        chartrange = '='+sheetname+'!$B$2:$'+endcol+'$2'
        timerange = '='+sheetname+'!$B$2:$'+endcol+'$2'
        corr_sheet = workbook.add_worksheet(sheetname)
        corr_sheet.write(0,0,"Timestep")
        corr_sheet.write(1,0,"Correlation")
        corr_sheet.write(5,0,"Product")
        corr_sheet.write(6,0,"Node %d" %(node_list[n][0]))
        corr_sheet.write(7,0,"Node %d" %(node_list[n][1]))
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
            corr_sheet.write(5,t+1,prod_t[n][t])
            corr_sheet.write(6,t+1,n0_t[n][t])
            corr_sheet.write(7,t+1,n1_t[n][t])
    # Average density over time
    overtime.write(0,0,"Timestep")
    data_tag = name
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
            overtime.write(t+5,0,"Trial "+str(t+1))
            for m in range(timesteps+1):
                overtime.write(t+5,m+1,density_list[t][m])
    else:
        overtime.write(6,0,"Trials: "+str(trials))
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
          " nodes for comparison, change the values in the variables.txt file.")
    print("Enter 'full', 'flat', 'linear', or 'loop' for model type.")
    model = input("Model: ").lower()
    if model in ['linear','loop']:
        print("Enter 'NN', 'TL', 'EI', or 'TM' for nearest neighbors, total " +
              "lattice density, empty interval, or temperature methods.")
    else:
        print("Enter 'NN', 'TL', or 'EI' for nearest neighbors, total " +
              "lattice density, or empty interval methods.")
    method = input("Method: ").upper()

    length = int(input("Length: "))
    if model != 'linear' and model != 'loop':
        width = int(input("Width: "))
    else: width = 1
    if model == 'full':
        height = int(input("Height: "))
    else: height = 1

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
    simulate(method, model, length, width, height, alpha, beta, gamma, mu, r1,r2,trials,k_c,J_c)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
