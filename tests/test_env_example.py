from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EnvExampleTests(unittest.TestCase):
    def test_expected_names_are_listed(self):
        text = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("TELEGRAM_API_TOKEN=", text)
        self.assertIn("ADMIN_CHAT_ID=", text)
        self.assertIn("INSTITUTE_CHAT_ID=", text)


if __name__ == "__main__":
    unittest.main()
