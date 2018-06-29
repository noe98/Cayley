"""
Author: Will Hanstedt
Filename: gamevol.py
Project: Research for Irina Mazilu, Ph.D.

A file to run high numbers of simulations for the game theory Senate model.
"""

import csv
import Cayley as cy
import Cayley.game_theory as cgt
import Cayley.research as cr
import xlsxwriter as xl
import time
a_list = cr.variable('a_list',list,float)
b_list = cr.variable('b_list',list,float)
c_list = cr.variable('c_list',list,float)
d_list = cr.variable('d_list',list,float)
issue_list = cr.variable('issue_list',list,float)
timesteps = cr.variable('timesteps',int)

def simulate(ac,bc,cc,dc,kc,issue_rating,trials):
    """The big one"""
    run_time = time.time()
    endcol = xl.utility.xl_col_to_name(timesteps+1)
    name = '%.2fa_%.2fb_%.2fc_%.2fd_%.2fIV' %(ac,bc,cc,dc,issue_rating)
    graph = cgt.Senate('blank',1)
    vote_d = dict()
    real_d = dict()
    imag_d = dict()
    workbook = xl.Workbook(name+'.xlsx')
    overtime = workbook.add_worksheet("Over_Time")
    realsheet = workbook.add_worksheet("Real_Reward")
    imagesheet = workbook.add_worksheet("Imagined_Reward")
    for agent in graph:
        vote_d[agent] = [0]*(timesteps+1)
        real_d[agent] = [0]*(timesteps+1)
        imag_d[agent] = [0]*(timesteps+1)

    print("\n#### RUNNING SIMULATION %s ####\n"%(name))

    for i in range(trials):
        graph = cgt.Senate('blank',1)
##        graph.emptyStrategy() ### HM... ###
        strategy_data_dump = list()
        real_data_dump = list()
        imagined_data_dump = list()
        for node in graph:
            cgt.random_agent(graph, node)
        cgt.random_strat_start(graph)
        strategy_data_dump.append(graph.getNodeFeature('strategy'))
        for t in range(timesteps):
            cgt.timestep(graph,issue_rating,ac,bc,cc,dc,kc)
            strategy_data_dump.append(graph.getNodeFeature('strategy'))
            real_data_dump.append(graph.getNodeFeature('real_reward'))
            imagined_data_dump.append(graph.getNodeFeature('imagined_reward'))

##        print(graph)

        graph.clear() ### YES? NO? ###

##        print(graph)

        for agent in graph:
            for t in range(timesteps+1):
                vote_d[agent][t] += strategy_data_dump[t][agent]
                if t != timesteps:
                    real_d[agent][t+1] += real_data_dump[t][agent]
                    imag_d[agent][t+1] += imagined_data_dump[t][agent]
        if (trials >= 100) and ((10*i)%trials == 0):
            try:
                ti = (time.time()-run_time)
                print("Trial: "+str(i))
                print(str(ti)+" secs")
            except NameError: pass

    graph = cgt.Senate('blank',1)
    rank_d = graph.getNodeFeature('rank')

    for agent in graph:
        overtime.write(rank_d[agent]+4,0,agent)
        realsheet.write(rank_d[agent],0,agent)
        imagesheet.write(rank_d[agent],0,agent)
        for t in range(timesteps+1):
            vote_d[agent][t] = vote_d[agent][t]/trials
            real_d[agent][t] = real_d[agent][t]/trials
            imag_d[agent][t] = imag_d[agent][t]/trials
            overtime.write(rank_d[agent]+4,t+1,vote_d[agent][t])
            realsheet.write(rank_d[agent],t+1,real_d[agent][t])
            imagesheet.write(rank_d[agent],t+1,imag_d[agent][t])
    overtime.write(0,0,"Timestep")
    overtime.write(1,0,"Average votes")
    realsheet.write(0,0,"Timestep")
    imagesheet.write(0,0,"Timestep")
    for t in range(timesteps+1):
        t_sum = 0
        for agent in graph:
            t_sum += vote_d[agent][t]
        overtime.write(0,t+1,t)
        overtime.write(1,t+1,t_sum)
        realsheet.write(0,t+1,t)
        imagesheet.write(0,t+1,t)

    over_chart = workbook.add_chart({'type':'line'})
    overtime.insert_chart('I8',over_chart)
    over_chart.set_title({'name':'Does It Pass?'})
    over_chart.set_x_axis({'name':'Timesteps'})
    over_chart.set_y_axis({'name':'Votes'})
    over_chart.add_series({'values':('=Over_Time!$B$2:$'+endcol+'$2'),
                           'name':'=Over_Time!$A$2'})
    over_chart.add_series({'values':('=Over_Time!$B$3:$'+endcol+'$3'),
                           'name':'=Over_Time!$A$3'})
    over_chart.add_series({'values':('=Over_Time!$B$4:$'+endcol+'$4'),
                           'name':'=Over_Time!$A$4'})



    workbook.close()

    print(str(time.time()-run_time) + " secs")




def main():
    print("Input 1 to run single set of parameters. Input 2 to "\
                     +"run ranges of parameters.")
    mode = int(input("Mode: "))
    if mode == 2:
        sets = []
        for ac in a_list:
            for bc in b_list:
                for cc in c_list:
                    for dc in d_list:
                        if dc < cc and cc <= bc and bc < ac:
                            sets.append([ac,bc,cc,dc])
##        print(sets)
##        print(len(sets))
        trials = int(input("Number of trials: "))
        kc = float(input("K value: "))
        start_time = time.time()
        for i in sets:
            for j in issue_list:
                simulate(i[0],i[1],i[2],i[3],kc,j,trials)
        print("\nTOTAL TIME: "+str(time.time()-start_time)+" secs")

if __name__ == '__main__':
    main()
