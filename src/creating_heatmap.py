# This script will take from the user the list of rs IDs. 
# It will then calculate the LD for all pairs of SNPs, and create a heatmap for each population separately, 
# and for r2 and D' separately.
# then the table of results will be saved as a txt file.

from src.LD_calculation_function import LinkageDisequilibrium 
from src.LDheatmap import LDheatmap
import matplotlib.pyplot as plt
import numpy as np
import csv

# simulating a list of rsIDs chosen by the user
#rsID_list = ['rs1050979', 'rs9405661', 'rs13217044', 'rs12203596']


# Loop over every possible pair of strings
def LD(rsID_list):
    results_pairwise_LD = []
    for i in range(len(rsID_list)):
        for j in range(i+1, len(rsID_list)):
            rsID_1 = rsID_list[i]
            rsID_2 = rsID_list[j]
            # Call your function with the two strings
            result = LinkageDisequilibrium(rsID_1, rsID_2)
            results_pairwise_LD.append(result)

            ####### ALL THE NECESSERY OUTPUTS FOR THE HEATMAPS. 
            # BRITISH R2, NIGERIAN R2, JAPANESE R2
            # BRITISH D', NIGERIAN D', JAPANESE D' 
            #  
            # extracting information from the list of dictionaries 
            # this obtains the r2 values list
            british_r2_values = [d['british_r2'] for d in results_pairwise_LD]
            nigerian_r2_values = [d['nigerian_r2'] for d in results_pairwise_LD]
            japanese_r2_values = [d['japanese_r2'] for d in results_pairwise_LD]
            british_dprime_values = [d['british_Dprime'] for d in results_pairwise_LD]
            nigerian_dprime_values = [d['nigerian_Dprime'] for d in results_pairwise_LD]
            japanese_dprime_values = [d['japanese_Dprime'] for d in results_pairwise_LD]

            #### TITLES FOR EACH HEATMAP
            british_r2_title = 'british_r2_values'
            nigerian_r2_title = 'nigerian_r2_values'
            japanese_r2_title = 'japanese_r2_values'
            british_dprime_title = 'british_dprime_values'
            nigerian_dprime_title = 'nigerian_dprime_values'
            japanese_dprime_title = 'japanese_dprime_values'

            ### BRITISH R2 HEATMAP
            british_r2_heatmap = LDheatmap(british_r2_values, rsID_list, british_r2_title)
            plt.savefig("static/british_r2.png")

            ### NIGERIAN R2 HEATMAP
            nigerian_r2_heatmap = LDheatmap(nigerian_r2_values, rsID_list, nigerian_r2_title)
            plt.savefig("static/nigerian_r2.png")

            ### JAPANESE R2 HEATMAP
            japanese_r2_heatmap = LDheatmap(japanese_r2_values, rsID_list, japanese_r2_title)
            plt.savefig("static/japanese_r2.png")


            ### BRITISH DPRIME HEATMAP
            british_dprime_heatmap = LDheatmap(british_dprime_values, rsID_list, british_dprime_title)
            plt.savefig("static/british_dprime.png")

            ### NIGERIAN DPRIME HEATMAP
            nigerian_dprime_heatmap = LDheatmap(nigerian_dprime_values, rsID_list, nigerian_dprime_title)
            plt.savefig("static/nigerian_dprime.png")

            ### JAPANESE DPRIME HEATMAP
            japanese_dprime_heatmap = LDheatmap(japanese_dprime_values, rsID_list, japanese_dprime_title)
            plt.savefig("static/japanese_dprime.png")
    # This creates the list of dictionaries with ALL the LD values and calculations
    return results_pairwise_LD


# print out the file as a txt file for the user
def write_table_to_file(data):
    with open('static/output.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(data[0].keys())  # Write the header row
        for row in data:
            writer.writerow(row.values()) 

