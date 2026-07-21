from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qa import qa

errors = []
for question, answer in qa.items():
    if not question.strip():
        errors.append("empty question")
    if not str(answer).strip():
        errors.append(f"empty answer for {question!r}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print(f"Checked {len(qa)} question answers")