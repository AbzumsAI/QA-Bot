# Testing

Run the unit tests before changing command parsing or matching.

```powershell
python -m unittest discover -s tests
```

Run the local checks with:

```powershell
python scripts\run_checks.py
```

The tests do not call Telegram.
