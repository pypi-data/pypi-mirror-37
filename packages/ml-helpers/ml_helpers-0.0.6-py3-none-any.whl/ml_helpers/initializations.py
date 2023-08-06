import numpy as np

def initialize_parameters(layer_dimensions, W_multiplier=0.01, use="random"):
  """
  Inputs:
      layer_dimensions -- list of dimensions of each layer in network including the input layer

  Output:
      parameters -- dictionary containing W1, b1, ... WL, bL
  """

  parameters = {}
  
  # number of layers in network
  L = len(layer_dimensions)

  if (L < 2):
    raise ValueError("layer_dimensions must have at least 2 elements (one input, one output")

  for l in range(1, L):
    W = 'W{}'.format(str(l))
    b = 'b{}'.format(str(l))
    current_layer_nodes_count = layer_dimensions[l]
    previous_layer_nodes_count = layer_dimensions[l - 1]
    
    if use == "zeros":
        parameters[W] = np.zeros((current_layer_nodes_count, previous_layer_nodes_count))
    elif use == "random":
        parameters[W] = np.random.randn(current_layer_nodes_count, previous_layer_nodes_count) * W_multiplier
    elif use == "he":
        parameters[W] = np.random.randn(current_layer_nodes_count, previous_layer_nodes_count) * np.sqrt(2/previous_layer_nodes_count)
    else:
        raise ValueError("invalid 'use' argument")
    
    parameters[b] = np.zeros((current_layer_nodes_count, 1))

  return parameters


def zeros(num_features):
  if num_features < 1:
    raise ValueError('num_features must be greater than zero')
  w = np.zeros((1, num_features))
  b = 0
  return {'W1': w, 'b1': b}

def initialize_lr_with_zeros(num_features):
  if num_features < 1:
    raise ValueError('num_features must be greater than zero')

  return initialize_parameters([num_features, 1], use="zeros")
  w = np.zeros((1, num_features))
  b = 0
  return {'W1': w, 'b1': b}