# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 12:08:07 2024

@author: sophi
"""
import random
import os

#Create directory where you want to make the outputs
folder_name = 'Case_and_Control_Groups'
os.mkdir(folder_name)

#Read input files (cases and controls)
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

#Shuffle controls
#Set num_groups to the number of groups you want to make
num_groups = 10
rand_ctrl_list = controlslist.copy()
random.shuffle(rand_ctrl_list)
print(len(rand_ctrl_list)/num_groups)

#Create function to assign groups to the shuffled controls
def assign_groups (rand_list, start_ind, end_ind, grouplist):
    for k in range(start_ind, end_ind):
        grouplist.append(rand_list[k])
    return grouplist     

#Create function to write outputs
#These include cases and controls where a case is 2 and a control is 1
def write_groups (out_folder, filename, cases_list, controls_list):  
    #Create file path to output
    full_path = os.path.join(out_folder, filename)      
    cases_controls_out = open(full_path, "wt")
    for i in range(len(caseslist)):
        print(cases_list[i], cases_list[i], 2, file =cases_controls_out,
              sep = "\t")
    for i in range(len(controls_list)):
        print(controls_list[i], controls_list[i], 1, 
              file = cases_controls_out, sep = "\t")
    cases_controls_out.close()

#Loop through to assign the groups. There are 10 groups in total for CRC case/control cohort.
group_size = (len(rand_ctrl_list))//num_groups 
for i in range(num_groups):
    grouping_list = []
    #condition when you are at the last group to include the remaining samples
    if (i == (num_groups - 1)):
        assign_groups(rand_ctrl_list, i * group_size, len(rand_ctrl_list), grouping_list)
        write_groups(folder_name, f"cases_ctrls_group{i+1}.txt", caseslist, grouping_list)
    else:
        assign_groups(rand_ctrl_list, i * group_size, (i+1) * group_size, grouping_list)
        write_groups(folder_name, f"cases_ctrls_group{i+1}.txt", caseslist, grouping_list)
