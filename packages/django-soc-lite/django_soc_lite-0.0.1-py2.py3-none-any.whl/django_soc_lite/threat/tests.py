from django.test import TestCase
from mock import Mock
from middleware import ThreatEquationMiddleware

class CartMiddlewareTest(TestCase):

    def setUp(self):
        self.cm = ThreatEquationMiddleware()
        self.request = Mock()
        self.request.session = {}
    def test_process_request_without_cart(self):
        self.assertEqual(self.cm.process_request(self.request), None)


"""
def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.middleware = self.ThreatEquationMiddleware()
        self.request = RequestFactory().get('/')
        self.middleware.process_request(self.request)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

"""
#python -m unittest tests
#python tests.py
