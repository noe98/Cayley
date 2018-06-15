"""
"""

import Cayley as cy
import Cayley.game_theory as cg
import xlsxwriter as xl
import time
from math import sqrt
from Cayley.change_me import timesteps
from change_me import senate_corr
import csv

def simulate(model, const, a_const, radius, issue, trials):
    network = cg.Senate(model, const, radius)
    polarity = issue-0.5
    senate = cy.MonteCarlo(network, 1/(a_const*abs(polarity)), 0, 1/(a_const*abs(polarity)))
    run_time = time.time()
    endcol = xl.utility.xl_col_to_name(timesteps+1)


    bp_tag = "%.1d" %const
    ag_tag = "%.1d" %a_const
    rad_tag = "%.3f" %radius
    IV_tag = "%.2f" %issue
    print(issue)
    print(IV_tag)
    if model == 'linear':
        name = ("LIN%sbp_%sag_%sIV" % (bp_tag, ag_tag, IV_tag))
    elif model == 'limited':
        name = ("LMT%sbp_%sag_%sIV_%srad" % (bp_tag, ag_tag, IV_tag, rad_tag))
    elif model == 'complete':
        name = ("CMP%sbp_%sag_%sIV" % (bp_tag, ag_tag, IV_tag))

    print("\n#### RUNNING SIMULATION %s ####\n"%(name))

    workbook = xl.Workbook(name+'.xlsx')
    overtime = workbook.add_worksheet("Over_Time")
##    overall = workbook.add_worksheet("Overall")

    density_list = dict() #[trial][timestep] stores overall densities
    state_collect = dict() #[trial] stores final state dictionaries
    node_d = dict() #[trial#][pair index][node index][timestep] stores node values

    for m in range(trials):
        density_list[m] = [0]*(timesteps+2)

    for i in range(trials):
        senate.clear()
        senate.senateDictionary(issue)

        for t in range(timesteps):
            senate.simulateVote()

        state_collect[i] = senate.simData(senate.getTimesteps()-1)

        node_d[i] = list() ### NOT GONNA BE PRETTY ... ###
        for n in range(len(senate_corr)):
            node_d[i].append([])
            for f in senate_corr[n]:
                node_d[i][n].append({})
                for t in range(timesteps+1):
                    node_d[i][n][f][t] = 2*(monte.simData(t)[senate_corr[n][f]])-1

        for y in range(senate.getTimesteps()):
            sum_t = 0 # Sum of relevant nodes at one timestep
            for x in network:
                sum_t += senate.simData(y)[x]
            dens_t = sum_t/len(network)
            density_list[i][y] = dens_t

        if trials <= 10: # Trial-by-trial is best for small sets
            worksheet = workbook.add_worksheet("Data trial %d" % (i+1))
            worksheet.write(0,0,"Timestep")
            for x in network:
                worksheet.write(x+1,0,"Node "+str(network.keys[x]))
            for y in range(self.getTimesteps()):
                worksheet.write(0,y+1,str(y))
            rank_d = network.getNodeFeature('rank')
            for y in range(self.getTimesteps()):
                for x in network:
                    worksheet.write(int(rank_d[x]),y+1,senate.simData(y)[x])

        if (trials >= 100) and ((10*i)%trials == 0):
            try:
                ti = (time.time()-run_time)
                print("Trial: "+str(i))
                print(str(ti)+" secs")
            except NameError: pass

    if (trials >= 100):
        print("\n#### COMPILING DATA %s ####\n"%(name))
        print(str(time.time()-run_time)+" secs")

    corr_t = dict()
    for n in senate_corr:
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

    for n in range(len(senate_corr)): # For recording correlations
        sheetname = ("%s+%s" %(senate_corr[n][0],senate_corr[n][1]))
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

    # Average density over time
    overtime.write(0,0,"Timestep")
    overtime.write(1,0,name)
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
    print("Enter 'Linear', 'Limited', or 'Complete' for model type.")
    model = input('Model: ').lower()
    trials = int(input("Number of trials: "))
    const = float(input("Input proportionality constant for beta and phi: "))
    a_const = float(input("Input proportionality constant for alpha and gamma: "))
    if model == 'limited':
        radius = float(input("Radius of connection: "))
    else: radius = 0
    issue = float(input("What is the issue rating? "))
    start_time = time.time()
    simulate(model, const, a_const, radius, issue, trials)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
