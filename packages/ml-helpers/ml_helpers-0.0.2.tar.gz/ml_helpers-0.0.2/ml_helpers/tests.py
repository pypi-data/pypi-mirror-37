import unittest
import numpy as np
from activations import sigmoid, sigmoid_derivative
from utils import vectorize, normalize_rows, softmax, loss

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

if __name__ == '__main__':
  unittest.main()