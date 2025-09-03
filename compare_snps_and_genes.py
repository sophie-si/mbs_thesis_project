#Compare outputs in files
#Look at BPM outputs first
#Then count the genes found and then count the snps found
#Put it in a set and keep comparing if they are the same as the dictionary entry
#Count frequency
import os
import pandas as pd
def freq_counter (inputname, col1, col2, outputname):
#Initialize dictionary to count frequencies
    curr_dict={}
#Get the file names of the CRC group folders
    directory = "C:/Users/sophi/Documents/Plan B Project/"
    matching_files = [f for f in os.listdir(directory) if f.startswith("CRC_g")]
    file_names = [os.path.join(f) for f in matching_files]
#Initialize run counter to 0
    run_counter = 0
#Go through the bpm files in each of the CRC groups and count how many times each pair appears
    for i in file_names:
        results_names = [f for f in os.listdir(i) if inputname in f and not "$" in f]
        if len(results_names) > 0:
            run_counter += 1
            for j in results_names:
                full_path = os.path.join(directory, i, j)
                normalized_path = os.path.normpath(full_path)
                df = pd.read_excel(normalized_path)
                for k in range(len(df)):
                    currlist = df[col1][k], df[col2][k]
                    currlist = tuple(sorted(currlist))
                    if (currlist in curr_dict) and (run_counter > curr_dict.get(currlist)):
                        curr_dict[currlist]+=1
                    else:
                        curr_dict[currlist]=1
#Export the snp_dict to an excel file
    curr_dict_keys = list(curr_dict.keys())
    key_1, key_2 = zip(*curr_dict_keys)
    curr_dict_vals = list(curr_dict.values())
    final_df = pd.DataFrame({col1:key_1, col2:key_2, 'Frequency':curr_dict_vals})
    final_df.to_excel(outputname, index=False) 

#Do it for the snps in the bpm interaction list
freq_counter("interaction_list_bpm", "snp1", "snp2", "snp_freqcount_bpm.xlsx")
freq_counter("interaction_list_bpm", "gene1", "gene2", "gene_freqcount_bpm.xlsx")
freq_counter("interaction_list_wpm", "snp1", "snp2", "snp_freqcount_wpm.xlsx")
freq_counter("interaction_list_wpm", "gene1", "gene2", "gene_freqcount_wpm.xlsx")