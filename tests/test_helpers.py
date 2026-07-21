import unittest

from main import build_numbered_lines, normalize_lookup_text, select_question_by_number


class HelperTests(unittest.TestCase):
    def test_normalize_lookup_text_collapses_spaces(self):
        self.assertEqual(normalize_lookup_text("  Course   PRICE  "), "course price")

    def test_build_numbered_lines(self):
        self.assertEqual(build_numbered_lines(["A", "B"]), "1. A\n2. B\n")

    def test_select_question_by_number(self):
        questions = ["One", "Two"]
        self.assertEqual(select_question_by_number("2", questions), "Two")
        self.assertIsNone(select_question_by_number("3", questions))
        self.assertIsNone(select_question_by_number("two", questions))


if __name__ == "__main__":
    unittest.main()
