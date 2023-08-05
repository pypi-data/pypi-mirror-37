#__author__ = "RVC"
#__email__= "ruben.vancoile@gmail.com"
#__date__= "2017-11-23"

import numpy as np


## EN 1990 based functions ##
#############################

def Gk_ULS(Rd,chi,u,ULS):
	# calculate MGk for bending ultimate limit state
	# for given load ratio chi = MQk/(MQk+MGk)
	# for given utilisation u

	# parameters
	gamma_G=1.35
	psi_0=0.7
	gamma_Q=1.5
	dzeta=0.85

	if ULS=='STR':
		return u*Rd/np.maximum(gamma_G+psi_0*gamma_Q*chi/(1-chi),dzeta*gamma_G+gamma_Q*chi/(1-chi))
	elif ULS=='EQU':
		return u*Rd/(gamma_G+gamma_Q*chi/(1-chi))

def kfi_req(chi,u,gR=1,ULS='STR'):
	# calculate utilisation fire (time 0 - i.e. no temperature effect), considering utilisation at ambient u
	# for given load ratio chi = Qk/(Qk+Gk)
	#
	# ULS: Rd=Rk/gR
	# ULS: Ed=u*Rd=gE*Ek
	# fire: Rd,fi=kfi*Rk
	# fire: Edfi=Ek=Ed/gE=u*Rd/gE=u*Rk/gE/gR=u*Rd,fi/kfi/gE/gR=ufi*Rdfi/kfi
	# ==> ufi=u/gE/gR

	## history log ##
	# 2017-12-15: created

	# parameters
	gamma_G=1.35
	psi_0=0.7
	gamma_Q=1.5
	dzeta=0.85

	psi_fi=0.5

	if ULS=='STR':
		return u*(1+psi_fi*chi/(1-chi))/np.maximum(gamma_G+psi_0*gamma_Q*chi/(1-chi),dzeta*gamma_G+gamma_Q*chi/(1-chi))
	elif ULS=='EQU':
		return u*(1+psi_fi*chi/(1-chi))/(gamma_G+gamma_Q*chi/(1-chi))