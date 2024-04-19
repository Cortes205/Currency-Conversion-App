import unittest
import os
import sys
import inspect
current = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent = os.path.dirname(current)
sys.path.insert(0, parent)
import main


class TestSearch(unittest.TestCase):

    def test_validCurrencies(self):
        print("Testing a Search for Each Currency")
        for index in range(0, len(main.currency_names)):
            # For whatever reason, the Belarusian Ruble is on the currency list twice
            # Generalized to omit a test if there exists another instance of a currency
            if index > 0:
                if main.currency_names[index] == main.currency_names[index-1]:
                    continue
            index_found = main.currency_search(main.currency_names[index])
            print(f'Searching for {main.currency_names[index]}\n\tExpected: {index}\n\tResult: {index_found}')
            self.assertEqual(index, index_found)

    def test_invalidCurrencies(self):
        print("Testing a Search for Non-Existent Currencies")

        index_found = main.currency_search("A")
        print(f'Searching for A\n\tExpected: -1\n\tResult: {index_found}')
        self.assertEqual(index_found, -1)

        index_found = main.currency_search("AB")
        print(f'Searching for AB\n\tExpected: -1\n\tResult: {index_found}')
        self.assertEqual(index_found, -1)

        index_found = main.currency_search("HIJ")
        print(f'Searching for HIJ\n\tExpected: -1\n\tResult: {index_found}')
        self.assertEqual(index_found, -1)

        index_found = main.currency_search("LMNO")
        print(f'Searching for LMNO\n\tExpected: -1\n\tResult: {index_found}')
        self.assertEqual(index_found, -1)

        index_found = main.currency_search("QRSTU")
        print(f'Searching for QRSTU\n\tExpected: -1\n\tResult: {index_found}')
        self.assertEqual(index_found, -1)

        index_found = main.currency_search("lowercase input")
        print(f'Searching for lowercase input\n\tExpected: -1\n\tResult: {index_found}')
        self.assertEqual(index_found, -1)

        index_found = main.currency_search("TESTING LARGE STRING WITH SPACES")
        print(f'Searching for TESTING LARGE STRING WITH SPACES\n\tExpected: -1\n\tResult: {index_found}')
        self.assertEqual(index_found, -1)


if __name__ == '__main__':
    unittest.main()
