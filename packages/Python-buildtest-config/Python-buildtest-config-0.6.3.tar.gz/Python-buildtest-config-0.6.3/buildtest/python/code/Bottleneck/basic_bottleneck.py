#Create a NumPy array
import numpy as np
a = np.array([1, 2, np.nan, 4, 5])

#Find the nanmean:
import bottleneck as bn
print bn.nanmean(a)
#3.0

#Moving window mean:
print bn.move_mean(a, window=2, min_count=1)
#array([ 1. ,  1.5,  2. ,  4. ,  4.5])
