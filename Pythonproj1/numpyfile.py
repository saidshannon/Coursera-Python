import numpy as np

data=np.genfromtxt("AAPL.csv", delimiter=";", skip_header=1)
print(data)