# Message flow

The main loop reads updates, skips non message updates, then handles text commands.

The order matters:

1. Commands are parsed first.
2. Numbered answers are checked after commands.
3. Free text is matched against question keys.
4. A fallback message is sent when nothing matches.

Small helper functions keep the parsing behavior easy to test.
