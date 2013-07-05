from pylearn2.datasets.cifar10 import CIFAR10
import unittest
from pylearn2.testing.skip import skip_if_no_data
import numpy as np

class TestCIFAR10(unittest.TestCase):
    def setUp(self):
        skip_if_no_data('cifar10')
        self.train = CIFAR10(which_set = 'train')
        self.test = CIFAR10(which_set = 'test')

    def test_topo(self):
        """Tests that a topological batch has 4 dimensions"""
        topo = self.train.get_batch_topo(1)
        self.assertEqual(topo.ndim, 4)

    def test_topo_c01b(self):
        """
        Tests that a topological batch with axes ('c',0,1,'b')
        can be dimshuffled back to match the standard ('b',0,1,'c')
        format.
        """
        batch_size = 100
        c01b_test = CIFAR10(which_set='test', axes=('c', 0, 1, 'b'))
        c01b_X = c01b_test.X[0:batch_size,:]
        c01b = c01b_test.get_topological_view(c01b_X)
        self.assertEqual(c01b.shape, (3, 32, 32, batch_size))
        b01c = c01b.transpose(3,1,2,0)
        b01c_X = self.test.X[0:batch_size,:]
        self.assertEqual(c01b_X.shape, b01c_X.shape)
        np.testing.assert_equal(c01b_X, b01c_X)
        b01c_direct = self.test.get_topological_view(b01c_X)
        self.assertEqual(b01c_direct.shape, b01c.shape)
        np.testing.assert_equal(b01c_direct, b01c)
