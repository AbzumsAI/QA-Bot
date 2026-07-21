import unittest

from qa import qa


class QaDataTests(unittest.TestCase):
    def test_questions_and_answers_are_not_empty(self):
        self.assertGreater(len(qa), 0)
        for question, answer in qa.items():
            with self.subTest(question=question):
                self.assertTrue(question.strip())
                self.assertTrue(str(answer).strip())


if __name__ == "__main__":
    unittest.main()
