# ------------------------------------------------------------------------------------------------------------
# STANDARDIZED VISUALIZATION MAGNELPY
# 	standardized visualization (colours, lines, labels...)
# 	for standardized input (pd.DataFrame...)
#
# Notes
#	* syntax sub- and superscripts: 'Xijk' write as '$X_{ijk}$''

# Wouter Botte, Ruben Van Coile - 2018
# cfr. Wouter Botte - Figures.py - PhD dissertation 2017
# ------------------------------------------------------------------------------------------------------------

####################
## MODULE IMPORTS ##
####################

import matplotlib.pyplot as plt
import numpy as np
import sys

####################
## MODULE IMPORTS ##
####################

font = {'size': 8}
plt.rc('font', **font)


###################
## AUX FUNCTIONS ##
###################

# def LinePlot_XmultiY(df,saveDir=''):

def LinePlot_XmultiY(df, axisLabels=['X', 'Y'], Xticks=None, Yticks=None, SW_show=False, savePath=None,
                     SW_return=False, Xminorticks=None, Yminorticks=None, SW_grid=False):
    ## lineplot visualization XmultiY
    # note: additional arguments could be packed in a DataFrame with columns X and Y, and different indices
    #
    #
    ## input explanation
    # df 			pd.DataFrame with index values X-axis and columns as Y-valuex
    #				column labels used as legend labels
    # Xticks 		np.array with major X ticks
    # Yticks 		np.array with major Y ticks
    # SW_show		boolean indicating immediate visualization of plot yes/no
    # savePath		path to save figure. Figure not saved if no path provided
    # SW_return		boolean. Returns the figure object (for further custom manipulation) if True
    # Xminorticks	np.array with minor X ticks
    # Yminorticks	np.array with minor Y ticks
    # SW_grid		boolean for gridlines
    #

    ## unpack
    # X values and bounds
    X = df.index.values

    ## initialization of plot - hardcoded parameters magnelpy
    fig, ax1 = plt.subplots(figsize=(3.5, 2.77))
    colors = ['k', 'r', 'green', 'orange', 'blue', 'm', 'c', 'grey', 'brown']
    linestyles = ['-', ':', '--', '-.', '--']
    dash4 = [20, 10]

    ## generation of plot from df data
    for i, key in enumerate(df.columns):
        tmp, = ax1.plot(X, df[key], color=colors[i], label=key, lw=0.5, linestyle=linestyles[i])
        if i == 4: tmp.set_dashes(dash4)

    ## plot formatting
    # set size
    ax1.legend(ncol=1, fontsize=7.5)
    # set ticks
    if Xticks is not None: ax1.set_xlim(Xticks[0], Xticks[-1]); plt.xticks(Xticks)
    if Yticks is not None: ax1.set_ylim(Yticks[0], Yticks[-1]); ax1.set_yticks(Yticks)
    ax1.minorticks_on()
    if Xminorticks is not None: ax1.set_xticks(Xminorticks, minor=True)
    if Yminorticks is not None: ax1.set_yticks(Yminorticks, minor=True)
    # set labels
    ax1.set_xlabel(axisLabels[0])
    ax1.set_ylabel(axisLabels[1])
    # set grids
    if SW_grid: ax1.grid(which='both', axis='both', color='gray', linestyle='-', linewidth=0.3)

    ## plot visualization and printing
    fig.tight_layout()
    if savePath is not None:
        plt.savefig(savePath, dpi=300)
    if SW_show: plt.show()

    if SW_return:
        return fig, ax1


def histogram(df, Xticks, Yticks, width=1, Xlabel='X', Ylabel='PDF [-]'):
    # bar plot of pd.DataFrame, index as X, column as Y
    # not finalized

    # this is for plotting purpose
    index = df['X'].values
    height = df['mcsPDF'].values
    fig = plt.bar(index, height, width)
    plt.xlabel(Xlabel, fontsize=10)
    plt.ylabel(Ylabel, fontsize=10)
    plt.xticks(Xticks, fontsize=8)
    plt.yticks(Yticks, fontsize=8)
    plt.title('Observed histogram')
    plt.show()
