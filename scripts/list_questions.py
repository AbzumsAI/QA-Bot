from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qa import qa

for index, question in enumerate(qa, start=1):
    print(f"{index}. {question}")