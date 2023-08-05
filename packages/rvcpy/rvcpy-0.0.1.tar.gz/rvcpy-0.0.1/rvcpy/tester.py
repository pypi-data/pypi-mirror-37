#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2017-11-10"

####################
## MODULE IMPORTS ##
####################

# general modules Python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# local modules rvcpy
import rvcpy.k_reduxTheta as kT
from rvcpy.statFunc import F_Normal
from rvcpy.PrintAuxiliary import Print_DataFrame
from rvcpy.EN1990 import kfi_req

from rvcpy.visualization import LinePlot_XmultiY

################
## Test Cener ##
################


baseMethod_Negar=1
# 1: noBase
# 2: NIST - not programmed
# 3: EC3


# temperatures
T=np.arange(0,1200+1,10)

# probabilities stdLow, mean, stdHigh
rlow=F_Normal(-1,0,1)
rmid=F_Normal(0,0,1)
rhigh=F_Normal(1,0,1)

# corresponding kfy 
kfyLow=kT.kfy_struct_Negar(T,rlow,baseMethod_Negar)
kfyMid=kT.kfy_struct_Negar(T,rmid,baseMethod_Negar)
kfyHigh=kT.kfy_struct_Negar(T,rhigh,baseMethod_Negar)

# dataframe
df_kfy=pd.DataFrame([kfyLow,kfyMid,kfyHigh],index=['$k_{fy,Low}$','kfyMid','kfyHigh'],columns=T)
df_kfy=df_kfy.transpose()

# visualize
axisLabels=['T [°C]','kfy [-]']
Ybounds=[0,1.2]
Xticks=np.arange(0,1200+1,200)
Yticks=np.arange(0,1.2+0.1,0.2)
savePath='test.png'
LinePlot_XmultiY(df_kfy,axisLabels=axisLabels,Xticks=Xticks,Yticks=Yticks,savePath=savePath)
# LinePlot_XmultiY(df_kfy,axisLabels=axisLabels)

# plt.figure('kfy')
# plt.plot(df_kfy.index,df_kfy.loc[:,['kfyLow','kfyMid','kfyHigh']])
# plt.grid(True)
# plt.xlabel('Theta [C]')
# plt.ylabel('kfy [-]')
# plt.show()

