# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 12:08:07 2024

@author: sophi
"""
casesin = open("cases.txt", "rt")
caseslist = []
for curr in casesin:
    line = curr.rstrip()
    caseslist.append(line)
casesin.close()

controlslist= []
controlsin = open("controls.txt","rt")
for curr in controlsin:
    line = curr.rstrip()
    controlslist.append(line)
controlsin.close()

import random
rand_ctrl_list = controlslist.copy()
random.shuffle(rand_ctrl_list)
print(len(rand_ctrl_list)/10)

def assign_groups (rand_list, start_ind, end_ind, grouplist):
    for k in range(start_ind, end_ind):
        grouplist.append(rand_list[k])
    return grouplist
group1list = []
assign_groups(rand_ctrl_list, 0, 14050, group1list)      

def write_groups (filename, cases_list, controls_list):        
    cases_controls_out = open(filename, "wt")
    for i in range(len(caseslist)):
        print(cases_list[i], cases_list[i], 2, file =cases_controls_out,
              sep = "\t")
    for i in range(len(controls_list)):
        print(controls_list[i], controls_list[i], 1, 
              file = cases_controls_out, sep = "\t")
    cases_controls_out.close()
write_groups ("cases_ctrls_group1.txt", caseslist, group1list)

group2list = []
assign_groups(rand_ctrl_list, 14050, 14050*2, group2list)
write_groups("cases_ctrls_group2.txt", caseslist, group2list)

group3list = []
assign_groups(rand_ctrl_list, 14050*2, 14050*3, group3list)
write_groups("cases_ctrls_group3.txt", caseslist, group3list)

group4list = []
assign_groups(rand_ctrl_list, 14050*3, 14050*4, group4list)
write_groups("cases_ctrls_group4.txt", caseslist, group4list)

group5list=[]
assign_groups(rand_ctrl_list, 14050*4, 14050*5, group5list)
write_groups("cases_ctrls_group5.txt", caseslist, group5list)

group6list=[]
assign_groups(rand_ctrl_list, 14050*5, 14050*6, group6list)
write_groups("cases_ctrls_group6.txt", caseslist, group6list)

group7list=[]
assign_groups(rand_ctrl_list, 14050*6, 14050*7, group7list)
write_groups("cases_ctrls_group7.txt", caseslist, group7list)

group8list=[]
assign_groups(rand_ctrl_list, 14050*7, 14050*8, group8list)
write_groups("cases_ctrls_group8.txt", caseslist, group8list)

group9list=[]
assign_groups(rand_ctrl_list, 14050*8, 14050*9, group9list)
write_groups("cases_ctrls_group9.txt", caseslist, group9list)

group10list=[]
assign_groups(rand_ctrl_list, 14050*9, len(rand_ctrl_list), group10list)
write_groups("cases_ctrls_group10.txt", caseslist, group10list)
   
# =============================================================================
# cases_controls_out = open("casescontrols.txt", "wt")
# for i in range(len(caseslist)):
#     print(caseslist[i], caseslist[i], 2, file =cases_controls_out,
#              sep = "\t")
# for i in range(len(controlslist)):
#     print(controlslist[i], controlslist[i], 1, 
#              file = cases_controls_out, sep = "\t")
# cases_controls_out.close()
# =============================================================================
    