import numpy as np

def sigmoid(Z):
  return np.power(1 + np.exp(-Z), -1)

def sigmoid_derivative(Z):
  S = sigmoid(Z)
  return S * (1 - S)