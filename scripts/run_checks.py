import subprocess
import sys

commands = [
    [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
    [sys.executable, "scripts/check_qa_data.py"],
    [sys.executable, "scripts/check_env_example.py"],
]

for command in commands:
    result = subprocess.run(command)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

print("Bot checks passed")