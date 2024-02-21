from Quiz import *
import unittest


class TestCategories(unittest.TestCase):
    def test_type(self):
        self.assertTrue(type(categories) is list)

    def test_categories_len(self):
        self.assertEqual(len(category_fi), len(categories)/2, msg="Category_fi is not half of categories")

    def test_nonan(self):
        for i in range(len(vocab_chosen_cleaned)):
            self.assertTrue(type(vocab_chosen_cleaned[i]) is str)

    def test_vocabulary_len(self):
        self.assertGreater(len(vocab_chosen_cleaned), 5, msg="There must be at least 5 words in the list!")

    def test_samelen(self):
       self.assertEqual(len(vocab_chosen_cleaned), len(vocab_chosen_translated), msg="Both vocabulary list must be the same size")


if __name__ == '__main__':
    unittest.main()
