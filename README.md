# mess-reminder

Sends mess meal reminders (Breakfast, Lunch, Snacks, Dinner) on a schedule via GitHub Actions.

## Notifications

Notifications are sent to:

- **ntfy.sh** — set the `NTFY_TOPIC` repo secret to your ntfy topic.
- **WhatsApp** (via [CallMeBot](https://www.callmebot.com/blog/free-api-whatsapp-messages/)) — sent to every subscriber in the `WHATSAPP_SUBSCRIBERS` secret. Skipped automatically if that secret is empty/unset.

### WhatsApp setup (CallMeBot)

Each person who wants reminders does a **one-time activation**, then you add them to a shared list:

1. They save `+34 644 71 81 99` as a contact on their phone.
2. They send it the WhatsApp message: `I allow callmebot to send me messages`.
3. Within a couple of minutes, CallMeBot replies with their personal API key. (If nothing arrives, they can try again after 24 hours — the free bot is occasionally overloaded.)
4. They send you their phone number and that API key (however you'd like — WhatsApp, etc).
5. You add/update the `WHATSAPP_SUBSCRIBERS` repo secret (Settings → Secrets and variables → Actions) as a JSON array with one entry per person:

   ```json
   [
     {"phone": "919876543210", "apikey": "1234567"},
     {"phone": "34600111222", "apikey": "7654321"}
   ]
   ```

   `phone` is the international format with no `+`, spaces, or leading zeros.

To add or remove someone, edit that secret's JSON and save — no code changes needed.

Phone numbers and API keys live only in this GitHub secret, never in the repo itself, since this repo is public.
