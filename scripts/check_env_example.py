from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / ".env.example").read_text(encoding="utf-8")
required = [
    "TELEGRAM_API_TOKEN=",
    "ADMIN_CHAT_ID=",
    "INSTITUTE_CHAT_ID=",
]

missing = [line for line in required if line not in text]
if missing:
    print("Missing env names: " + ", ".join(missing))
    raise SystemExit(1)

print("Env example check passed")