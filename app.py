import numpy as np
import matplotlib.pyplot as plt

def maskingEfficiency(n, lambdaP):
    E_single = 20 * np.log10(lambdaP / (2 * 3e-2))
    E_total = E_single - 20 * np.log10(np.sqrt(n))
    return E_total

f = 3.26e9
c = 3e8
lambdaP = c/f
plateWidth = 50e-2
plateHeight = 50e-2
holeWidth = 2e-2
holeHeight = 3e-2