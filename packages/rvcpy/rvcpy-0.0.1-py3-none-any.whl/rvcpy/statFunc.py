#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2017-11-12"

from copy import deepcopy
from scipy.stats import uniform
from scipy.stats import gumbel_r
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import t

import numpy as np
import pandas as pd


## inverse CDF function ##
##########################

def Finv_Uniform(r,a,b):

	return uniform.ppf(r,a,b-a)

def Finv_Gumbel(r,m,s):

	scale,loc=p_Gumbel(m,s)

	return gumbel_r.ppf(r,loc,scale)

def Finv_Normal(r,m,s):

	return norm.ppf(r,m,s)

def Finv_Lognormal(r,m,s):

	sln,mln=p_Lognormal(m,s)

	return lognorm.ppf(r,sln,0,np.exp(mln))

def Finv_t(r,df):

	return t.ppf(r,df)


## CDF function ##
##################

def F_Normal(x,m,s):

	return norm.cdf(x,m,s)

def F_Lognormal(x,m,s):

	sln,mln=p_Lognormal(m,s)

	return lognorm.cdf(x,sln,0,np.exp(mln))

def F_Gumbel(r,m,s):

	scale,loc=p_Gumbel(m,s)

	return gumbel_r.cdf(r,loc,scale)


## PDF function ##
##################

def f_Normal(x,m,s):

	return norm.pdf(x,m,s)

def f_Lognormal(x,m,s):

	sln,mln=p_Lognormal(m,s)

	return lognorm.pdf(x,sln,0,np.exp(mln))


## parameter calculation ##
###########################

def p_Lognormal(m,s):

	cov=s/m;

	sln=np.sqrt(np.log(1+cov**2))
	mln=np.log(m)-1/2*sln**2

	return sln,mln

def p_Gumbel(m,s):

	# parameters Gumbel W&S
	alpha=1.282/s
	u=m-0.5772/alpha

	# parameters Gumbel scipy
	scale=1/alpha
	loc=u

	return scale,loc

## 'moment' calculation ##
##########################

def m_Lognormal(mln,sln):

	cov=np.sqrt(np.exp(sln**2)-1)
	m=np.exp(mln+1/2*sln**2)

	return m,m*cov

## post-processing ##
#####################

def MCStoPDF(sMC,binN):
	# USE: transforms pd_Series into PDF_histogram pd_DataFrame

	# histogram calculation
	(hist,binEdge)=np.histogram(sMC,bins=binN)
	# print(hist)
	# print(binEdge)

	# relative frequency and PDF scaling
	nMCS=len(sMC.index)
	delta_bin=binEdge[2]-binEdge[1]

	relFreq=hist/nMCS
	PDF=relFreq/delta_bin # integral over bin-width equal to relFreq

	# mid-bin listing
	x=(binEdge[1:]+binEdge[:-1])/2

	# pandas DataFrame output
	out=pd.DataFrame([x,PDF],index=['X','mcsPDF'])


	return out.transpose()