import unittest
import totalUp_test
import buy_test
import sell_test
import borrowLoan_test
import payLoan_test
import paycheck_test
import doodad_test
import insurance_test
import naturalDisaster_test
import pollution_test
import baby_test
import charity_test
import downsized_test
import forcedSale_test
import mentor_test
import REUpgrade_test
import recessionTradeImproves_test


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_fail(self):
        self.assertFalse(False)


if __name__ == '__main__':
    unittest.main()
