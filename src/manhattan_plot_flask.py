from flask import Flask

## Taking the manhattan plot function and putting it into the flask app.
app = Flask(__name__)

@app.route('/plot.png')
def manhattan_plot(data):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
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

if __name__ == '__main__':
    app.run(debug=True)
