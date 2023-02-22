# Requirements
import matplotlib.pyplot as plt
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np

#Read the original GWAS data into a csv.
gwas = pd.read_csv("gwas-association-downloaded_2023-01-30-EFO_0009706-withChildTraits.tsv", sep = '\t')

# Original GWAS data into a data frame.
gwasdata = pd.DataFrame(gwas)

# Filtered gwas data by relevant columns.
df = gwasdata[['SNPS', 'CHR_ID', 'CHR_POS', 'P-VALUE', 'PVALUE_MLOG']]

# Remove rows which are empty for chromosome ID.
df1 = df.dropna(subset=['CHR_ID'])

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

# Sort the df by chromosome number.
df2 = df1.sort_values('CHR_ID')

# Create running_pos variable.
running_pos = 0

# Cumulative position is the position of the SNP in the entire genome opposed to genomic position which is in representative chromosome.
cumulative_pos = []

# For loop to calculate the cumulative positions of all SNPs.
for chrom, group_df2 in df2.groupby('CHR_ID'):
    cumulative_pos.append(group_df2['CHR_POS'] + running_pos)
    running_pos += group_df2['CHR_POS'].max()
    
# Add cumulative_pos column to df.
df2['cumulative_pos'] = pd.concat(cumulative_pos)

# Using seaborn to generate the Manhattan plot.
import seaborn as sns
%matplotlib inline

g = sns.relplot(
    data = df2,
    x = 'cumulative_pos',
    y = 'PVALUE_MLOG',
    aspect = 2,
    hue = 'CHR_ID',
    palette='Set1',
    legend=None
)

# X-axis label.
g.ax.set_xlabel('Chromosome')

# Set x-axis ticks in the middle of all values for each chromosome.
g.ax.set_xticks(df2.groupby('CHR_ID')['cumulative_pos'].median())

# Labelling the x-axis ticks as the chromosome number.
g.ax.set_xticklabels(df2['CHR_ID'].unique())

# Rotate x-axis labels 90 degrees for a cleaner look.
g.set_xticklabels(rotation=90)

# Title
g.fig.suptitle('Manhattan Plot showing p-value association between SNPs linked to Type 1 diabetes')

# Calculates the middle/ median value for each chromosome and that is where the x-axis line is placed for each chromosome.
df2.groupby('CHR_ID')['cumulative_pos'].median()

# Returns the chromosome number from data and this can be used to label x-axis lines.
df2['CHR_ID'].unique()
