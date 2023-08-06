import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from _base import *

np.random.seed(42)

x = np.array([1,5,4,3,1])
y = np.array([9,5,4,3,1])
z = np.array(['yes', 'no','yes', 'no','no'])


ScatterPlot(8,5, x, y, \
			hue=z, \
			title = "Title", \
			x_label = "X", \
			y_label = "Y")
plt.show()
 