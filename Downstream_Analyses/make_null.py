import pandas as pd
import numpy as np
import pickle
from classes import GenstatsOut
from classes import Stats
from classes import bpmindclass

#Load the data in. Get the significant BPMs/WPMs for 2 out of 10, 3, 4 etc runs. Use pvalue 0.05 as a cutoff
#First get the pvalues that are significant for real runs
pvalcut = 0.05
bpmpval_list = []
wpmpval_list = []

for i in range(1,11):
    file= f"CRC_g{i}/intermediate/results_ssM_mhygessi_combined_R0.pkl"
    with open(file, "rb") as file:
        data = pickle.load(file)
    bpm_pval = data.bpm_pv
    wpm_pval = data.wpm_pv

    #Check the stats of the pvals
    print(bpm_pval.describe())
    print(wpm_pval.describe())

    #Save the indices
    bpmrows = bpm_pval[bpm_pval['bpm_pv'] <= pvalcut]
    wpmrows = wpm_pval[wpm_pval['wpm_pv'] <= pvalcut]

    bpmpval_list.append(bpmrows.index)
    wpmpval_list.append(wpmrows.index)

#Save them all
all_vals_bpm = np.concatenate([idx.to_numpy() for idx in bpmpval_list])
counts_bpm = pd.Series(all_vals_bpm, dtype="int64").value_counts().sort_index()
all_vals_wpm = np.concatenate([idx.to_numpy() for idx in wpmpval_list])
counts_wpm = pd.Series(all_vals_wpm, dtype="int64").value_counts().sort_index()

#open file for pathway name info
file1 = "CRC_g1/intermediate/BPMind.pkl"
with open (file1, 'rb') as file1:
    data1 = pickle.load(file1)
    
#This checks to see if the random significant bpm/wpms found that meet a specified threshold match the real bpms/wpms found and how many of them they match with.
def match_inds(in_keys, effect, df_int):
    mask = (df_int['ind'].isin(in_keys)) & (df_int['eff'] == effect)
    return int(mask.sum())

#Use different cutoffs for number of discoveries.
for j in range(2, 10):
    at_least_5_bpm = counts_bpm[counts_bpm >= j]
    at_least_5_wpm = counts_wpm[counts_wpm >= j]
    
    #Map it back to the names
    #Get the pathways for BPMs
    bpms = data1.bpm
    path1 = bpms['path1names']
    path2 = bpms['path2names']
    path1 = path1.append(path1).reset_index().drop(columns = ['index'])
    path2 = path2.append(path2).reset_index().drop(columns = ['index'])
    path1 = path1.iloc[at_least_5_bpm.index].reset_index().drop(columns = ['index'])
    path2 = path2.iloc[at_least_5_bpm.index].reset_index().drop(columns = ['index'])

    #Determine if they have a protective or risk effect
    eff_bpm = []
    for i in range(len(at_least_5_bpm)):
        if at_least_5_bpm.index[i]<=len(bpms.index):
            eff_bpm.append('protective')
        else:
            eff_bpm.append('risk')
    eff_bpm = pd.DataFrame(eff_bpm, columns=['eff'])
    #Convert the at_least_5_bpm into a dataframe
    top_bpm_inds = pd.Series(at_least_5_bpm.index)
    top_bpms = pd.concat([path1, path2, eff_bpm, top_bpm_inds], axis = 1)
    top_bpms = top_bpms.rename(columns = {0:'ind'})
    #get pathways for WPMs
    wpms = data1.wpm
    pathway = wpms['pathway']
    pathway = pathway.append(pathway).reset_index().drop(columns = ['index'])
    pathway = pathway.iloc[at_least_5_wpm.index].reset_index().drop(columns = ['index'])

    #Determine if they have protective or risk effect
    eff_wpm = []
    for i in range(len(at_least_5_wpm)):
        if at_least_5_wpm.index[i]<=len(wpms.index):
            eff_wpm.append('protective')
        else:
            eff_wpm.append('risk')
    eff_wpm = pd.DataFrame(eff_wpm, columns=['eff'])

    #Stitch pathways and effects together
    top_wpm_inds = pd.Series(at_least_5_wpm.index)
    top_wpms = pd.concat([pathway, eff_wpm, top_wpm_inds], axis = 1)
    top_wpms = top_wpms.rename(columns = {0:'ind'})
    
    #Generate Null Distribution
    #We want to select a random genstats run from each of the CRC runs (ex. run 1 genstats3, run 2 genstats5, run 3 genstats 3 etc.)
    m_rand_bpm_total = []
    m_rand_wpm_total = []
    rand_bpms = []
    rand_wpms = []
    #Do this for 1000 iterations
    for _ in range(1000):
        null_prot_bpms = {}
        null_risk_bpms = {}
        null_prot_wpms = {}
        null_risk_wpms = {}
        for i in range(1, 11):
            #generate the random genstats file you want to open for the CRC run
            rand_num = np.random.randint(1,11)
            file = f"CRC_g{i}/intermediate/genstats_ssM_mhygessi_combined_R{rand_num}.pkl"
            with open(file, "rb") as file:
                data = pickle.load(file)
            #do it for protective and then for risk
            prot = data.protective_stats
            bpm_prot_stats = prot.bpm_local_pv
            wpm_prot_stats = prot.wpm_local_pv

            #find pvalues that meet the threshold and count how many times they appear across 10 runs for the bpm
            for ind, pval in enumerate(bpm_prot_stats):
                if (ind in null_prot_bpms) and (pval <= 0.05):
                    null_prot_bpms[ind] += 1
                elif (pval <= 0.05):
                    null_prot_bpms[ind] = 1
            #do this for wpms too
            for ind, pval in enumerate(wpm_prot_stats):
                if (ind in null_prot_wpms) and (pval <= 0.05):
                    null_prot_wpms[ind] += 1
                elif (pval <= 0.05):
                    null_prot_wpms[ind] = 1

            #repeat for the risk interactions
            risk = data.risk_stats
            bpm_risk_stats = risk.bpm_local_pv
            wpm_risk_stats = risk.wpm_local_pv

            for ind, pval in enumerate(bpm_risk_stats):
                if (ind in null_risk_bpms) and (pval <= 0.05):
                    null_risk_bpms[ind] += 1
                elif (pval <= 0.05):
                    null_risk_bpms[ind] = 1
            for ind, pval in enumerate(wpm_risk_stats):
                if (ind in null_risk_wpms) and (pval <= 0.05):
                    null_risk_wpms[ind] += 1
                elif (pval <= 0.05):
                    null_risk_wpms[ind] = 1

        #check how many bpms meet meet the p-value threshold for at least x out of 10 runs
        #let's do it for different numbers and see how the null distribution varies for different p-value cutoffs
        bpm_prot_keys = [key for key, value in null_prot_bpms.items() if value >= j]
        bpm_risk_keys = [key for key, value in null_risk_bpms.items() if value >= j]

        wpm_prot_keys = [key for key, value in null_prot_wpms.items() if value >= j]
        wpm_risk_keys = [key for key, value in null_risk_wpms.items() if value >= j]

        #Count how many of the random bpms/wpms match with the real results and add them up
        match_nums = match_inds(bpm_prot_keys, 'protective', top_bpms)
        match_nums1 = match_inds(bpm_risk_keys, 'risk', top_bpms)
        match_nums2 = match_inds(wpm_prot_keys, 'protective', top_wpms)
        match_nums3 = match_inds(wpm_risk_keys, 'risk', top_wpms)
        m_random_bpm = match_nums + match_nums1
        m_random_wpm = match_nums2 + match_nums3
        #Add them to the list for each iteration
        m_rand_bpm_total.append(m_random_bpm)
        m_rand_wpm_total.append(m_random_wpm)
        
        #Add to the list the total bpms/wpms that meet the threshold(they don't have to match the real data)
        rand_bpms.append(len(bpm_prot_keys) + len(bpm_risk_keys))
        rand_wpms.append(len(wpm_prot_keys) + len(wpm_risk_keys))
        
        #save outputs
    top_bpms.to_csv(f'bpms_{j}_cutoff.csv', index=False)
    top_wpms.to_csv(f'wpms_{j}_cutoff.csv', index=False)
    with open(f'bpms_{j}_cutoff_nums.txt', 'wt') as outfile:
        for i in m_rand_bpm_total:
            print(i, file = outfile)
    with open(f'wpms_{j}_cutoff_nums.txt', 'wt') as outfile:
        for i in m_rand_wpm_total:
            print(i, file = outfile)
    with open(f'bpms_{j}_cutoff_all.txt', 'wt') as outfile:
        for i in rand_bpms:
            print(i, file = outfile)
    with open(f'wpms_{j}_cutoff_all.txt', 'wt') as outfile:
        for i in rand_wpms:
            print(i, file = outfile)
