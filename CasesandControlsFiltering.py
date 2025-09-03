import numpy as np
import pandas as pd

#Open to save just the headers
ukdata = open('ukb45089_filtered1.csv', 'rt')
line = ukdata.readline()
line = line.rstrip()
headers = line.split(',')
ukdata.close()
#cases = 41202-*, 41204-*, 40006-*, 20001-*
#Save the names of all the indices where the column headers that have the indicated values occur
case1_inds = []
for i, curr in enumerate (headers):
    if ("41202" in curr) or ("41204" in curr) or ("40006" in curr):
        case1_inds.append(i)
#Make a new df that only has these columns
case1df = pd.read_csv('ukb45089_filtered1.csv', usecols=case1_inds, low_memory=False)
#C18, C19, C20
#Search for rows that have the CRC values in them, these will be cases
case1_samples = set()
for row in case1df.itertuples():
    for i in range(len(row)):
        if ("C18" in str(row[i])) or ("C19" in str(row[i])) or ("C20" in str(row[i])):
            case1_samples.add(row.Index)
case1_samples_list = sorted(case1_samples)

#controls
#Save the column headers where the indicated values occur
control1_inds = []
for i, curr in enumerate (headers):
    if ("41202" in curr) or ("41204" in curr):
        control1_inds.append(i)
#Make a new df that only contains the columns indicated
control1df = pd.read_csv('ukb45089_filtered1.csv', usecols=control1_inds, low_memory=False)

#Find columns that don't contain a C or D
control1_samples = set()
#shouldn't contain C or D
for row in control1df.itertuples():
    nocdcounter = 0
    for i in range(len(row)):
        if (("C" not in str(row[i]))==True) and (("D" not in str(row[i]))==True):
            nocdcounter += 1
    if nocdcounter == len(row):        
        control1_samples.add(row.Index)
control1_samples_list = sorted(control1_samples) 

#Make a new df that only contains the columns indicated
control2_inds = []
for i, curr in enumerate (headers):
    if ("40006" in curr) or ("40013" in curr) or ("20001" in curr):
        control2_inds.append(i)        
control2df = pd.read_csv('ukb45089_filtered1.csv', usecols=control2_inds, low_memory=False)

#select rows by index so we are only looking at the controls we have filtered out so far and make a new df from it
control2_samples = set()
for row in control2df.itertuples():
    nacounter = 0
    for i in range(len(row)):
        if ("nan" in str(row[i])):
            nacounter += 1
    if nacounter == (len(row)-1):
        control2_samples.add(row.Index)
        
#Check how many control2 samples there are
print(len(control2_samples))

#combine the control sample groups so we are only getting the controls that satisfy both conditions
controls_comb = control2_samples.intersection(control1_samples)

#Make sure there is no overlap between cases and controls
common_elements = controls_comb.intersection(case1_samples)
controls_comb_list = sorted(controls_comb) 

#Export cases and controls as a txt file
firstcol = pd.read_csv('ukb45089_filtered1.csv', usecols=[0])
outputfile = open("cases.txt", "wt")
for i in case1_samples_list:
    caseid= int(firstcol.iloc[i,0])
    print(caseid, file= outputfile)
outputfile.close()
outputfile = open("controls.txt", "wt")
for i in controls_comb_list:
    caseid= int(firstcol.iloc[i,0])
    print(caseid, file= outputfile)
outputfile.close()

#Plot the histogram
#Find only the columns that have the age
age_inds = []
for i, curr in enumerate (headers):
    curr = curr.split("-")
    if ("34" in curr):
        age_inds.append(i)
        
#Make a new df with only the ages
agedf = pd.read_csv('ukb45089_filtered1.csv', usecols= age_inds )
case_agedf = agedf.iloc[case1_samples_list]        
case_agearray = np.array(case_agedf)
#Calculate the ages
case_adj_agearray= np.array(2024 - case_agearray)
case_adj_agelist = list(case_adj_agearray.flatten())

import matplotlib.pyplot as plt
#Plot the distribution
plt.hist(case_adj_agelist, color='skyblue', edgecolor='black')
plt.xlabel('Age (Years)')
plt.ylabel('Frequency')
plt.title('Age Distribution of Colorectal Cancer Cases from UK BioBank Data')
plt.show()

#Controls before filtering them by age
control_agedf = agedf.iloc[controls_comb_list]
control_agearray = np.array(control_agedf)
control_adj_agearray = np.array(2024 - control_agearray)
control_adj_agelist = list(control_adj_agearray.flatten())

plt.hist(control_adj_agelist, color='skyblue', edgecolor='black')
plt.xlabel('Age (Years)')
plt.ylabel('Frequency')
plt.title('Age Distribution of Controls from UK BioBank Data')
plt.show()

#Check average ages between control and case groups. Controls had lower average, so control samples were adjusted
print(sum(case_adj_agelist)/len(case_adj_agelist))
print(np.nansum(control_adj_agearray)/len(control_adj_agelist))

#Do additional age filtering on controls where years 1949 and above are considered in sample group only
control_age_samples = set()
for row in agedf.itertuples():
    for i in range(len(row)):
        if (row[1] <= 1949)==True:
            control_age_samples.add(row.Index)
            
control_age_fil = controls_comb.intersection(control_age_samples)
control_age_fil_list = sorted(control_age_fil)

#Make a plot for the control group now with these new controls
control_age_fildf = agedf.iloc[control_age_fil_list]
control_age_filarray = np.array(control_age_fildf)
control_adj_age_filarray = np.array(2024 - control_age_filarray)
control_adj_age_fillist = list(control_adj_age_filarray.flatten())

plt.hist(control_adj_age_fillist, color='skyblue', edgecolor='black')
plt.xlabel('Age (Years)')
plt.ylabel('Frequency')
plt.title('Age Distribution of Controls from UK BioBank Data')
plt.savefig('Controls_Age_Updated_Histogram.png')
plt.show()

#Save the new control groups
outputfile1 = open("controls1.txt", "wt")
for i in control_age_fil_list:
    controlid = int(firstcol.iloc[i,0])
    print(controlid, file = outputfile1)
outputfile1.close()

#See what races the cases are.
#Find the columns that contain the race information
race_inds = []
for i, curr in enumerate (headers):
    curr = curr.split("-")
    if ("21000" in curr):
        race_inds.append(i)
        
#Make a df that only contains the race info        
racedf = pd.read_csv('ukb45089_filtered1.csv', usecols= race_inds )

#Find the race info for the cases
case_racedf = racedf.iloc[case1_samples_list]        
case_racearray = np.array(case_racedf.iloc[:,0])
case_races = []
for i in range(len(case_racearray)):
    if ("nan" not in str(case_racearray[i])):
        case_races.append(case_racearray[i])
case_races_dict = {}
for i in range(len(case_races)):
    if str(case_races[i]) in case_races_dict:
        case_races_dict[str(case_races[i])] += 1
    else:
        case_races_dict[str(case_races[i])] = 1
case_races_keys = list(case_races_dict.keys())
case_races_vals = list(case_races_dict.values())

#Might show races by what they are by using a table if I need the actual races displayed on the histogram
plt.bar(case_races_keys,case_races_vals)
plt.xticks(rotation=90)
plt.xlabel('Ethnicity')
plt.ylabel('Frequency')
plt.title('Ethnicity Distribution of Cases from UK BioBank Data')   
plt.show()

#Do the same thing for controls just to see
control_racedf = racedf.iloc[control_age_fil_list]        
control_racearray = np.array(control_racedf.iloc[:,0])
control_races = []
for i in range(len(control_racearray)):
    if ("nan" not in str(control_racearray[i])):
        control_races.append(control_racearray[i])
control_races_dict = {}
for i in range(len(control_races)):
    if str(control_races[i]) in control_races_dict:
        control_races_dict[str(control_races[i])] += 1
    else:
        control_races_dict[str(control_races[i])] = 1
control_races_keys = list(control_races_dict.keys())
control_races_vals = list(control_races_dict.values())

#Plot it
plt.bar(control_races_keys,control_races_vals)
plt.xticks(rotation=90)
plt.xlabel('Ethnicity')
plt.ylabel('Frequency')
plt.title('Ethnicity Distribution of Cases from UK BioBank Data')   
plt.show()