# Forwarding

The bot forwards feature ideas to the admin chat and program suggestions to the institute chat.

Those chat IDs come from environment variables. I keep them out of the repo because they are deployment values.

If forwarding fails in production, I check the chat ID and bot permission first.
