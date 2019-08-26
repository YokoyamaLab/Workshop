import math
import numpy as np
import matplotlib.pyplot  as plt

lam = 20.5

t = np.arange(0, 51)

x = np.array( [] )

for i in range(0,51):
    res = pow(lam,i) * pow(math.e,-lam) / math.factorial(i)
    print(res)
    x = np.append(x, res)

plt.plot(t, x)

plt.show()
