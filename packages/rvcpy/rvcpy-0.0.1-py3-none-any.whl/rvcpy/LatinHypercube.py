# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2017-11-10"

import numpy as np
import pandas as pd
from rvcpy.PrintAuxiliary import *
from scipy.stats import *


################################
### Latin Hypercube function ###
################################

def LHS_rand(number_sim, number_variables, method='Olsson', test=False):
    ## sample (r-values) generation according to LHS scheme
    # method: r-value selection in specified interval
    # 'Olsson': random selection
    # 'Center': center of interval selection

    ### initialise ###
    ##################
    P = np.zeros((number_sim, number_variables))

    ### control variables ###
    #########################

    ### basic setup of integers and random permutation ###
    ######################################################

    x0 = np.arange(1, number_sim + 1, 1)

    for j in np.arange(number_variables):
        P[:, j] = np.random.permutation(x0)

    P = pd.DataFrame(P)

    ### correction for correlation ###
    ##################################

    Yx = P.div(number_sim + 1)
    Y = Yx.apply(norm.ppf)

    Y = Y.as_matrix()
    COV_Y = np.cov(Y, rowvar=0)
    L = np.linalg.cholesky(COV_Y)

    Y = np.dot(Y, np.transpose(np.linalg.inv(L)))
    # Yx=pd.DataFrame(Y)

    ### updated P-matrix (ranks of Y) ###
    #####################################

    Y = pd.DataFrame(Y)
    Y2 = Y.rank()

    ### sampling matrix via ranks & aselect ###
    ###########################################
    if method == 'Olsson':
        R = pd.DataFrame(np.random.rand(number_sim, number_variables))
    elif method == 'Center':
        R = pd.DataFrame(0.5 * np.ones((number_sim, number_variables)))
    Y3 = Y2.subtract(R)

    S = Y3.div(number_sim)

    ### output ###
    ##############

    if test:

        ### printing for testing ###
        Sx = P.subtract(R)
        Sx = Sx.div(number_sim)
        COV_Sx = pd.DataFrame(np.corrcoef(Sx, rowvar=0))
        L = pd.DataFrame(L)
        COV_S = pd.DataFrame(np.corrcoef(S, rowvar=0))

        return P, Sx, COV_Sx, L, Y2, S, COV_S

    else:

        ### standard output ###
        return S


#################
### TEST-ZONE ###
#################

if __name__ == "__main__":
    number_sim = 100
    number_variables = 5

    # LHS_rand(number_sim,number_variables)

    P, Sx, COV_Sx, L, Y2, S, COV_S = LHS_rand(number_sim, number_variables, 'Olsson', True)
    # P, Sx, COV_Sx, L, Y2, S, COV_S=LHS_rand(number_sim,number_variables,'Center',True)

    Print_DataFrame([P, Sx, COV_Sx, L, Y2, S, COV_S], 'LHS_TMP', ['P', 'Sx', 'COV_Sx', 'L', 'Y2', 'S', 'COV_S'])
