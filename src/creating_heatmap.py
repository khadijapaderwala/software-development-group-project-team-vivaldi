

from LD_calculation_function import LinkageDisequilibrium 
from LDheatmap import LDheatmap
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
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

print(results_pairwise_LD)



values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

n = 4

# initialize a 4x4 matrix with all zeros
matrix = np.zeros((n, n))

# assign the values from the list to the appropriate positions in the matrix using a loop
index = 0
for i in range(n):
    for j in range(i+1, n):
        matrix[i][j] = values[index]
        index += 1

print(matrix)


ld = matrix
labels = ['rsID1', 'rsID2', 'rsID3', 'rsID4']
print(ld)
print(labels)

figure = ld_plot(ld=ld, labels=labels)
plt.show()






# test for the code
'''
n = 4

ld = np.random.RandomState(seed=42).random((n, n))
labels = [f'chr1.{i}' for i in range(n)]
print(ld)
print(labels)

figure = ld_plot(ld=ld, labels=labels)
plt.show()
'''







'''
# extracting information from the list of dictionaries 
rsIDs = [(d['rsID_1'], d['rsID_2']) for d in results_pairwise_LD]
#print(rsIDs)

# values
values = [d['british_r2'] for d in results_pairwise_LD]
print(values)

# Initialize a 2D matrix to store the pairwise r2 values
matrix = np.zeros((len(values), len(values)))
#print(matrix)

print(values[0],  # r2 value for SNP1 vs. SNP2
    values[1],  # r2 value for SNP1 vs. SNP3
    values[2], # r2 value for SNP1 vs. SNP4
    values[3],  # r2 value for SNP2 vs. SNP3
    values[4],  # r2 value for SNP2 vs. SNP4
    values[5]) 

# Populate the matrix with the pairwise r2 values
index = 0
for i in range(len(values)):
    for j in range(i+1, len(values)):
            r2 = values[index]
            print(r2)
            matrix[i][j] = r2
            matrix[j][i] = r2
            index += 1
            print(index)


# Set diagonal elements to 1.0
for i in range(len(snps)):
    matrix[i][i] = 1.0

# Print the matrix
for i in range(4):
    for j in range(4):
        print("{:.2f}".format(matrix[i][j]), end='\t')
    print()
'''










# Create a heatmap plot using Seaborn
sns.heatmap(matrix, cmap="YlGnBu", annot=True, square=True)

plt.show()

# code for heatmap of r^2 value

'''
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create a DataFrame with one 'r^2' value.
df = pd.DataFrame([r2], index=['r^2'])

# Calculate the correlation matrix.
corr_matrix = df.corr()

# Create a mask to hide the upper triangle of the correlation matrix.
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# Create the heatmap using seaborn.
sns.heatmap(corr_matrix, cmap='coolwarm', annot=True, mask=mask)

# Remove the x and y-axis labels.
plt.xticks([])
plt.yticks([])

# Display the heatmap.
plt.show()
'''
