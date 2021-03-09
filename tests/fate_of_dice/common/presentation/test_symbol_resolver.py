import unittest

from fate_of_dice.common.presentation import SymbolResolver


class TestSymbolResolver(unittest.TestCase):

    def test_arrow_character(self):
        symbol = SymbolResolver.arrow_character()
        self.assertEqual(symbol, '🠖')

    def test_circled_number(self):
        self.assertEqual(SymbolResolver.circled_number(6, 6), '🗹')
        self.assertEqual(SymbolResolver.circled_number(1, 6, 1), '🞮')
        self.assertEqual(SymbolResolver.circled_number(1), '➀')
        self.assertEqual(SymbolResolver.circled_number(2), '➁')
        self.assertEqual(SymbolResolver.circled_number(3), '➂')
        self.assertEqual(SymbolResolver.circled_number(4), '➃')
        self.assertEqual(SymbolResolver.circled_number(5), '➄')
        self.assertEqual(SymbolResolver.circled_number(6), '➅')
        self.assertEqual(SymbolResolver.circled_number(7), '➆')
        self.assertEqual(SymbolResolver.circled_number(8), '➇')
        self.assertEqual(SymbolResolver.circled_number(9), '➈')
        self.assertEqual(SymbolResolver.circled_number(10), '➉')

    def test_dice(self):
        self.assertEqual(SymbolResolver.dice(1), '⚀')
        self.assertEqual(SymbolResolver.dice(2), '⚁')
        self.assertEqual(SymbolResolver.dice(3), '⚂')
        self.assertEqual(SymbolResolver.dice(4), '⚃')
        self.assertEqual(SymbolResolver.dice(5), '⚄')
        self.assertEqual(SymbolResolver.dice(6), '⚅')


if __name__ == '__main__':
    unittest.main()
