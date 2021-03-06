from pylearn2.datasets.norb_small import NORBSmall, FoveatedNORB
import unittest
import numpy

from nose.plugins.skip import SkipTest
from pylearn2.datasets.exc import NoDataPathError, NotInstalledError


class TestNORBSmall(unittest.TestCase):
    def setUp(self):
        try:
            self.train = NORBSmall(which_set='train')
            self.test = NORBSmall(which_set='test')
        except (NoDataPathError, NotInstalledError):
            raise SkipTest()

        #NORBSmall doesn't define any extra method of its own aside from
        #the @classmethod load(...) which is called by the constructor.

class TestFoveatedNORB(unittest.TestCase):
    def setUp(self):
        try:
            self.train = FoveatedNORB(which_set='train')
            self.test = FoveatedNORB(which_set='test')
            self.train_one_hot = self.train.convert_to_one_hot()
            self.test_one_hot = self.test.convert_to_one_hot()
        except (NoDataPathError, NotInstalledError):
            raise SkipTest()

    def test_one_hot(self):
        train_non_zeros = numpy.transpose(numpy.nonzeros(self.train_one_hot))
        test_non_zeros = numpy.transpose(numpy.nonzeros(self.test_one_hot))
        self.assertEquals(len(train_non_zeros), 1)
        self.assertEquals(len(test_non_zeros), 1)
        self.assertEquals(self.train_one_hot[train_non_zeros[0]], 1)
        self.assertEquals(self.test_one_hot[test_non_zeros[0]], 1)

    def test_restrict_instances(self):
        pass
        #TODO: what are 'instances' and how do I generate one to perform testing?
