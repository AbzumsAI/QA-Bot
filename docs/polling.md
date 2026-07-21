# Polling

The bot uses Telegram long polling through `getUpdates`.

`TELEGRAM_POLL_TIMEOUT` controls the long poll wait. `TELEGRAM_REQUEST_TIMEOUT` controls normal request calls.

When network errors happen, `get_updates` returns an error shape instead of crashing the loop.
