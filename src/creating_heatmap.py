
from LD_calculation_function import LinkageDisequilibrium 

ld = LinkageDisequilibrium('rs1050979', 'rs9405661')
print(ld)





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
