import unittest

from main import find_matching_questions, split_command


class BotInputTests(unittest.TestCase):
    def test_empty_text_does_not_match_any_question(self):
        questions = ["Course price", "Class time"]

        self.assertEqual(find_matching_questions("", questions), [])
        self.assertEqual(find_matching_questions("   ", questions), [])

    def test_matching_is_case_insensitive(self):
        questions = ["Course price", "Class time"]

        self.assertEqual(find_matching_questions("PRICE", questions), ["Course price"])

    def test_command_keeps_argument(self):
        command, argument = split_command("/search algebra")

        self.assertEqual(command, "/search")
        self.assertEqual(argument, "algebra")

    def test_command_removes_bot_name(self):
        command, argument = split_command("/help@AbzumsBot")

        self.assertEqual(command, "/help")
        self.assertEqual(argument, "")


if __name__ == "__main__":
    unittest.main()
