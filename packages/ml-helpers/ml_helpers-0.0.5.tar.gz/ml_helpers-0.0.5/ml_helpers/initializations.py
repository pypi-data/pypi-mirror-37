import numpy as np

def zeros(num_features):
  w = np.zeros((num_features, 1))
  b = 0
  return w, b