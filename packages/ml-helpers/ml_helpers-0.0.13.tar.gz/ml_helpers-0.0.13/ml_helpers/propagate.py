import numpy as np
try:
  from activations import sigmoid, sigmoid_derivative, relu, relu_derivative
except ImportError:
  from .activations import sigmoid, sigmoid_derivative, relu, relu_derivative

def propagate(parameters, X, Y, activation="sigmoid"):
  assert(parameters['W1'].shape[1] == X.shape[0])
  assert(X.shape[1] == Y.shape[1])

  A, caches = _propagate_forward(parameters, X, activation)
  
  Y = Y.reshape(A.shape) # ensure Y is the same shape as AL
  
  grads = _propagate_back(A, Y, caches)
  return grads, _cost(A, Y)

def _propagate_forward(parameters, A_prev, activation="relu", output_activation="sigmoid"):
  caches = []
  L = len(parameters) // 2
  
  # Input + hidden layers
  for l in range(1, L):
    W = parameters['W{}'.format(l)]
    b = parameters['b{}'.format(l)]

    A_prev, cache = _step_forward(A_prev, W, b, activation)
    caches.append(cache)

  # Output layer
  W = parameters['W{}'.format(L)]
  b = parameters['b{}'.format(L)]
  AL, cache = _step_forward(A_prev, W, b, output_activation)
  caches.append(cache)
  
  return AL, caches

def _step_forward(A_prev, W, b, activation="sigmoid"):
  # linear
  # Z[l] = W[l] dot A[l-1] + b[l]
  Z = np.dot(W, A_prev) + b
  linear_cache = (A_prev, W, b)
  
  # activation
  # A[l] = g[l](Z[l])
  if activation == "sigmoid":
    A = sigmoid(Z)
  elif activation == "relu":
    A = relu(Z)
  elif activation == "tanh":
    A = np.tanh(Z)
  
  activation_cache = (Z, activation)

  return A, (linear_cache, activation_cache)

def _cost(A, Y):
  m = Y.shape[1]
  logprobs = np.multiply(Y, np.log(A)) + np.multiply((1 - Y), np.log(1 - A))
  cost = -np.sum(logprobs) / m
  cost = np.squeeze(cost) # Turns [[17]] to 17
  return cost

def _propagate_back(AL, Y, caches):
  grads = {}
  L = len(caches) # number of layers  

  # derivative of the cost function with respect to AL
  dA = -(np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

  # Loop from l=L-1 to l=0
  for l in reversed(range(L)):
    current_cache = caches[l]
    dw, db = "dW{}".format(l + 1), "db{}".format(l + 1)
    dA, grads[dw], grads[db] = _step_backward(dA, current_cache)
  
  return grads


def _step_backward(dA, cache):
  ((A_prev, W, b), (Z, activation)) = cache

  # dZ = dA * g[l]'(Z[l])
  if activation == "relu":
    activation_derivative = relu_derivative(Z)
  elif activation == "sigmoid":
    activation_derivative = sigmoid_derivative(Z)

  dZ = dA * activation_derivative

  m = A_prev.shape[1]
  dA_prev = np.dot(np.transpose(W), dZ) # * D / keep_prob
  dW = np.divide(np.dot(dZ, np.transpose(A_prev)), m)# + (lambd/m) * W
  db = np.divide(np.sum(dZ, axis=1, keepdims=True), m)

  return dA_prev, dW, db