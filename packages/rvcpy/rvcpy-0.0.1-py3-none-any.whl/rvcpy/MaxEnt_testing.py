# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2018-06-28"

#
# sampling scheme for external model input
# L=5 is hardcoded - limited variable may exist at different locations, but has not been finalized
#


####################
## MODULE IMPORTS ##
####################

import pandas as pd
import numpy as np
import sys


directory="C:/Users/rvcoile/Google Drive/Research/Codes/Python3.6/REF/rvcpy"
sys.path.append(directory)
from rvcpy.PrintAuxiliary import Print_DataFrame

# from rvcpy.statFunc import F_Normal

###############
## HARDCODED ##
###############

##############
## FUNCTION ##
##############

##########
## CORE ##
##########

## user input ##
################

# filename
filename=input("\nPlease provide path to input file Gauss samples (*.xlsx): ")
if filename[0]=="\"": filename=filename[1:-1] # strips quotes from path

# sheet Excel file with data
print("\n## Gauss samples in sheet 'modelInput'. Note required layout. ##")
u=input("Press ENTER to confirm, or provide name of worksheet: ")
if u!='': sheet=u;
else: sheet='DATA'
print("\nWorksheet set to ", sheet)

# Test to be performed
print("Please provide number of Test to be performed: ")
print("1 : direct test single variable")
u=input("\n")
test=int(u)

## Test application ##
######################

if test==1:
    Y=Test01(X)


## MaxEnt output generation ##
##############################

# Print_DataFrame([samples_modelInput,samplingScheme],outdir+'/MDRMGauss_samples',['modelInput','samplingScheme'])

##########
## TEST ##
##########

print(test)