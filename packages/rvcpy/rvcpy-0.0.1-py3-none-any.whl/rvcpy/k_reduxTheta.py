# __author__ = "RVC"
# __email__= "ruben.vancoile@gmail.com"
# __date__= "2017-12-14"


import numpy as np

from rvcpy.statFunc import Finv_Normal


## structural steel reduction function ##
#########################################

def kfy_struct(Theta, method='Negar', r=0):
    if method == 'Negar':
        return kfy_struct_Negar(Theta, r, 1)

    return 0


def kfy_struct_Negar(Theta, r, base=1, methodEN=2):
    # (Negar Elhami Khorasani, 2015) as given in nota Thomas Gernay: MaxEnt-1panel_V2.docx

    if base == 1:  # no base
        # regression coefficients (Khorasani, 2015), p.128, Eq. 5.6, as given in Excel datasheet
        t1 = 1.610513417
        t2 = -0.001675254547
        t3 = -0.000003363505313
        t4 = 0.3543142209

        # error term regression
        eps = Finv_Normal(r, 0, 1)

        # evaluation
        Z = t1 + t2 * Theta + t3 * Theta ** 2 + t4 * eps

        return 1.2 * np.exp(Z) / (np.exp(Z) + 1)  # kfy, Eq. 5.6 (Khorasani, 2015)
    elif base == 2:  # NIST base
        return 0
    elif base == 3:  # EC base
        # currently found to be problematic

        kfyEN = kfy_struct_EN(Theta, methodEN)  # [-] Eurocode nominal reduction factor
        # method 2 ==> utility formula section 4.2.4 as default EN 1993-1-2

        # base value
        rlogit = np.log(((kfyEN + 10 ** -6) / 1.7) / (1 - (kfyEN + 10 ** -6) / 1.7))
        eps = Finv_Normal(r, 0, 1)

        # evaluation
        teller = 1.7 * np.exp(rlogit + 0.412 - 0.81 * 10 ** -3 * Theta + 0.58 * 10 ** -6 * Theta ** 1.9 + 0.43 * eps)
        noemer = (1 + np.exp(rlogit + 0.412 - 0.81 * 10 ** -3 * Theta + 0.58 * 10 ** -6 * Theta ** 1.9 + 0.43 * eps))
        kfy = teller / noemer

    return kfy


def kfy_struct_EN(Theta, method=2):
    if method == 1:
        # tabulated data, Table 3.1, EN 1993-1-2

        # not programmed
        return 0
    elif method == 2:
        # utilisation formula, 4.2.4, EN 1993-1-2
        return (1 / (0.9674 * (1 + np.exp((Theta - 492) / 39.19)))) ** (1 / 3.833)
