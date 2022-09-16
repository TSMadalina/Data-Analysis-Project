import numpy as np
import pandas as pd
import ACP as acp
import scipy.stats as sts  # what does this mean

# clasa care incapsuleaza o implementare de AEF
class AEF:
    def __init__(self, matrix):  # matrix este numpy.ndarray
        self.X = matrix

        # instantiere model ACP
        model = acp.ACP(self.X)
        self.Xstd = model.getXstd()
        self.R = model.getR()

    def getXstd(self):
        return self.Xstd

    def bartlett_test(self, loadings, epsilons):
        n = self.X.shape[0]
        m, q = np.shape(loadings)

        v = self.R
        psi = np.diag(epsilons)
        v_ = loadings @ np.transpose(loadings) + psi

        # calculul matricei identitate estimate
        I_ = np.linalg.inv(v_) @ v
        detI = np.linalg.det(I_)

        if detI > 0:
            chi2 = (n - 1 - (2 * m + 4 * q - 5) / 6) * (np.trace(I_) - np.log(detI) - m)
            r = ((m - q) ** 2 - m - q) / 2
            p_value = sts.chi2.cdf(chi2, r)

        else:
            chi2, p_value = np.nan, np.nan

        return chi2, p_value
