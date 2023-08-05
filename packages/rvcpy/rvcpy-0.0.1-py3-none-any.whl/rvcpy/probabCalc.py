# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2017-11-24"

import pandas as pd
import sympy as sy
import numpy as np

import rvcpy.statFunc as statFunc
from rvcpy.PrintAuxiliary import Print_DataFrame


########################
## USE AND BACKGROUND ##
########################
#
#
#

###############################
## (TEMPORARY LOCAL SUPPORT) ##
###############################

def ParameterRealization_r(varDict, rArray):
    # evaluates parameter realizations
    # input
    # * parameterDict with info stochastic variable
    # * array of r-values

    ## List of modifications
    # 2017-11-24: created

    DistType = varDict['Dist']

    if DistType == 'N':
        return statFunc.Finv_Normal(rArray, varDict['m'], varDict['s'])
    if DistType == 'LN':
        return statFunc.Finv_Lognormal(rArray, varDict['m'], varDict['s'])
    if DistType == 'G':
        return statFunc.Finv_Gumbel(rArray, varDict['m'], varDict['s'])
    if DistType == 'DET':
        return np.ones(np.shape(rArray)) * varDict['m']


def LS_evaluation(LS_eval, nvar, xMatrix):
    # evaluates limitstate (more generally: evaluates function)
    # input
    # * lambdified function
    # * number of variables
    # * matrix of input values, with row for each set of parameter realizations
    # note
    # ordering of matrix input values must correspond with lambdify order

    ## List of modifications
    # 2017-12-24: created

    #
    ### CODING TO BE IMPROVED ###
    #

    # currently hardcoded number of subs
    # more Pythonic code? !?!?!?
    if nvar == 1:
        lsEvalList = LS_eval(xMatrix[:, 0])
    elif nvar == 2:
        lsEvalList = LS_eval(xMatrix[:, 0], xMatrix[:, 1])
    elif nvar == 3:
        lsEvalList = LS_eval(xMatrix[:, 0], xMatrix[:, 1], xMatrix[:, 2])
    elif nvar == 4:
        lsEvalList = LS_eval(xMatrix[:, 0], xMatrix[:, 1], xMatrix[:, 2], xMatrix[:, 3])
    elif nvar == 5:
        lsEvalList = LS_eval(xMatrix[:, 0], xMatrix[:, 1], xMatrix[:, 2], xMatrix[:, 3], xMatrix[:, 4])
    elif nvar == 6:
        lsEvalList = LS_eval(xMatrix[:, 0], xMatrix[:, 1], xMatrix[:, 2], xMatrix[:, 3], xMatrix[:, 4], xMatrix[:, 5])
    ## to be continued

    return lsEvalList


###############
## FUNCTIONS ##
###############

def MonteCarlo(limitstate, ParameterDict, nMC):
    # performs crude Monte Carlo simulation
    # input
    # * limitstate: symbolic limit state function
    # * ParameterDict: dictionary of all parameters, including probabilistic discription
    # * nMC: number of simulations
    # output
    # * array of limit state evaluations, DataFrame with parameter values and limit state valuation, DataFrame with random values

    ## List of modifications
    # 2017-11-24: created
    # 2017-12-24: LS_evaluation outside of MonteCarlo

    ## create MCS array random values
    symbolList = limitstate.atoms(sy.Symbol)
    nvar = len(symbolList)
    rMatrix = np.random.rand(nMC, nvar)

    ## calculate MCS array random realizations
    xMatrix = np.zeros((nMC, nvar))
    # indexing in the ParameterDict - general indexing
    indexDict = {}
    for key in ParameterDict:
        indexDict[ParameterDict[key]['name']] = key
    # random realization per parameter
    varOrder = []
    for i, X in enumerate(symbolList):
        # save order for printing lists
        var = X.name
        varOrder.append(var)
        # collect Dict (stochastic) variable
        localDict = ParameterDict[indexDict[var]]
        xMatrix[:, i] = ParameterRealization_r(localDict, rMatrix[:, i])

    ## evaluate limit state
    limitstateEval = sy.lambdify(tuple(varOrder), limitstate, 'numpy')
    lsEvalList = LS_evaluation(limitstateEval, nvar, xMatrix)

    ## output
    # outR first, before appending the varOrder...
    outR = pd.DataFrame(rMatrix, columns=varOrder)
    # set output - variable realizations + limit state evaluation
    lsEvalList = np.reshape(lsEvalList, (nMC, 1))
    full = np.concatenate((xMatrix, lsEvalList), axis=1)
    varOrder.append('LS')
    outX = pd.DataFrame(full, columns=varOrder)

    return lsEvalList, outX, outR


def Taylor(limitstate, ParameterDict):
    # Taylor approximation of mean value and standard deviation
    # input
    # * limitstate: symbolic limit state function
    # * ParameterDict: dictionary of all parameters, including probabilistic discription
    # output
    # * mean value, standard deviation

    # 2017-11-24: created

    # list of symbols in limitstate
    symbolList = limitstate.atoms(sy.Symbol)
    nvar = len(symbolList)
    xMatrix = np.zeros((2, nvar))  # array mean values and standard deviations

    # indexing in the ParameterDict - general indexing
    indexDict = {}
    for key in ParameterDict:
        indexDict[ParameterDict[key]['name']] = key

    # values per parameter
    varOrder = []
    lsList = []
    for i, X in enumerate(symbolList):
        # save order for printing lists
        var = X.name
        varOrder.append(var)
        # collect Dict (stochastic) variable
        localDict = ParameterDict[indexDict[var]]
        xMatrix[:, i] = [localDict['m'], localDict['s']]
        # take derivative of limitstate function
        ls = sy.diff(limitstate, X)
        lsList.append(ls)

    ## evaluate limit state - mean value
    limitstateEval = sy.lambdify(tuple(varOrder), limitstate, 'numpy')
    m = LS_evaluation(limitstateEval, nvar, xMatrix);
    m = m[0]

    s2 = 0
    for i in np.arange(nvar):
        functionEval = sy.lambdify(tuple(varOrder), lsList[i], 'numpy')
        d = LS_evaluation(functionEval, nvar, xMatrix)
        if type(d) != int: d = d[0]
        s2 = s2 + d ** 2 * xMatrix[1, i] ** 2

    return m, np.sqrt(s2)

##########
## TEST ##
##########

# # limit state
# r,e1,e2=sy.symbols("r e1 e2")
# g=r-e1*e2

# # number of Monte Carlo
# nsim=10

# # ParameterDict
# mr=20; sr=3
# me1=3; se1=2
# me2=5; se2=3

# R={
# 'name':'r',
# 'Dist':'N',
# 'DIM':"[N]",
# 'm':mr,
# 's':sr,
# 'info':''
# }

# E1={
# 'name':'e1',
# 'Dist':'LN',
# 'DIM':"[N]",
# 'm':me1,
# 's':se1,
# 'info':''
# }

# E2={
# 'name':'e2',
# 'Dist':'G',
# 'DIM':"[N]",
# 'm':me2,
# 's':se2,
# 'info':''
# }

# Dict={
# 	'01':R,
# 	'02':E1,
# 	'03':E2
# 	}

# # Z,dfX,dfr=MonteCarlo(g,Dict,nsim)
# # Print_DataFrame([dfr,dfX],'TestOutput/test3var',['r','X'])
# # print(dfr)

# [m,s]=Taylor(g,Dict)


# print(m,s)
