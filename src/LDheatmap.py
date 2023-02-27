# File for the function that creates the heatmaps for D' and r^2 measures of LD. 

import matplotlib.pyplot as plt
import numpy as np
import itertools

def LDheatmap(values, labels, title):
    '''
    Plot of a Linkage Disequilibrium (LD) matrix
    Inputs: 
    :param values: a list of values, of either r2 or D'.
    The function then creates a matrix like this:
    [[0.  1   2   3]
    [0.  0.   4   5]
    [0.  0.  0.   6]
    [0.  0.  0.  0. ]]
    Where the 0s are, they won't show on the heatmap as they are masked. 
    :param labels: A list of position names, such as rsIDs. 
    :param title: A string for the title of the heatmap.
    
    output: a triangle heatmap with the position names, whose size depends on the size of the ld matrix.
    '''
    
    # The size of the matrix is dictated by the length of the labels. A matrix of 0s is created.
    n = len(labels)
    ld = np.zeros((n, n))

    # Assign the values to the appropriate positions in the matrix using a loop
    index = 0
    for i in range(n):
        for j in range(i+1, n):
            ld[i][j] = values[index]
            index += 1 

    # Assigning the number of rows in the ld matrix to n
    n = ld.shape[0]

    # Initialize the figure for plotting
    figure = plt.figure()

    # Creating a mask for the lower triangle of the matrix (so bottom left corner of the input matrix)
    mask = np.tri(n, k=0)
    ld_masked = np.ma.array(ld, mask=mask)

    # Creating a 2x2 transformation matrix to transform the plot 
    t = np.array([[1, 0.5], [-1, 0.5]])
    # Creates a coordinate matrix by using itertools.product to generate all possible combinations of row/column indices 
    # and transforms the coordinates using the t matrix
    coordinate_matrix = np.dot(np.array([(i[1], i[0]) 
                                for i in itertools.product(range(n, -1, -1), range(0, n + 1, 1))]), t)

    # Adds a subplot
    ax = figure.add_subplot(1, 1, 1)
    # Sets the position of the bottom spine to the center of the plot
    ax.spines['bottom'].set_position('center')
    # Hides the top, right, and left spine, and y-axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Sets the tick parameters for the x-axis
    plt.tick_params(axis='x', which='both', top=False)
    # Plots the heatmap using pcolormesh and np.flipud to flip the matrix vertically.
    plt.pcolormesh(coordinate_matrix[:, 1].reshape(n + 1, n + 1),
                   coordinate_matrix[:, 0].reshape(n + 1, n + 1), np.flipud(ld_masked))
    # Specifies the x-tick parameters for the plot
    plt.xticks(ticks=np.arange(len(labels)) + 0.5, labels=labels, rotation='vertical', fontsize=8)
    # Adding a colourbar 
    plt.colorbar()
    # Add a title 
    plt.title(title)
    
    return figure
