import unittest
import numpy as np
from activations import sigmoid, sigmoid_derivative
from propagate import propagate, _cost, _step_forward, _propagate_forward, _step_backward, _propagate_back
from utils import vectorize, normalize_rows, softmax, loss
from initializations import initialize_parameters, initialize_lr_with_zeros


class TestActivations(unittest.TestCase):

  def test_sigmoid(self):
    self.assertEqual(sigmoid(0), 0.5)
    self.assertGreater(sigmoid(100), .99)
    self.assertLess(sigmoid(-100), .01)

    Z = np.array([1,2,3])
    expected = np.array([0.73105858, 0.88079708, 0.95257413])
    self.assertTrue(np.allclose(sigmoid(Z), expected))

  def test_sigmoid_derivative(self):
    self.assertEqual(sigmoid_derivative(0), 0.25)
    self.assertLess(sigmoid_derivative(100), .001)
    self.assertLess(sigmoid_derivative(-100), .001)

    Z = np.array([1, 2, 3])
    expected = np.array([0.1966119, 0.1049935, 0.04517666])
    self.assertTrue(np.allclose(sigmoid_derivative(Z), expected))

class TestUtils(unittest.TestCase):
  
  def test_vectorize(self):
    with self.assertRaises(AssertionError):
      vectorize([])
    
    array = vectorize(np.array([]))
    self.assertEqual(array.shape, (0,1))

    array = vectorize(np.zeros((2,1)))
    self.assertEqual(array.shape, (2,1))

    array = vectorize(np.zeros((1,3)))
    self.assertEqual(array.shape, (3,1))

    array = vectorize(np.zeros((3,4,2,5)))
    self.assertEqual(array.shape, (120,1))

    image = np.array([
      [
        [0.67826139, 0.29380381],
        [0.90714982, 0.52835647],
        [0.4215251 , 0.45017551]
      ],
      [
        [0.92814219, 0.96677647],
        [0.85304703, 0.52351845],
        [0.19981397, 0.27417313]
      ],
      [
        [0.60659855, 0.00533165],
        [0.10820313, 0.49978937],
        [0.34144279, 0.94630077]
      ]
    ])

    expected = np.array([
      [0.67826139],
      [0.29380381],
      [0.90714982],
      [0.52835647],
      [0.4215251 ],
      [0.45017551],
      [0.92814219],
      [0.96677647],
      [0.85304703],
      [0.52351845],
      [0.19981397],
      [0.27417313],
      [0.60659855],
      [0.00533165],
      [0.10820313],
      [0.49978937],
      [0.34144279],
      [0.94630077]
    ])

    self.assertTrue(np.allclose(vectorize(image), expected))

  def test_normalize_rows(self):
    arg = np.zeros((3,2))
    self.assertTrue(np.array_equal(normalize_rows(arg), arg))

    arg = np.array([
      [0, 3, 4],
      [1, 6, 4]
    ])

    expected = np.array([
      [0, 0.6, 0.8],
      [0.13736056, 0.82416338, 0.54944226]
    ])

    self.assertTrue(np.allclose(normalize_rows(arg), expected))

  def test_softmax(self):
    arg = np.zeros((3,2))
    self.assertTrue(np.array_equal(softmax(arg), arg + 0.5))

    arg = np.array([
      [9, 2, 5, 0, 0],
      [7, 5, 0, 0 ,0]
    ])

    expected = np.array([
      [9.80897665e-01, 8.94462891e-04, 1.79657674e-02, 1.21052389e-04, 1.21052389e-04],
      [8.78679856e-01, 1.18916387e-01, 8.01252314e-04, 8.01252314e-04, 8.01252314e-04]
    ])

    self.assertTrue(np.allclose(softmax(arg), expected))

  def test_loss(self):
    with self.assertRaises(AssertionError):
      loss([], [], L=0)
    
    with self.assertRaises(AssertionError):
      loss([], [], L=3)

    size = 10
    y = np.random.randint(2, size=size)
    yhat = np.copy(y)

    self.assertEqual(loss(yhat, y, L=1), 0)
    self.assertEqual(loss(yhat, y, L=2), 0)

    yhat = (y == 0).astype(int)
    self.assertEqual(loss(yhat, y, L=1), size)
    self.assertEqual(loss(yhat, y, L=2), size)

    y = np.array([1, 0, 0, 1, 1])
    yhat = np.array([.9, 0.2, 0.1, .4, .9])

    self.assertEqual(loss(yhat, y, L=1), 1.1)
    self.assertEqual(loss(yhat, y, L=2), 0.43)

class TestInitialization(unittest.TestCase):

  def test_initialize_parameters(self):
    for i in range(5, 8):
      for o in range(1, 4):
        layer_dimensions = [dimension for dimension in [i,o] if dimension != 0]
        parameters = initialize_parameters(layer_dimensions, use="zeros")
        self.assertEqual(len(parameters), 2)
        
        self.assertTrue(np.array_equal(parameters["W1"], np.zeros((o,i))))
        self.assertTrue(np.array_equal(parameters["b1"], np.zeros((o, 1))))
        for h1 in range(1, 4):
          layer_dimensions = [dimension for dimension in [i, h1, o] if dimension != 0]
          parameters = initialize_parameters(layer_dimensions, use="zeros")
          self.assertEqual(len(parameters), 4)
          
          self.assertTrue(np.array_equal(parameters["W1"], np.zeros((h1,i))))
          self.assertTrue(np.array_equal(parameters["b1"], np.zeros((h1, 1))))
          
          self.assertTrue(np.array_equal(parameters["W2"], np.zeros((o, h1))))
          self.assertTrue(np.array_equal(parameters["b2"], np.zeros((o, 1))))
          for h2 in range(7, 9):
            layer_dimensions = [dimension for dimension in [i,h1,h2,o] if dimension != 0]
            parameters = initialize_parameters(layer_dimensions, use="zeros")
            self.assertEqual(len(parameters), 6)
            
            self.assertTrue(np.array_equal(parameters["W1"], np.zeros((h1,i))))
            self.assertTrue(np.array_equal(parameters["b1"], np.zeros((h1, 1))))
            
            self.assertTrue(np.array_equal(parameters["W2"], np.zeros((h2, h1))))
            self.assertTrue(np.array_equal(parameters["b2"], np.zeros((h2, 1))))
            
            self.assertTrue(np.array_equal(parameters["W3"], np.zeros((o, h2))))
            self.assertTrue(np.array_equal(parameters["b3"], np.zeros((o, 1))))
    

  def test_initialize_lr_with_zeros(self):
    with self.assertRaises(ValueError):
      initialize_lr_with_zeros(0)

    for l in range(1,4):
      parameters = initialize_lr_with_zeros(l)
      self.assertTrue(np.array_equal(parameters['W1'], np.zeros((1,l))))
      self.assertEqual(parameters['b1'], 0)
      self.assertEqual(parameters['b1'].shape, (1, 1))

class TestPropagate(unittest.TestCase):

  def test__step_forward(self):
    A_prev = np.array([
      [-0.41675785, -0.05626683],
      [-2.1361961, 1.64027081],
      [-1.79343559, -0.84174737]
    ])
    W = np.array([[0.50288142, -1.24528809, -1.05795222]])
    b = np.array([[-0.90900761]])

    activation = 'sigmoid'
    A, ((cA_prev, cW, cb), (cZ, cActivation)) = _step_forward(A_prev, W, b, activation)
    self.assertTrue(np.allclose(A, [[0.96890023, 0.11013289]]))
    self.assertIs(A_prev, cA_prev)
    self.assertIs(W, cW)
    self.assertIs(b, cb)
    self.assertTrue(np.allclose(cZ, np.array([[3.43896134, -2.08938436]])))
    self.assertIs(activation, cActivation)

    activation = 'relu'
    A, ((cA_prev, cW, cb), (cZ, cActivation)) = _step_forward(A_prev, W, b, activation)
    self.assertTrue(np.allclose(A, [[3.43896131, 0.]]))
    self.assertIs(A_prev, cA_prev)
    self.assertIs(W, cW)
    self.assertIs(b, cb)
    self.assertTrue(np.allclose(cZ, np.array([[3.43896131, -2.08938436]])))
    self.assertIs(activation, cActivation)

  def test__propagate_forward(self):
    X = np.array([
      [-0.31178367, 0.72900392, 0.21782079, -0.8990918 ],
      [-2.48678065, 0.91325152, 1.12706373, -1.51409323],
      [1.63929108, -0.4298936, 2.63128056, 0.60182225],
      [-0.33588161, 1.23773784, 0.11112817, 0.12915125],
      [0.07612761, -0.15512816, 0.63422534, 0.810655]
    ])

    parameters = {
      'W1': np.array([
        [0.35480861, 1.81259031, -1.3564758 , -0.46363197, 0.82465384],
        [-1.17643148, 1.56448966, 0.71270509, -0.1810066 , 0.53419953],
        [-0.58661296, -1.48185327, 0.85724762, 0.94309899, 0.11444143],
        [-0.02195668, -2.12714455, -0.83440747, -0.46550831, 0.23371059]
      ]),
      'b1': np.array([
        [1.38503523],
        [-0.51962709],
        [-0.78015214],
        [0.95560959]
      ]),
      'W2': np.array([
        [-0.12673638, -1.36861282, 1.21848065, -0.85750144],
        [-0.56147088, -1.0335199 , 0.35877096, 1.07368134],
        [-0.37550472, 0.39636757, -0.47144628, 2.33660781]
      ]),
      'b2': np.array([
        [1.50278553],
        [-0.59545972],
        [0.52834106]
      ]),
      'W3': np.array([
        [0.9398248, 0.42628539, -0.75815703]
      ]),
      'b3': np.array([[-0.16236698]])
    }

    AL, caches = _propagate_forward(parameters, X)
    self.assertTrue(np.allclose(AL, np.array([[0.03921668, 0.70498921, 0.19734387, 0.04728177]])))
    self.assertEqual(len(caches), 3)
  
  def test__step_backward(self):
    dAL = np.array([[-0.41675785, -0.05626683]])
    A_prev = np.array([
      [-2.1361961, 1.64027081],
      [-1.79343559, -0.84174737],
      [0.50288142, -1.24528809]
    ])
    W = np.array([[-1.05795222, -0.90900761, 0.55145404]])
    b =  np.array([[2.29220801]])
    Z = np.array([[0.04153939, -1.11792545]])
    
    cache = ((A_prev, W, b), (Z, 'sigmoid'))
    dA_prev, dW, db = _step_backward(dAL, cache)

    self.assertTrue(np.allclose(dA_prev, np.array([[0.11017994, 0.01105339], [0.09466817, 0.00949723], [-0.05743092, -0.00576154]])))
    self.assertTrue(np.allclose(dW, np.array([[0.10266786, 0.09778551, -0.01968084]])))
    self.assertTrue(np.allclose(db, [[-0.05729622]]))
    
    cache = ((A_prev, W, b), (Z, 'relu'))
    dA_prev, dW, db = _step_backward(dAL, cache)

    self.assertTrue(np.allclose(dA_prev, np.array([[0.44090989, 0.], [0.37883606, 0.], [-0.2298228, 0.]])))
    self.assertTrue(np.allclose(dW, np.array([[0.44513824, 0.37371418, -0.10478989]])))
    self.assertTrue(np.allclose(db, [[-0.20837892]]))

  def test__propagate_back(self):
    AL = np.array([[1.78862847, 0.43650985]])
    Y = np.array([[1, 0]])
    A_prev = np.array([
      [0.09649747, -1.8634927],
      [-0.2773882 , -0.35475898],
      [-0.08274148, -0.62700068],
      [-0.04381817, -0.47721803]
    ])
    W = np.array([
      [-1.31386475,  0.88462238,  0.88131804,  1.70957306],
      [0.05003364, -0.40467741, -0.54535995, -1.54647732],
      [0.98236743, -1.10106763, -1.18504653, -0.2056499]
    ])
    b = np.array([
      [1.48614836],
      [0.23671627],
      [-1.02378514]
    ])
    Z = np.array([
      [-0.7129932 ,  0.62524497],
      [-0.16051336, -0.76883635],
      [-0.23003072,  0.74505627]
    ])
    first_cache = ((A_prev, W, b), (Z, 'relu'))

    A_prev = np.array([
      [1.97611078, -1.24412333],
      [-0.62641691, -0.80376609],
      [-2.41908317, -0.92379202]
    ])
    W = np.array([[-1.02387576,  1.12397796, -0.13191423]])
    b = np.array([[-1.62328545]])
    Z = np.array([[0.64667545, -0.35627076]])
    
    second_cache = ((A_prev, W, b), (Z, 'sigmoid'))
    
    caches = [first_cache, second_cache]

    expected = {
      'dW1': np.array([
        [ 0.41010002, 0.07807203, 0.13798444, 0.10502167],
        [0.,0.,0.,0.],
        [0.05283652, 0.01005865, 0.01777766, 0.0135308]
      ]),
      'db1': np.array([[-0.22007063], [0.], [-0.02835349]]),
      'dW2': np.array([[-0.39202432, -0.13325855, -0.04601089]]),
      'db2': np.array([[ 0.15187861]])
    }

    grads = _propagate_back(AL, Y, caches)

    self.assertTrue(np.allclose(expected['dW1'], grads['dW1']))
    self.assertTrue(np.allclose(expected['db1'], grads['db1']))
    self.assertTrue(np.allclose(expected['dW2'], grads['dW2']))
    self.assertTrue(np.allclose(expected['db2'], grads['db2']))

  def test__cost(self):
    Y, A = np.array([[1, 1, 1]]), np.array([[0.8, 0.9, 0.4]])
    self.assertEqual(_cost(A, Y), 0.414931599615397)
  
  def test_propagate(self):
    w, b, X, Y = np.array([[1., 2.]]), 2., np.array([[1.,2.,-1.],[3.,4.,-3.2]]), np.array([[1,0,1]])
    parameters = {
      'W1': w,
      'b1': b
    }
    grads, cost = propagate(parameters, X, Y)
    self.assertTrue(np.allclose(grads['dW1'], np.array([[0.99845601, 2.39507239]])))
    self.assertTrue(np.allclose(grads['db1'], np.array([[0.00145558]])))
    self.assertEqual(cost, 5.801545319394553)



if __name__ == '__main__':
  unittest.main()