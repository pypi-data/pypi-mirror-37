# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2017-11-24"

import pandas as pd
import sympy as sy
import numpy as np

from copy import deepcopy

import rvcpy.statFunc as statFunc
from rvcpy.PrintAuxiliary import Print_DataFrame
from rvcpy.GaussWeightsAndPoints import GaussPoints, GaussSampleScheme


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
    #
    ### TO BE IMPROVED ###
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


def MDRM_CalculationPoints(samplingScheme, GaussPoint_df):
    modelInput = pd.DataFrame(index=samplingScheme.index, columns=GaussPoint_df.columns)

    # initialize median values for all parameter realizations
    for var in modelInput.columns:
        modelInput[var] = GaussPoint_df.loc[3, var]

    # correct on every line the single modified Gauss point
    for i in modelInput.index:

        # j,l realization
        [j, l] = samplingScheme.loc[i, :]

        # assignment
        if l != 0:  # 0-value corresponds with median point
            modelInput.loc[i, l] = GaussPoint_df.loc[j, l]

    return modelInput


def MDRMG_sampling(limitstate, ParameterDict, L):
    # input
    # * limitstate: symbolic limit state function - here: more appropriate function 'Y'
    # * ParameterDict: dictionary of all parameters, including probabilistic discription
    # * L: number of Gauss points per stochastic variable (default=5)
    # output
    # * Prints *.xlsx with Gauss realizations for MaxEnt2018.py application
    #
    # indexing in the ParameterDict - general indexing
    indexDict = {}
    for key in ParameterDict:
        indexDict[ParameterDict[key]['name']] = key

    ## calculate Gauss point realizations
    symbolList = limitstate.atoms(sy.Symbol);
    n = len(symbolList)  # number of stochastic variables limitstate
    nSim = (
                       L - 1) * n + 1  # number of sample points - correct for odd L only... But even number inefficient in current procedure
    points = GaussPoints(L)  # Gauss points for L
    r_realizations = statFunc.F_Normal(points, 0, 1);
    r_realizations = r_realizations.flatten()  # quantiles corresponding with Gauss points

    # realizations per variable
    GaussPoint_df = pd.DataFrame(index=np.arange(1, L + 1))
    varOrder = []
    for i, var in enumerate(indexDict.keys()):
        localDict = ParameterDict[indexDict[var]]
        varOrder.append(var)
        samplepoints = ParameterRealization_r(localDict, r_realizations)
        GaussPoint_df[i + 1] = samplepoints

    ## assign in sampling scheme ##
    samplingScheme = GaussSampleScheme(L, n, nSim)
    samples_modelInput = MDRM_CalculationPoints(samplingScheme, GaussPoint_df);
    samples_modelInput.columns = varOrder

    return samples_modelInput, samplingScheme, varOrder


def VarDict_to_df(ParameterDict):
    # transforms ParameterDict syntax into pd.DataFrame syntax (MaxEnt_sampling.py)
    # but VarOrder is important

    # indexing in the ParameterDict - general indexing
    # allows to call the correct parameter-dictionary based on the name of the variable as it appears in the limitstate
    indexDict = {}
    for key in ParameterDict:
        indexDict[ParameterDict[key]['name']] = key

    print(len(indexDict.keys()))

    # define an order of variables, and assign accordingly to pd.DataFrame
    Parameter_df = pd.DataFrame(index=np.arange(len(indexDict.keys()) + 1),
                                columns=['number', 'X', 'type', 'info1', 'info2', 'p1', 'p2'])
    for i, X in enumerate(indexDict.keys()):
        print(i)
        print(X)
        print()

    ## WIP ##

    # save order for printing lists
    # varOrder.append(X)
    # # collect Dict (stochastic) variable
    # localDict=ParameterDict[indexDict[var]]


# return Parameter_df,Parameter_df['X'].tolist()


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


def MaxEnt_GaussEval(limitstate, ParameterDict, L=5):
    # Evaluate Gauss point realizations for MaxEnt calculation
    #
    # input
    # * limitstate: symbolic limit state function - here: more appropriate function 'Y'
    # * ParameterDict: dictionary of all parameters, including probabilistic discription
    # * L: number of Gauss points per stochastic variable (default=5)
    # output
    # * Prints *.xlsx with Gauss realizations for MaxEnt2018.py application
    #

    # input evaluation
    # opportunity for future evaluation : DET-detection and omission
    symbolList = limitstate.atoms(sy.Symbol);
    n = len(symbolList)  # number of stochastic variables limitstate

    # issue: MaxEnt sampling takes pd.DataFrame (cfr. StochVar.xlsx) as input => need to develop switch or adapt code
    # WIP - TMP hardcoded: ParameterDict as dict entry - not yet option to read *.xlsx
    # print(isinstance(ParameterDict,dict))
    # StochVar,varOrder=VarDict_to_df(ParameterDict) # transforms Dict to Stochvar-syntax

    samples_modelInput, samplingScheme, varOrder = MDRMG_sampling(limitstate, ParameterDict, L)

    # # add mean value realization if requested
    # if SW_add_mean:
    #     # initialize series
    #     s = pd.Series(index=samples_modelInput.columns); s.name='MeanEval'
    #     # iterate over stochastic variables and introduce mean value for each of them
    #     for var in StochVar.columns:
    #         local_StochVar=StochVar[var]
    #         mean=MeanEval(local_StochVar)
    #         s[local_StochVar['number']]=mean
    #     # add series to sampling dataframe
    #     samples_modelInput=samples_modelInput.append(s)

    # evaluate model Y
    Y = limitstate  # for notation purposes only
    YEval = sy.lambdify(tuple(varOrder), Y, 'numpy')  # note: YEval identical to limitstateEval in MCS
    MDRMG_realizations = LS_evaluation(YEval, n, samples_modelInput.values)

    # set model output conform MaxEnt input requirement
    MDRMG_out = deepcopy(samplingScheme);
    MDRMG_out['Y'] = MDRMG_realizations
    MDRMG_out = MDRMG_out[['Y', 'j', 'l']]

    return samples_modelInput, samplingScheme, MDRMG_out


##########
## TEST ##
##########

if __name__ == "__main__":
    # limit state
    r, e1, e2 = sy.symbols("r e1 e2")
    g = r - e1 * e2

    # number of Monte Carlo
    nsim = 10

    # ParameterDict
    mr = 20;
    sr = 3
    me1 = 3;
    se1 = 2
    me2 = 5;
    se2 = 3

    R = {
        'name': 'r',
        'Dist': 'N',
        'DIM': "[N]",
        'm': mr,
        's': sr,
        'info': ''
    }

    E1 = {
        'name': 'e1',
        'Dist': 'LN',
        'DIM': "[N]",
        'm': me1,
        's': se1,
        'info': ''
    }

    E2 = {
        'name': 'e2',
        'Dist': 'G',
        'DIM': "[N]",
        'm': me2,
        's': se2,
        'info': ''
    }

    Dict = {
        '01': R,
        '02': E1,
        '03': E2
    }

    # Z,dfX,dfr=MonteCarlo(g,Dict,nsim)
    # Print_DataFrame([dfr,dfX],'TestOutput/test3var',['r','X'])
    # print(dfr)

    [m, s] = Taylor(g, Dict)

    print(m, s)
