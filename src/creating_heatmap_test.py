# script that will take from the user the list of rs IDs. 
# It will then calculate the LD for all pairs of SNPs, and create a heatmap for each population separately, 
# and for r2 and D' separately.

from LD_calculation_function import LinkageDisequilibrium 
from LDheatmap import LDheatmap
import matplotlib.pyplot as plt
import csv

# from the html page, the code would somehow create a list 
# and I can link to it from here, obtain the list 

# simulating a list of rsIDs chosen by the user
rsID_list = ['rs1050979', 'rs9405661', 'rs13217044', 'rs12203596']
results_pairwise_LD = []

# Loop over every possible pair of strings
for i in range(len(rsID_list)):
    print(i)
    for j in range(i+1, len(rsID_list)):
        print(j)
        rsID_1 = rsID_list[i]
        rsID_2 = rsID_list[j]
        # Call your function with the two strings
        result = LinkageDisequilibrium(rsID_1, rsID_2)
        results_pairwise_LD.append(result)
# This creates the list of dictionaries with ALL the LD values and calculations
print(results_pairwise_LD)


# print out the file as a txt file for the user
def write_table_to_file(data):
    with open('output.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(data[0].keys())  # Write the header row
        for row in data:
            writer.writerow(row.values()) 
file = write_table_to_file(results_pairwise_LD)
print(file)




####### ALL THE NECESSERY OUTPUTS FOR THE HEATMAPS. 
# BRITISH R2, NIGERIAN R2, JAPANESE R2
# BRITISH D', NIGERIAN D', JAPANESE D' 
#  
# extracting information from the list of dictionaries 
# this obtains the r2 values list
british_r2_values = [d['british_r2'] for d in results_pairwise_LD]
print(british_r2_values)

nigerian_r2_values = [d['nigerian_r2'] for d in results_pairwise_LD]
print(nigerian_r2_values)

japanese_r2_values = [d['japanese_r2'] for d in results_pairwise_LD]
print(japanese_r2_values)

british_dprime_values = [d['british_Dprime'] for d in results_pairwise_LD]
print(british_r2_values)

nigerian_dprime_values = [d['nigerian_Dprime'] for d in results_pairwise_LD]
print(nigerian_r2_values)

japanese_dprime_values = [d['japanese_Dprime'] for d in results_pairwise_LD]
print(japanese_r2_values)


#### TITLES FOR EACH HEATMAP
british_r2_title = 'british_r2_values'
nigerian_r2_title = 'nigerian_r2_values'
japanese_r2_title = 'japanese_r2_values'
british_dprime_title = 'british_dprime_values'
nigerian_dprime_title = 'nigerian_dprime_values'
japanese_dprime_title = 'japanese_dprime_values'



### BRITISH R2 HEATMAP
british_r2_heatmap = LDheatmap(british_r2_values, rsID_list, british_r2_title)
plt.savefig("british_r2.png")

### NIGERIAN R2 HEATMAP
nigerian_r2_heatmap = LDheatmap(nigerian_r2_values, rsID_list, nigerian_r2_title)
plt.savefig("nigerian_r2.png")

### JAPANESE R2 HEATMAP
japanese_r2_heatmap = LDheatmap(japanese_r2_values, rsID_list, japanese_r2_title)
plt.savefig("japanese_r2.png")


### BRITISH DPRIME HEATMAP
british_dprime_heatmap = LDheatmap(british_dprime_values, rsID_list, british_dprime_title)
plt.savefig("british_dprime.png")

### NIGERIAN DPRIME HEATMAP
nigerian_dprime_heatmap = LDheatmap(nigerian_dprime_values, rsID_list, nigerian_dprime_title)
plt.savefig("nigerian_dprime.png")

### JAPANESE DPRIME HEATMAP
japanese_dprime_heatmap = LDheatmap(japanese_dprime_values, rsID_list, japanese_dprime_title)
plt.savefig("japanese_dprime.png")


