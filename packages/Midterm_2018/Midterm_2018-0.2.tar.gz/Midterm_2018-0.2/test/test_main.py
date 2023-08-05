#!/usr/bin/python
 
import unittest
 
def raiseException():
    raise ValueError('Invalid value ...');
 
class SimplisticTest(unittest.TestCase):
 
    def setUp(self):
        self.fixture = range(1, 10);
        print 'In setUp ...';
 
    def tearDown(self):
        del self.fixture;
        print 'In tearDown ...';
 
    def test(self):
        self.failUnless(True);
 
    def testFail(self):
        self.failIf(False, 'Test fail ...');
 
    def testError(self):
        raise RuntimeError('Test error ...');
 
    def testAssertTrue(self):
        self.assertTrue(True, 'Test assert true ...');
 
    def testAssertFalse(self):
        self.assertFalse(False);
 
    def testEqual(self):
        self.failUnlessEqual(1, 3-2);
 
    def testRaiseError(self):
        self.failUnlessRaises(ValueError, raiseException);
 
class secondTest(unittest.TestCase):
 
    def testSecond(self):
        print 'test second ...';
 
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimplisticTest);
    suite_2 = unittest.TestLoader().loadTestsFromTestCase(secondTest);
    allTests = unittest.TestSuite([suite, suite_2]);
    #unittest.TextTestRunner(verbosity=2).run(allTests);
    unittest.main();
