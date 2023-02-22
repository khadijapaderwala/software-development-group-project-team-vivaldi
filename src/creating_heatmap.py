# script that will take from the user the list of rs IDs. 
# It will then calculate the LD for all pairs of SNPs, and create a heatmap for each population separately, 
# and for r2 and D' separately.

from LD_calculation_function import LinkageDisequilibrium 
from LDheatmap import LDheatmap
import matplotlib.pyplot as plt
import numpy as np

# from the html page, the code would somehow create a list 
# and I can link to it from here, obtain the list 

# simulating a list of rsIDs chosen by the user
rsID_list = ['rs1050979', 'rs9405661', 'rs13217044', 'rs12203596']
results_pairwise_LD = []

# Loop over every possible pair of strings
for i in range(len(rsID_list)):
    for j in range(i+1, len(rsID_list)):
        rsID_1 = rsID_list[i]
        rsID_2 = rsID_list[j]
        # Call your function with the two strings
        result = LinkageDisequilibrium(rsID_1, rsID_2)
        results_pairwise_LD.append(result)
# This creates the list of dictionaries with ALL the LD values and calculations
print(results_pairwise_LD)


####### lets try this for the british pop r2 values. 
# extracting information from the list of dictionaries 
# this obtains the r2 values list
british_r2_values = [d['british_r2'] for d in results_pairwise_LD]
print(british_r2_values)

british_r2_heatmap = LDheatmap(british_r2_values, rsID_list)
plt.show()

