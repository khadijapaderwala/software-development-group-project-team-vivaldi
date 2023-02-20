# This is an alternative approach to creating a manhattan plot using a module called qmplot however at the moment is harder to link to our website.

# In your terminal install qmplot.
pip install qmplot

import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
from qmplot import manhattanplot

gwas = pd.read_csv("gwas-association-downloaded_2023-01-30-EFO_0009706-withChildTraits.tsv", sep = '\t')

# Original gwas data.
gwasdata = pd.DataFrame(gwas)

# Filtered gwas data by relevant columns.
df = gwasdata[['SNPS', 'CHR_ID', 'CHR_POS', 'P-VALUE', 'PVALUE_MLOG']] # 815 rows

# Remove rows which are empty for chromosome ID.
df1 = df.dropna(subset=['CHR_ID']) # 553 rows

# Convert 1 to 01 etc to make sure chromosomes are in correct order.
df1['CHR_ID']=df1['CHR_ID'].replace(['1'], '01')
df1['CHR_ID']=df1['CHR_ID'].replace(['2'], '02')
df1['CHR_ID']=df1['CHR_ID'].replace(['3'], '03')
df1['CHR_ID']=df1['CHR_ID'].replace(['4'], '04')
df1['CHR_ID']=df1['CHR_ID'].replace(['5'], '05')
df1['CHR_ID']=df1['CHR_ID'].replace(['6'], '06')
df1['CHR_ID']=df1['CHR_ID'].replace(['7'], '07')
df1['CHR_ID']=df1['CHR_ID'].replace(['8'], '08')
df1['CHR_ID']=df1['CHR_ID'].replace(['9'], '09')

# The above data filtering of the original gwas data is not necessary for use in qmplot (as qmplot can read the data frame as it is) however I have done this so I can obtain df2, the same variable from the Manhattan_Plot.py page.
# However, qmplot does not read any headings so the corresponding headings have to be altered as referenced in the qmplot README.md.
df3 = df1.rename({'CHR_ID': '#CHROM', 'SNPS': 'ID', 'CHR_POS': 'POS', 
                  'P-VALUE': 'P'}, axis = 'columns')

# Sort the df by chromosome number.
df3 = df1.sort_values('#CHROM')

# Generate a Manhattan plot of all the data.
ax = manhattanplot(data = df3,
                  suggestiveline = None,
                  genomewideline = None,
                 xticklabel_kws = {"rotation": "vertical"})

# Generate a Manahattan plot of a specific chromosome in the data.
bx = manhattanplot(data = df3, CHR = "06",
              suggestiveline = None,
              genomewideline = None,
              xlabel = "Chromosome 6")
# Having trouble with this as it does not produce a Manhattan plot of the entire chromosome.

# Save the Manhattan plot as a .png file.
plt.savefig("output_manhattan_plot.png")
