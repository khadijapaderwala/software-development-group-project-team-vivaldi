import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import matplotlib.pyplot as plt

def manhattan_plot(data):
    # Sort the SNPs by genomic position
    SNPs = data.sort_values("CHR_POS")
    
    # Plot the -log10(p-value) of each SNP against its genomic position
    fig, ax = plt.subplots()
    ax.scatter(SNPs["CHR_POS"], -np.log10(SNPs["P-VALUE"]), s=10)
    
    # Set the axis labels and title
    ax.set_xlabel("Chromosome" + " " + data['CHR_ID'].iloc[0])
    ax.set_ylabel("-log10 (p-value)")
    ax.set_title("Manhattan plot")

    plt.show()
