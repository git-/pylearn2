from pylearn2.datasets.mnist import MNIST
import unittest
import numpy as np

from nose.plugins.skip import SkipTest
from pylearn2.datasets.exc import NoDataPathError, NotInstalledError


class TestMNIST(unittest.TestCase):
    def setUp(self):
        try:
            self.train = MNIST(which_set = 'train')
            self.test = MNIST(which_set = 'test')
        except (NoDataPathError, NotInstalledError):
            raise SkipTest()

    def test_range(self):
        """Tests that the data spans [0,1]"""
        for X in [self.train.X, self.test.X ]:
            self.assertTrue(X.min() == 0.0)
            self.assertTrue(X.max() == 1.0)

    def test_topo(self):
        """Tests that a topological batch has 4 dimensions"""
        topo = self.train.get_batch_topo(1)
        self.assertTrue(topo.ndim == 4)

    def test_topo_c01b(self):
        """
        Tests that a topological batch with axes ('c',0,1,'b')
        can be dimshuffled back to match the standard ('b',0,1,'c')
        format.
        """
        try:
            batch_size = 100
            c01b_test = MNIST(which_set='test', axes=('c', 0, 1, 'b'))
            c01b_X = c01b_test.X[0:batch_size,:]
            c01b = c01b_test.get_topological_view(c01b_X)
            self.assertTrue(c01b.shape == (1, 28, 28, batch_size))
            b01c = c01b.transpose(3,1,2,0)
            b01c_X = self.test.X[0:batch_size,:]
            self.assertTrue(c01b_X.shape == b01c_X.shape)
            self.assertTrue(np.all(c01b_X == b01c_X))
            b01c_direct = self.test.get_topological_view(b01c_X)
            self.assertTrue(b01c_direct.shape == b01c.shape)
            self.assertTrue(np.all(b01c_direct == b01c))
        except (NoDataPathError, NotInstalledError):
            raise SkipTest()

