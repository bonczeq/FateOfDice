import unittest

from fate_of_dice.common.presentation import SymbolResolver


class TestSymbolResolver(unittest.TestCase):

    def test_arrow_character(self):
        symbol = SymbolResolver.arrow_character()
        self.assertEqual('🠖', symbol)

    def test_circled_number(self):
        self.assertEqual(SymbolResolver.circled_number(6, 6), '🗹')
        self.assertEqual(SymbolResolver.circled_number(1, 6, 1), '🞮')
        self.assertEqual('➀', SymbolResolver.circled_number(1))
        self.assertEqual('➁', SymbolResolver.circled_number(2))
        self.assertEqual('➂', SymbolResolver.circled_number(3))
        self.assertEqual('➃', SymbolResolver.circled_number(4))
        self.assertEqual('➄', SymbolResolver.circled_number(5))
        self.assertEqual('➅', SymbolResolver.circled_number(6))
        self.assertEqual('➆', SymbolResolver.circled_number(7))
        self.assertEqual('➇', SymbolResolver.circled_number(8))
        self.assertEqual('➈', SymbolResolver.circled_number(9))
        self.assertEqual('➉', SymbolResolver.circled_number(10))

    def test_dice(self):
        self.assertEqual('⚀', SymbolResolver.dice(1))
        self.assertEqual('⚁', SymbolResolver.dice(2))
        self.assertEqual('⚂', SymbolResolver.dice(3))
        self.assertEqual('⚃', SymbolResolver.dice(4))
        self.assertEqual('⚄', SymbolResolver.dice(5))
        self.assertEqual('⚅', SymbolResolver.dice(6))


if __name__ == '__main__':
    unittest.main()
