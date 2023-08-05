#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2015-07-19"

import numpy as np
import pandas as pd
import os, shutil







######################### 
###  PRINT FUNCTIONS  ###
#########################

def Print_DataFrame(mytotallist,name,sheet):

	writer=pd.ExcelWriter(name+'.xlsx')
	for n,df in enumerate(mytotallist):
		Single_Print_DataFrame(df,writer,sheet[n])
	writer.save()
	writer.close()

def Single_Print_DataFrame(df,writer,sheet):
	df.to_excel(writer,sheet)

def RemoveFolderData(folder):
	for the_file in os.listdir(folder):
		file_path=os.path.join(folder, the_file)
		if os.path.isfile(file_path):
			os.unlink(file_path)

def PrintMaxEnt(data,targetdir,targetfilename,method='MCS'):

	if method=='MCS':
		# data as pd.Series
		n=data.index.size;
		index=np.arange(1,n+1)
		df=pd.DataFrame(data,columns=[data.name]); df.index=index
		Print_DataFrame([df],targetdir+'/'+targetfilename,['DATA'])